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
from .utils import img_paste, json_to_obj


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
    item = ArkItem(args.extract_plain_text())
    info = item.get_info()
    if info is None: # 数据库中没有信息,直接返回
        await matcher.finish("数据库中没有物品信息")
    # 找到对应的图片路径
    item_pic = f"./arksrc/item/{info['iconId']}.png"
    item_rarity_pic = f"./arksrc/item_rarity_img/sprite_item_r{info['rarity']}.png"
    img_paste(item_pic, item_rarity_pic, f"./{info['iconId']}.png")
    info['pic'] = f"file:///{os.getcwd()}/{info['iconId']}.png"
    # 计算stage code
    stage_code = json_to_obj('./data/stage_code.json')
    for each in info['stageDropList']:
        each['stageCode'] = stage_code[each['stageId']]
    # 根据jinja模板生成图片
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('data/'))
    temp = env.get_template('./item_info.jinja')
    html = temp.render(args = info)
    with open('item_info.html', 'w', encoding='utf8') as _:
        _.write(html)
    options = {
        'width': 600,
        "enable-local-file-access": None
    }
    with open('item_info.html', 'r', encoding='utf8') as _:
        imgkit.from_file(_, 'item_info.jpg', options=options)
    await matcher.send(MessageSegment.image(f"file:///{os.getcwd()}/item_info.jpg"))
    os.remove(f"{info['iconId']}.png")
    os.remove('item_info.html')
    os.remove('item_info.jpg')
