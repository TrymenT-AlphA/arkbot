"""提供物品数据的更新和查询
"""
import os
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from .utils import render_jinja
from .core.ark_item import ArkItem

ItemUpdate = on_command(
    cmd='ItemUpdate',
    rule=to_me(),
    aliases={'更新物品数据'},
    permission=SUPERUSER)


@ItemUpdate.handle()
async def _handler(matcher: Matcher) -> None:
    """更新物品数据库
    """
    await matcher.send('开始更新物品数据库...')
    await matcher.send(f'更新了{ArkItem.update()}条信息')
    await matcher.send('物品数据库更新完毕!')


ItemInfo = on_command(
    cmd='ItemInfo',
    rule=to_me(),
    aliases={'查询物品'})


@ItemInfo.handle()
async def _handler(matcher: Matcher, args: Message = CommandArg()) -> None:
    """查询物品
    """
    args = ArkItem(name=args.extract_plain_text()).get_info()
    if args is None:
        await matcher.finish("数据库中没有物品信息")
    args['cssPath'] = f"file:///{os.getcwd()}/data/style.css"
    render_jinja(
        root='data',
        template='item_info',
        args=args
    )
    await matcher.send(
        MessageSegment.image(f"file:///{os.getcwd()}/data/item_info.jpg")
    )
    os.remove('data/item_info.jpg')
