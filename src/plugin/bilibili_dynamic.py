# encoding:utf-8
"""定时推送b站动态
"""
from bilibili_api.user import User
from nonebot import get_bot, require, on_command
from nonebot.adapters.onebot.v11 import Message, Event
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.exception import ActionFailed
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from .core.data_base import Database
from .utils import json_str_to_obj, obj_to_json_str


# 设置定时任务
BilibiliDynamic = require('nonebot_plugin_apscheduler').scheduler
@BilibiliDynamic.scheduled_job('interval', minutes=1)
async def _scheduler() -> None:
    """定时获取b站动态并自动推送
    """
    bot = get_bot()
    _db = Database()
    sql = """SELECT `uid`, `gids`, `did` FROM `bilibili_dynamic`"""
    _db.execute(sql)
    res = _db.fetchall()
    for _ in res:
        uid, gids, did = tuple(map(json_str_to_obj, _))
        user = User(uid)
        dyna = (await user.get_dynamics())['cards'][0]
        latest_did = dyna['desc']['dynamic_id']
        if did == latest_did: # 没有动态更新
            continue
        messages = []
        if dyna['desc']['type'] == 2: # 文字+图片动态
            messages.append(dyna['card']['item']['description'])
            for picture in dyna['card']['item']['pictures']:
                messages.append(f"[CQ:image,file={picture['img_src']}]")
        elif dyna['desc']['type'] == 8: # 视频动态
            messages.append(dyna['card']['dynamic'])
            messages.append(
                dyna['card']['title']
                +f"\n[CQ:image,file={dyna['card']['pic']}]"
                +f"\n➥{dyna['card']['short_link']}")
        try: # 防止某些群发送失败而没有即使更新did的值
            for group_id in gids: # 发送消息
                for message in messages:
                    await bot.call_api(
                        'send_group_msg',
                        group_id = group_id,
                        message = message)
        except ActionFailed as _:
            print(_)
        finally:
            sql = """UPDATE `bilibili_dynamic`
                SET `did`=%s WHERE `uid`=%s"""
            args = tuple(map(obj_to_json_str, (latest_did, uid)))
            _db.execute(sql, args)

# 添加动态订阅
AddBiliDyna = on_command(
    cmd='AddBiliDyna',
    rule=to_me(),
    aliases={'添加动态订阅'},
    permission=SUPERUSER)
@AddBiliDyna.handle()
async def _handler(matcher: Matcher, args: Message = CommandArg()) -> None:
    """对带参调用直接给变量赋值

    参数:
        matcher (Matcher): matcher
        args (Message, optional): 参数纯文本. Defaults to CommandArg().
    """
    if len(args) > 0:
        matcher.set_arg('AddBiliDyna_args', args)
@AddBiliDyna.got('AddBiliDyna_args', prompt='请输入b站up的uid')
async def _gotter(matcher: Matcher, event: Event, state: T_State) -> None:
    """添加一个动态订阅

    参数:
        matcher (Matcher): Matcher
        event (Event): Event
        state (T_State): T_State
    """
    args = state['AddBiliDyna_args']
    if len(args) == 0:
        AddBiliDyna.reject('请输入用户的uid')
    args = args.extract_plain_text().strip().split(' ')
    if len(args) == 1:
        _, gid, _ = event.get_session_id().split('_')
        uid = args[0]
    elif len(args) == 2:
        uid, gid = args
    else:
        return None
    _db = Database()
    sql = """SELECT `gids` FROM `bilibili_dynamic` WHERE `uid`=%s"""
    args = obj_to_json_str(uid)
    _db.execute(sql, args)
    res = _db.fetchone()
    if res is None:
        sql = """INSERT INTO `bilibili_dynamic`
            SET `uid`=%s, `gids`=%s, `did`=%s"""
        args = tuple(map(obj_to_json_str, (uid, [gid], 0)))
    else:
        gids = json_str_to_obj(res[0])
        if gid in gids:
            await matcher.finish('动态订阅已存在')
        gids += [gid]
        sql = """UPDATE `bilibili_dynamic`
            SET `gids`=%s WHERE `uid`=%s"""
        args = tuple(map(obj_to_json_str, (gids, uid)))
    _db.execute(sql, args)
    await matcher.send('成功添加动态订阅')

# 删除动态订阅
DelBiliDyna = on_command(
    cmd='DelBiliDyna',
    rule=to_me(),
    aliases={'删除动态订阅'},
    permission=SUPERUSER)
@DelBiliDyna.handle()
async def _handler(matcher: Matcher, args: Message = CommandArg()) -> None:
    """对带参调用直接给变量赋值

    参数:
        matcher (Matcher): matcher
        args (Message, optional): 参数纯文本. Defaults to CommandArg().
    """
    if len(args) > 0:
        matcher.set_arg('DelBiliDyna_args', args)
@DelBiliDyna.got('DelBiliDyna_args', prompt='请输入b站up的uid')
async def _gotter(matcher: Matcher, event: Event, state: T_State) -> None:
    """删除一个动态订阅

    参数:
        matcher (Matcher): Matcher
        event (Event): Event
        state (T_State): T_State
    """
    args = state['DelBiliDyna_args']
    if len(args) == 0:
        DelBiliDyna.reject('请输入用户的uid')
    args = args.extract_plain_text().strip().split(' ')
    if len(args) == 1:
        _, gid, _ = event.get_session_id().split('_')
        uid = args[0]
    elif len(args) == 2:
        uid, gid = args
    else:
        return None
    _db = Database()
    sql = """SELECT `gids` FROM `bilibili_dynamic` WHERE `uid`=%s"""
    args = obj_to_json_str(uid)
    _db.execute(sql, args)
    res = _db.fetchone()
    if res is None: # 该uid不存在
        await matcher.finish('该订阅不存在')
    gids = json_str_to_obj(res[0])
    if gid not in gids: # 该群没有订阅该用户
        await matcher.finish('该订阅不存在')
    gids.remove(gid)
    sql = """UPDATE `bilibili_dynamic`
        SET `gids`=%s WHERE `uid`=%s"""
    args = tuple(map(obj_to_json_str, (gids, uid)))
    _db.execute(sql, args)
    await matcher.send('成功删除订阅')
