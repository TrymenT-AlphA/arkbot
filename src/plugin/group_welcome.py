"""入群提醒
"""
from nonebot import on_command, on_notice
from nonebot.adapters.onebot.v11 import GroupIncreaseNoticeEvent, MessageSegment, Message, Event
from nonebot.matcher import Matcher
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from .core.data_base import Database
from .utils import obj_to_json_str, json_str_to_obj

# 注册群成员增加响应函数
GroupWelcome = on_notice()


@GroupWelcome.handle()
async def _handler(matcher: Matcher, event: GroupIncreaseNoticeEvent) -> None:
    """当有新成员入群时,如果数据库中有入群欢迎,输出入群欢迎

    参数:
        matcher (Matcher): matcher
        event (GroupIncreaseNoticeEvent): 新成员入群事件
    """
    _, group_id, user_id = event.get_session_id().split('_')
    _db = Database()
    sql = """SELECT `msg` FROM `group_welcome` WHERE `gid`=%s"""
    args = obj_to_json_str(group_id)
    _db.execute(sql, args)
    res = _db.fetchone()
    if res is not None:  # 设置了入群欢迎词
        await matcher.finish(MessageSegment.at(user_id) + json_str_to_obj(res[0]))


# 设置入群欢迎词
AddWelcomeMSG = on_command(
    cmd='AddWelcomeMSG',
    rule=to_me(),
    aliases={'添加入群欢迎'})


@AddWelcomeMSG.handle()
async def _handler(matcher: Matcher, args: Message = CommandArg()) -> None:
    """对带参调用直接给变量赋值

    参数:
        matcher (Matcher): matcher
        args (Message, optional): 参数纯文本. Defaults to CommandArg().
    """
    if len(args) > 0:
        matcher.set_arg('AddWelcomeMSG_args', args)


@AddWelcomeMSG.got('AddWelcomeMSG_args', prompt='请输入入群欢迎词')
async def _gotter(matcher: Matcher, event: Event, state: T_State) -> None:
    """获取入群欢迎词并存入数据库

    参数:
        matcher (Matcher): Matcher
        event (Event): Event
        state (T_State): T_State
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
    _db = Database()
    sql = """SELECT `gid` FROM `group_welcome` WHERE `gid`=%s"""
    args = obj_to_json_str(gid)
    _db.execute(sql, args)
    if _db.fetchone() is None:
        sql = """INSERT INTO `group_welcome` SET `gid`=%s, `msg`=%s"""
        args = tuple(map(obj_to_json_str, (gid, msg)))
        msg = '成功添加入群欢迎'
    else:
        sql = """UPDATE `group_welcome` SET `msg`=%s WHERE `gid`=%s"""
        args = tuple(map(obj_to_json_str, (msg, gid)))
        msg = '成功覆盖入群欢迎'
    _db.execute(sql, args)
    await matcher.finish(msg)


# 删除入群欢迎
DelWelcomeMSG = on_command(
    cmd='DelWelcomeMSG',
    rule=to_me(),
    aliases={'删除入群欢迎'},
    permission=SUPERUSER)


@DelWelcomeMSG.handle()
async def _handler(matcher: Matcher, event: Event, args: Message = CommandArg()) -> None:
    """删除数据库中相关的数据

    参数:
        matcher (Matcher): Matcher
        event (Event): Event
        args (Message): 参数. 默认CommandArg()
    """
    _db = Database()
    if len(args) == 0:
        _, gid, _ = event.get_session_id().split('_')
    elif len(args) == 1:
        gid = args.extract_plain_text()
    else:
        return None
    sql = """SELECT `gid` FROM `group_welcome` WHERE `gid`=%s"""
    args = obj_to_json_str(gid)
    _db.execute(sql, args)
    if _db.fetchone() is not None:
        sql = """DELETE FROM `group_welcome` WHERE `gid`=%s"""
        args = obj_to_json_str(gid)
        _db.execute(sql, args)
        await matcher.finish('成功删除入群欢迎')
    await matcher.finish('不存在入群欢迎')
