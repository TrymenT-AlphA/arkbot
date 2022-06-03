# encoding:utf-8
import os
import sys

from nonebot import on_command, get_bot
from nonebot.rule import to_me
from nonebot.permission import SUPERUSER
from nonebot.matcher import Matcher


reboot = on_command(
    cmd='reboot',
    rule=to_me(),
    aliases={'重启'},
    priority=0,
    permission=SUPERUSER)


@reboot.handle()
async def rebootHandler(matcher: Matcher) -> None:
    """
    重启
    """
    bot = get_bot()
    await bot.call_api(
        'send_group_msg',
        group_id = '645350897',
        message = '重启中...'
    )
    sys.stdout.flush()
    program = sys.executable
    os.execl(program, program, *sys.argv)
