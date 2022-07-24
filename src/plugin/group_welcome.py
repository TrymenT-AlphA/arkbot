"""入群提醒
"""
from nonebot import on_command
from nonebot import on_notice
from nonebot.matcher import Matcher
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Event
from nonebot.adapters.onebot.v11 import Message
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11 import GroupIncreaseNoticeEvent
from .core.data_base import MySQL

# 注册群成员增加响应函数
GroupWelcome = on_notice()


@GroupWelcome.handle()
async def _handler(matcher: Matcher, event: GroupIncreaseNoticeEvent) -> None:
    """当有新成员入群时,如果数据库中有入群欢迎,输出入群欢迎
    """
    _, group_id, user_id = event.get_session_id().split('_')
    _db = MySQL()
    res = _db.select_one(
        table='group_welcome',
        keys=('msg',),
        condition='`gid`=%s',
        args=(group_id,)
    )
    if res:  # 设置了入群欢迎词
        await matcher.finish(MessageSegment.at(user_id) + res['msg'])


# 设置入群欢迎词
AddWelcomeMSG = on_command(
    cmd='AddWelcomeMSG',
    rule=to_me(),
    aliases={'添加入群欢迎'})


@AddWelcomeMSG.handle()
async def _handler(matcher: Matcher, args: Message = CommandArg()) -> None:
    """对带参调用直接给变量赋值
    """
    if len(args) > 0:
        matcher.set_arg('AddWelcomeMSG_args', args)


@AddWelcomeMSG.got('AddWelcomeMSG_args', prompt='请输入入群欢迎词')
async def _gotter(matcher: Matcher, event: Event, state: T_State) -> None:
    """获取入群欢迎词并存入数据库
    """
    args = state['AddWelcomeMSG_args']
    if len(args) == 0:
        await AddWelcomeMSG.reject('请输入入群欢迎词')
    args = args.extract_plain_text().strip().split(' ')
    if len(args) == 1:
        _, gid, _ = event.get_session_id().split('_')
        msg = args[0]
    elif len(args) == 2:
        gid, msg = args
    else:
        return None
    _db = MySQL()
    res = _db.select_one(
        table='group_welcome',
        keys=('gid',),
        condition='`gid`=%s',
        args=(gid,)
    )
    if not res:
        _db.insert(
            table='group_welcome',
            keys=('gid', 'msg'),
            vals=(gid, msg)
        )
        await matcher.finish('成功添加入群欢迎')
    else:
        _db.update(
            table='group_welcome',
            keys=('msg',),
            vals=(msg,),
            condition='`gid`=%s',
            args=(gid,)
        )
        await matcher.finish('成功覆盖入群欢迎')


# 删除入群欢迎
DelWelcomeMSG = on_command(
    cmd='DelWelcomeMSG',
    rule=to_me(),
    aliases={'删除入群欢迎'},
    permission=SUPERUSER)


@DelWelcomeMSG.handle()
async def _handler(matcher: Matcher, event: Event, args: Message = CommandArg()) -> None:
    """删除数据库中相关的数据
    """
    _db = MySQL()
    if len(args) == 0:
        _, gid, _ = event.get_session_id().split('_')
    elif len(args) == 1:
        gid = args.extract_plain_text()
    else:
        return
    res = _db.select_one(
        table='group_welcome',
        keys=('gid',),
        condition='`gid`=%s',
        args=(gid,)
    )
    if res:
        _db.delete(
            table='group_welcome',
            condition='`gid`=%s',
            args=(gid,)
        )
        await matcher.finish('成功删除入群欢迎')
    await matcher.finish('不存在入群欢迎')
