# encoding:utf-8
"""提供干员数据的更新和查询
"""
import os
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from .core.ark_item import ArkItem
from .core.ark_op import ArkOp
from .core.ark_range import ArkRange
from .utils import bring_in_blackboard, untag, render_jinja

OpUpdate = on_command(
    cmd='OpUpdate',
    rule=to_me(),
    aliases={'更新干员数据'},
    permission=SUPERUSER)


@OpUpdate.handle()
async def _handler(matcher: Matcher) -> None:
    """更新干员数据库

    参数:
        matcher (Matcher): Matcher
    """
    await matcher.send('开始更新干员数据库...')
    await matcher.send(f'更新了{ArkOp.update()}条信息')
    await matcher.send('干员数据库更新完毕!')


OpInfo = on_command(
    cmd='OpInfo',
    rule=to_me(),
    aliases={'查询干员'})


@OpInfo.handle()
async def _handler(matcher: Matcher, args: Message = CommandArg()) -> None:
    """查询干员数据

    参数:
        matcher (Matcher): Matcher
        args (Message, optional): 参数. Defaults to CommandArg().
    """
    args = ArkOp(args.extract_plain_text()).get_info()
    if args is None:
        await matcher.finish("数据库中没有干员信息")
    args['cssPath'] = f"file:///{os.getcwd()}/data/style.css"
    # 根据jinja模板生成图片
    render_jinja(
        root='data',
        template='op_info',
        args=args
    )
    await matcher.send(
        MessageSegment.image(f"file:///{os.getcwd()}/data/op_info.jpg")
    )
    os.remove('data/op_info.jpg')
