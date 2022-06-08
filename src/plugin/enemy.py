# encoding:utf-8
from click import option
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Message, MessageSegment
import os, re
import imgkit

from .core.Enemy import Enemy


enemyupdate = on_command(
    cmd='enemyupdate',
    rule=to_me(),
    aliases={'更新敌方数据'},
    priority=0,
    permission=SUPERUSER)


@enemyupdate.handle()
async def enemyupdateHandler(matcher: Matcher) -> None:
    await matcher.send('开始更新敌方数据...')
    Enemy.update()
    await matcher.send('敌方数据更新完毕!')


enemysimplequery = on_command(
    cmd='enemysimplequery',
    rule=to_me(),
    aliases={'查询敌方'},
    priority=0)


@enemysimplequery.handle()
async def enemysimplequeryHandler(matcher: Matcher, args: Message = CommandArg()) -> None:
    name = args.extract_plain_text()
    enemy = Enemy(name)
    simple_info = enemy.get_simple_info()
    if simple_info is None:
        await matcher.finish("数据库中没有敌方信息")

    tagpattern = re.compile(r'<.*?>')
    for tag in re.findall(tagpattern, simple_info['description']):
        simple_info['description'] = simple_info['description'].replace(tag, '')
    if simple_info['ability'] is not None:
        for tag in re.findall(tagpattern, simple_info['ability']):
            simple_info['ability'] = simple_info['ability'].replace(tag, '')
    with open('data/enemy/simple_info_template.html', 'r', encoding='utf8') as f:
        html = f.read()

    pic = f"file:///{os.getcwd()}/Arknights-Bot-Resource/enemy/{simple_info['enemyId']}.png"
    html = html.replace('{{pic}}', pic)
    
    params = (
        'enemyIndex',
        'name',
        'enemyRace',
        'attackType',
        'endure',
        'attack',
        'defence',
        'resistance',
        'description',
        'ability',
    )
    for each in params:
        if simple_info[each] is None:
            html = html.replace('{{'+each+'}}', '')
        else:
            html = html.replace('{{'+each+'}}', simple_info[each])

    with open('data/enemy/simple_info.html', 'wb') as f:
        f.write(html.encode('utf8'))

    options = {
        'width': 600,
        "enable-local-file-access": None
    }
    with open('data/enemy/simple_info.html', 'r', encoding='utf8') as f:
        imgkit.from_file(f, 'data/enemy/simple_info.jpg', options=options)
    await matcher.send(MessageSegment.image(f"file:///{os.getcwd()}/data/enemy/simple_info.jpg"))
