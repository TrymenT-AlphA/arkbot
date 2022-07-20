"""机器人首次运行的初始化程序,用于初始化数据库
"""
from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from .core.ark_enemy import ArkEnemy
from .core.ark_item import ArkItem
from .core.ark_range import ArkRange
from .core.ark_op import ArkOp

Initialize = on_command(
    cmd='Initialize',
    rule=to_me(),
    aliases={'初始化'},
    permission=SUPERUSER)


@Initialize.handle()
async def _handler(matcher: Matcher) -> None:
    """初始化数据库

    参数:
        matcher (Matcher): Matcher
    """
    await matcher.send('开始初始化程序...')
    # 各个表的更新
    ArkEnemy().update()
    ArkItem().update()
    ArkRange().update()
    ArkOp().update()
    await matcher.send('初始化完毕!')
