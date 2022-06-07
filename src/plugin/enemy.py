# encoding:utf-8
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER

from .core.Enemy import Enemy


enemyupdate = on_command(
    cmd='enemyupdate',
    rule=to_me(),
    aliases={'更新敌方数据'},
    priority=0,
    permission=SUPERUSER)


@enemyupdate.handle()
async def enemyHandler(matcher: Matcher) -> None:
    await matcher.send('开始更新...')
    Enemy.update()
    await matcher.send('更新完毕!')
