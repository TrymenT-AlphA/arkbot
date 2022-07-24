"""定时推送b站动态
"""
from bilibili_api.user import User
from nonebot import get_bot
from nonebot import require
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Event
from nonebot.adapters.onebot.v11 import Message
from nonebot.adapters.onebot.exception import ActionFailed
from .core.data_base import MySQL


BilibiliDynamic = require('nonebot_plugin_apscheduler').scheduler


@BilibiliDynamic.scheduled_job('interval', minutes=1)
async def _scheduler() -> None:
    """定时获取b站动态并自动推送
    """
    bot = get_bot()
    _db = MySQL()
    res = _db.select_all(
        table='bilibili_dynamic',
        keys=('uid', 'gids', 'did')
    )
    for _ in res:
        uid, gids, did = _.values()
        user = User(uid)
        dyna = (await user.get_dynamics())['cards'][0]
        latest_did = dyna['desc']['dynamic_id']
        if did == latest_did:  # 没有动态更新
            continue
        messages = []
        if dyna['desc']['type'] == 2:  # 文字+图片动态
            messages.append(dyna['card']['item']['description'])
            for picture in dyna['card']['item']['pictures']:
                messages.append(f"[CQ:image,file={picture['img_src']}]")
        elif dyna['desc']['type'] == 8:  # 视频动态
            messages.append(dyna['card']['dynamic'])
            messages.append(
                dyna['card']['title']
                + f"\n[CQ:image,file={dyna['card']['pic']}]"
                + f"\n➥{dyna['card']['short_link']}"
            )
        try:  # 防止某些群发送失败而没有即使更新did的值
            for group_id in gids:  # 发送消息
                for message in messages:
                    await bot.call_api(
                        'send_group_msg',
                        group_id=group_id,
                        message=message
                    )
        except ActionFailed as e:
            print(e)
        finally:
            _db.update(
                table='bilibili_dynamic',
                keys=('did',),
                vals=(latest_did,),
                condition='`uid`=%s',
                args=(uid,)
            )


AddBiliDyna = on_command(
    cmd='AddBiliDyna',
    rule=to_me(),
    aliases={'添加动态订阅'},
    permission=SUPERUSER)


@AddBiliDyna.handle()
async def _handler(matcher: Matcher, args: Message = CommandArg()) -> None:
    """对带参调用直接给变量赋值
    """
    if len(args) > 0:
        matcher.set_arg('AddBiliDyna_args', args)


@AddBiliDyna.got('AddBiliDyna_args', prompt='请输入b站up的uid')
async def _gotter(matcher: Matcher, event: Event, state: T_State) -> None:
    """添加一个动态订阅
    """
    args = state['AddBiliDyna_args']
    if len(args) == 0:
        await AddBiliDyna.reject('请输入用户的uid')
    args = args.extract_plain_text().strip().split(' ')
    if len(args) == 1:
        _, gid, _ = event.get_session_id().split('_')
        uid = args[0]
    elif len(args) == 2:
        uid, gid = args
    else:
        return None

    _db = MySQL()
    res = _db.select_one(
        table='bilibili_dynamic',
        keys=('gids',),
        condition='`uid`=%s',
        args=(uid,)
    )
    if res:
        if gid in res['gids']:
            await matcher.finish('动态订阅已存在')
        res['gids'] += [gid]
        _db.update(
            table='bilibili_dynamic',
            keys=('gids',),
            vals=(res['gids'],),
            condition='`uid`=%s',
            args=(uid,)
        )
    else:
        _db.insert(
            table='bilibili_dynamic',
            keys=('uid', 'gids', 'did'),
            vals=(uid, [gid], 0)
        )
    await matcher.send('成功添加动态订阅')


DelBiliDyna = on_command(
    cmd='DelBiliDyna',
    rule=to_me(),
    aliases={'删除动态订阅'},
    permission=SUPERUSER)


@DelBiliDyna.handle()
async def _handler(matcher: Matcher, args: Message = CommandArg()) -> None:
    """对带参调用直接给变量赋值
    """
    if len(args) > 0:
        matcher.set_arg('DelBiliDyna_args', args)


@DelBiliDyna.got('DelBiliDyna_args', prompt='请输入b站up的uid')
async def _gotter(matcher: Matcher, event: Event, state: T_State) -> None:
    """删除一个动态订阅
    """
    args = state['DelBiliDyna_args']
    if len(args) == 0:
        await DelBiliDyna.reject('请输入用户的uid')
    args = args.extract_plain_text().strip().split(' ')
    if len(args) == 1:
        _, gid, _ = event.get_session_id().split('_')
        uid = args[0]
    elif len(args) == 2:
        uid, gid = args
    else:
        return None
    _db = MySQL()
    res = _db.select_one(
        table='bilibili_dynamic',
        keys=('gids',),
        condition='`uid`=%s',
        args=(uid,)
    )
    if not res:
        await matcher.finish('该订阅不存在')
    if gid not in res['gids']:
        await matcher.finish('该订阅不存在')
    res['gids'].remove(gid)
    _db.update(
        table='bilibili_dynamic',
        keys=('gids',),
        vals=(res['gids'],),
        condition='`uid`=%s',
        args=(uid,)
    )
    await matcher.send('成功删除订阅')
