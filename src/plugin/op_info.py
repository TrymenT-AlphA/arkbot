# encoding:utf-8
"""提供干员数据的更新和查询
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
from .core.ark_op import ArkOp
from .core.ark_range import ArkRange
from .utils import bring_in_blackboard, untag


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
    _op = ArkOp(args.extract_plain_text())
    info = _op.get_info()
    if info is None: # 数据库中没有信息,直接返回
        await matcher.finish("数据库中没有干员信息")
    # 找到对应的图片路径
    info['pic'] = \
        f"file:///{os.getcwd()}/arksrc/avatar/{info['phases'][0]['characterPrefabKey']}.png"
    try:
        info['description'] = untag(info['description']).replace('\\n', '</br>')
    except KeyError:
        ... # 忽略
    # 处理tagList
    if info['tagList'] is not None:
        info['tagList'] = ','.join(info['tagList'])
    # 处理职业信息，pass
    # 处理攻击范围信息
    for i, _ in enumerate(info['phases']):
        info['phases'][i]['range'] = ArkRange(_['rangeId']).get_html()
    # 处理天赋信息
    try:
        for i, _i in enumerate(info['talents']):
            for j, _j in enumerate(_i['candidates']):
                info['talents'][i]['candidates'][j]['description'] = \
                    bring_in_blackboard(info['talents'][i]['candidates'][j]).replace('\\n', '</br>')
    except TypeError:
        ...
    # 处理技能信息
    for i, _i in enumerate(info['skills']):
        if _i['skillInfo']['iconId'] is None:
            info['skills'][i]['skillPic'] = \
                f"file:///{os.getcwd()}/arksrc/skill/skill_icon_{_i['skillId']}.png"
        else:
            info['skills'][i]['skillPic'] = \
                f"file:///{os.getcwd()}/arksrc/skill/skill_icon_{_i['skillInfo']['iconId']}.png"
        for j, _j in enumerate(_i['skillInfo']['levels']):
            info['skills'][i]['skillInfo']['levels'][j]['description'] = \
                bring_in_blackboard(_i['skillInfo']['levels'][j]).replace('\\n', '</br>')
            if _i['skillInfo']['levels'][j]['rangeId'] is not None:
                info['skills'][i]['skillInfo']['levels'][j]['range'] = \
                    ArkRange(_i['skillInfo']['levels'][j]['rangeId']).get_html()
    # 处理精英化材料信息
    for i, _i in enumerate(info['phases']):
        if _i['evolveCost'] is not None:
            for j, _j in enumerate(_i['evolveCost']):
                info['phases'][i]['evolveCost'][j]['pic'] = \
                    ArkItem(item_id=_j['id']).get_info()['pic']
    # 处理技能升级表
    try:
        for i, _i in enumerate(info['allSkillLvlup']):
            for j, _j in enumerate(_i['lvlUpCost']):
                info['allSkillLvlup'][i]['lvlUpCost'][j]['pic'] = \
                    ArkItem(item_id=_j['id']).get_info()['pic']
    except TypeError:
        ...
    # 处理技能专精表
    try:
        for i, _i in enumerate(info['skills']):
            for j, _j in enumerate(_i['levelUpCostCond']):
                for k, _k in enumerate(_j['levelUpCost']):
                    info['skills'][i]['levelUpCostCond'][j]['levelUpCost'][k]['pic'] = \
                        ArkItem(item_id=_k['id']).get_info()['pic']
    except TypeError:
        ...
    # obj_to_json(info, 'temp.json')
    # 根据jinja模板生成图片
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('data/'))
    temp = env.get_template('./op_info.jinja')
    html = temp.render(args = info)
    with open('op_info.html', 'w', encoding='utf8') as _:
        _.write(html)
    options = {
        'width': 1020,
        "enable-local-file-access": None
    }
    with open('op_info.html', 'r', encoding='utf8') as _:
        imgkit.from_file(_, 'op_info.jpg', options=options)
    await matcher.send(MessageSegment.image(f"file:///{os.getcwd()}/op_info.jpg"))
    os.remove('op_info.html')
    os.remove('op_info.jpg')
