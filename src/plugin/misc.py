# encoding:utf-8
import os
import sys

from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me


changelog = on_command(
    cmd='changelog',
    rule=to_me(),
    aliases={'更新日志'})

@changelog.handle()
async def changelogHandler(matcher: Matcher) -> None:
    repository = 'https://github.com/TrymenT-AlphA/arknightsbot.git'
    message = f"github:{repository}"
    
    with open('README.md', 'r', encoding='utf8') as f:
        for line in reversed(f.readlines()):
            if len(line.strip()) == 0:
                continue

            line = line.strip().replace('#', '-')
            message = f"{line}\n{message}"
            
            if line == '- 更新日志':
                break

    await matcher.finish(message)


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
