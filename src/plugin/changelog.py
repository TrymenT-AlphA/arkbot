"""输出更新日志
"""
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher

ChangeLog = on_command(
    cmd='ChangeLog',
    rule=to_me(),
    aliases={'更新日志'})


@ChangeLog.handle()
async def _handler(matcher: Matcher) -> None:
    """根据本地README输出更新日志
    """
    repo = 'https://github.com/TrymenT-AlphA/arknightsbot.git'
    msg = '➥' + repo
    with open('README.md', 'r', encoding='utf8') as _:
        for line in reversed(_.readlines()):
            if len(line.strip()) == 0:
                continue
            line = line.strip().replace('#', '-')
            msg = line + '\n' + msg
            if line == '- 更新日志':
                break
    await matcher.finish(msg)
