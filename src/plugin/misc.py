"""杂项
"""
from nonebot import get_bot, get_driver, on_command
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.rule import to_me
from .core.data_base import Database
from .utils import json_to_obj

# bot上下线提醒
driver = get_driver()


@driver.on_bot_connect
async def _on_bot_connect() -> None:
    """bot连接成功时
    """
    logger.success('连接成功！高性能です!')
    bot = get_bot()
    await bot.call_api(
        'send_group_msg',
        group_id='645350897',
        message='连接成功！高性能です!')
    _db = Database()  # 尝试建立数据表
    _ = json_to_obj('./data/tables.json')
    for t_name, sql in _.items():
        _db.execute(f"SHOW TABLES LIKE '{t_name}'")
        if _db.fetchone() is None:
            _db.execute(sql)


@driver.on_bot_disconnect
async def _on_bot_disconnect() -> None:
    """bot断开连接时
    """
    logger.error('断开连接...')
    # ... # do sth.


# 输出更新日志
ChangeLog = on_command(
    cmd='ChangeLog',
    rule=to_me(),
    aliases={'更新日志'})


@ChangeLog.handle()
async def _handler(matcher: Matcher) -> None:
    """根据本地README输出更新日志

    参数:
        matcher (Matcher): matcher
    """
    repo = 'https://github.com/TrymenT-AlphA/arknightsbot.git'
    message = '➥' + repo
    with open('README.md', 'r', encoding='utf8') as _:
        for line in reversed(_.readlines()):
            if len(line.strip()) == 0:  # 空行跳过
                continue
            line = line.strip().replace('#', '-')
            message = line + '\n' + message
            if line == '- 更新日志':
                break  # 到头了
    await matcher.finish(message)
