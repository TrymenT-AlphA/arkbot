"""敌方数据的更新和查询
"""
import os
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message
from nonebot.adapters.onebot.v11 import MessageSegment
from .core.ark_enemy import ArkEnemy
from .utils import render_jinja


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
    if not args:
        await matcher.finish("数据库中没有敌方信息")
    args['cssPath'] = f"file:///{os.getcwd()}/data/style.css"
    render_jinja(
        root='data',
        template='enemy_info',
        args=args
    )
    await matcher.send(
        MessageSegment.image(f"file:///{os.getcwd()}/data/enemy_info.jpg")
    )
    os.remove('data/enemy_info.jpg')
