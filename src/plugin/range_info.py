# encoding:utf-8
"""提供攻击范围的更新
"""
from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from .core.ark_range import ArkRange


RangeUpdate = on_command(
    cmd='RangeUpdate',
    rule=to_me(),
    aliases={'更新攻击范围数据'},
    permission=SUPERUSER)
@RangeUpdate.handle()
async def _handler(matcher: Matcher) -> None:
    """更新攻击范围数据库

    参数:
        matcher (Matcher): Matcher
    """
    await matcher.send('开始更新攻击范围数据库...')
    await matcher.send(f'更新了{ArkRange.update()}条信息')
    await matcher.send('攻击范围数据库更新完毕!')
