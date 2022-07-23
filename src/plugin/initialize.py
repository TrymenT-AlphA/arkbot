"""机器人首次运行的初始化程序,用于初始化数据库
"""
from nonebot import on_command
from nonebot import get_driver
from nonebot.matcher import Matcher
from nonebot.rule import to_me
from nonebot.permission import SUPERUSER
from nonebot.log import logger
from .utils import json_to_obj
from .core.data_base import MySQL
from .core.ark_enemy import ArkEnemy
from .core.ark_item import ArkItem
from .core.ark_range import ArkRange
from .core.ark_op import ArkOp

driver = get_driver()


@driver.on_bot_connect
async def _on_bot_connect() -> None:
    """bot连接成功时
    """
    logger.success('连接成功！高性能です!')
    _db = MySQL()
    _ = json_to_obj('./data/tables.json')
    for table, sql in _.items():
        _db.execute(f"SHOW TABLES LIKE '{table}'")
        if not _db.fetch_one():
            _db.execute(sql)


@driver.on_bot_disconnect
async def _on_bot_disconnect() -> None:
    """bot断开连接时
    """
    # do sth.


Initialize = on_command(
    cmd='Initialize',
    rule=to_me(),
    aliases={'初始化'},
    permission=SUPERUSER)


@Initialize.handle()
async def _handler(matcher: Matcher) -> None:
    """初始化数据库
    """
    await matcher.send('初始化中...')
    ArkEnemy().update()
    ArkItem().update()
    ArkRange().update()
    ArkOp().update()
    await matcher.send('初始化完毕!')
