# encoding:utf-8
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher


changelog = on_command(
    cmd='changelog',
    rule=to_me(),
    aliases={'更新日志'},
    priority=0)


@changelog.handle()
async def changelogHandler(matcher: Matcher) -> None:
    """
    输出更新日志
    """
    repository = 'https://github.com/TrymenT-AlphA/arknightsbot.git'
    message = f"github:{repository}"
    with open('README.md', 'r', encoding='utf8') as f:
        for line in reversed(f.readlines()):
            # 空行跳过
            if len(line.strip()) == 0:
                continue

            line = line.strip().replace('#', '-')
            message = f"{line}\n{message}"
            if line == '- 更新日志':
                break
    await matcher.send(message)
