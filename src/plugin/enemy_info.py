"""提供敌方数据的更新和查询
"""
import os
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from .core.ark_enemy import ArkEnemy
from .utils import untag, render_jinja

EnemyUpdate = on_command(
    cmd='EnemyUpdate',
    rule=to_me(),
    aliases={'更新敌方数据'},
    permission=SUPERUSER)


@EnemyUpdate.handle()
async def _handler(matcher: Matcher) -> None:
    """更新敌方数据库
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
    """查询敌方
    """
    args = ArkEnemy(args.extract_plain_text()).get_info()
    if args is None:
        await matcher.finish("数据库中没有敌方信息")
    args['cssPath'] = f"file:///{os.getcwd()}/data/style.css"
    # 数据预处理
    try:
        args['description'] = untag(args['description'])
        args['ability'] = untag(args['ability'])
        args['Value'][0]['enemyData']['description']['m_value'] = untag(
            args['Value'][0]['enemyData']['description']['m_value']
        )
    except KeyError:
        ...  # 忽略
    # 提取Value中的参数
    for i in range(1, len(args['Value'])):
        level_0 = args['Value'][0]
        level_i = args['Value'][i]
        for _k, _v in level_i['enemyData'].items():
            if _k != 'attributes':
                if _v is None and level_0['enemyData'][_k] is not None:
                    level_i['enemyData'][_k] = level_0['enemyData'][_k]
                elif isinstance(_v, dict):
                    if not _v['m_defined'] and level_0['enemyData'][_k]['m_defined']:
                        level_i['enemyData'][_k] = level_0['enemyData'][_k]
            else:
                for _kk, _vv in _v.items():
                    if not _vv['m_defined'] and level_0['enemyData'][_k][_kk]['m_defined']:
                        level_i['enemyData'][_k][_kk] = level_0['enemyData'][_k][_kk]
    # 根据jinja模板生成图片
    render_jinja('enemy_info', args=args)
    await matcher.send(MessageSegment.image(f"file:///{os.getcwd()}/data/enemy_info.jpg"))
    os.remove('data/enemy_info.jpg')
