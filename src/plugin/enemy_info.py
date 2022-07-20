# encoding:utf-8
"""提供敌方数据的更新和查询
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
from .core.ark_enemy import ArkEnemy
from .utils import untag


EnemyUpdate = on_command(
    cmd='EnemyUpdate',
    rule=to_me(),
    aliases={'更新敌方数据'},
    permission=SUPERUSER)
@EnemyUpdate.handle()
async def _handler(matcher: Matcher) -> None:
    """更新敌方数据库

    参数:
        matcher (Matcher): Matcher
    """
    await matcher.send('开始更新敌方数据库...')
    await matcher.send(f'更新了{ArkEnemy.update()}条信息')
    await matcher.send('敌方数据库更新完毕!')

EnemyInfo = on_command(
    cmd='EnemyInfo',
    rule=to_me(),
    aliases={'查询敌方'})
@EnemyInfo.handle()
async def _handler(matcher: Matcher, args: Message = CommandArg()) -> None:
    """查询敌方数据

    参数:
        matcher (Matcher): Matcher
        args (Message, optional): 参数. Defaults to CommandArg().
    """
    enemy = ArkEnemy(args.extract_plain_text())
    info = enemy.get_info()
    if info is None: # 数据库中没有信息,直接返回
        await matcher.finish("数据库中没有敌方信息")
    # 找到对应的图片路径
    info['cssPath'] = f"file:///{os.getcwd()}/data/style.css"
    info['pic'] = f"file:///{os.getcwd()}/arksrc/enemy/{info['enemyId']}.png"
    try:
        info['description'] = untag(info['description'])
        info['ability'] = untag(info['ability'])
        info['Value'][0]['enemyData']['description']['m_value'] \
            = untag(info['Value'][0]['enemyData']['description']['m_value'])
    except KeyError:
        ... # 忽略
    # 提取Value中的参数
    for i in range(1, len(info['Value'])):
        level_0 = info['Value'][0]
        level_i = info['Value'][i]
        for _k, _v in level_i['enemyData'].items():
            if _k != 'attributes':
                # 在level_i未定义,在level_0中定义,默认使用level_0的值
                if _v is None and level_0['enemyData'][_k] is not None:
                    level_i['enemyData'][_k] = level_0['enemyData'][_k]
                elif isinstance(_v,dict): # 字典类型的量特殊考虑
                    if not _v['m_defined'] and level_0['enemyData'][_k]['m_defined']:
                        level_i['enemyData'][_k] = level_0['enemyData'][_k]
            else: # _k为'attributes',是个字典
                for _kk, _vv in _v.items():
                    if not _vv['m_defined'] and level_0['enemyData'][_k][_kk]['m_defined']:
                        level_i['enemyData'][_k][_kk] = level_0['enemyData'][_k][_kk]
    # 根据jinja模板生成图片
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('data/'))
    temp = env.get_template('enemy_info.jinja') # data/enemy_info.jinja
    html = temp.render(args = info)
    with open('data/enemy_info.html', 'w', encoding='utf8') as _:
        _.write(html)
    options = {
        'width': 1020,
        "enable-local-file-access": None
    }
    with open('data/enemy_info.html', 'r', encoding='utf8') as _:
        imgkit.from_file(_, 'data/enemy_info.jpg', options=options)
    await matcher.send(MessageSegment.image(f"file:///{os.getcwd()}/data/enemy_info.jpg"))
    os.remove('data/enemy_info.html')
    os.remove('data/enemy_info.jpg')
