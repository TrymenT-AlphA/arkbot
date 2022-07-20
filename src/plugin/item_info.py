"""提供物品数据的更新和查询
"""
import os
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from .core.ark_item import ArkItem
from .utils import json_to_obj, render_jinja

ItemUpdate = on_command(
    cmd='ItemUpdate',
    rule=to_me(),
    aliases={'更新物品数据'},
    permission=SUPERUSER)


@ItemUpdate.handle()
async def _handler(matcher: Matcher) -> None:
    """更新物品数据库

    参数:
        matcher (Matcher): Matcher
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
    # 计算stage code
    stage_code = json_to_obj('data/stage_code.json')
    for each in args['stageDropList']:
        each['stageCode'] = stage_code[each['stageId']]
    # 根据jinja模板生成图片
    render_jinja('item_info', args=args)
    await matcher.send(MessageSegment.image(f"file:///{os.getcwd()}/data/item_info.jpg"))
    os.remove('data/item_info.jpg')
