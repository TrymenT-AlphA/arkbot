# encoding:utf-8
import os
import sys

from nonebot import get_bot, get_driver, on_command
from nonebot.adapters import Bot
from nonebot.drivers import Driver
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me


# bot上下线提醒
driver: Driver = get_driver()

@driver.on_bot_connect
async def onBotConnect():
    bot: Bot = get_bot()
    await bot.call_api(
        'send_group_msg',
        group_id = '645350897',
        message = '连接成功！高性能です!'
    )

@driver.on_bot_disconnect
async def onBotDisconnect():
    logger.error('失联中...')


# 输出更新日志
changelog = on_command(
    cmd='changelog',
    rule=to_me(),
    aliases={'更新日志'})

@changelog.handle()
async def changelogHandler(matcher: Matcher) -> None:
    repo = 'https://github.com/TrymenT-AlphA/arknightsbot.git'
    message = f"github:{repo}"
    with open('README.md', 'r', encoding='utf8') as f:
        for line in reversed(f.readlines()):
            if len(line.strip()) == 0: # enmty
                continue
            line = line.strip().replace('#', '-')
            message = line+'\n'+message
            if line == '- 更新日志':
                break
    await matcher.finish(message)


# 重启bot
reboot = on_command(
    cmd='reboot',
    rule=to_me(),
    aliases={'重启'},
    permission=SUPERUSER)

@reboot.handle()
async def rebootHandler(matcher: Matcher) -> None:
    await matcher.send('重启中...')
    sys.stdout.flush()
    program = sys.executable
    os.execl(program, program, *sys.argv)
