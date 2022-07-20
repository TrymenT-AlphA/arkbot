# encoding:utf-8
"""提供物品数据的更新和查询
"""
import os
import imgkit
import jinja2
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from .core.ark_item import ArkItem
from .utils import json_to_obj


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
    """查询物品数据

    参数:
        matcher (Matcher): Matcher
        args (Message, optional): 参数. Defaults to CommandArg().
    """
    item = ArkItem(name = args.extract_plain_text())
    info = item.get_info()
    if info is None: # 数据库中没有信息,直接返回
        await matcher.finish("数据库中没有物品信息")
    # 找到对应的图片路径
    info['cssPath'] = f"file:///{os.getcwd()}/data/style.css"
    info['pic'] = f"file:///{os.getcwd()}/arksrc/item/{info['iconId']}.png"
    # 计算stage code
    stage_code = json_to_obj('data/stage_code.json')
    for each in info['stageDropList']:
        each['stageCode'] = stage_code[each['stageId']]
    # 根据jinja模板生成图片
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('data/'))
    temp = env.get_template('item_info.jinja') # data/item_info.jinja
    html = temp.render(args = info)
    with open('data/item_info.html', 'w', encoding='utf8') as _:
        _.write(html)
    options = {
        'width': 1020,
        "enable-local-file-access": None
    }
    with open('data/item_info.html', 'r', encoding='utf8') as _:
        imgkit.from_file(_, 'data/item_info.jpg', options=options)
    await matcher.send(MessageSegment.image(f"file:///{os.getcwd()}/data/item_info.jpg"))
    os.remove('data/item_info.html')
    os.remove('data/item_info.jpg')
