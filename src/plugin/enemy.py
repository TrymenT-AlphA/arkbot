# encoding:utf-8
import os
import re
from tkinter import E

import imgkit
import jinja2
from git.repo import Repo
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from nonebot.log import logger

from .core.Enemy import Enemy


enemyupdate = on_command(
    cmd='enemyupdate',
    rule=to_me(),
    aliases={'更新敌方数据'},
    permission=SUPERUSER)

@enemyupdate.handle()
async def enemyupdateHandler(matcher: Matcher) -> None:
    await matcher.send('开始更新本地仓库...')
    repo = Repo('./Arknights-Bot-Resource')
    logger.info(repo.git.pull())
    await matcher.send('本地仓库更新完毕！')
    await matcher.send('开始更新敌方数据库...')
    await matcher.send(f'更新了{Enemy.update()}条信息')
    await matcher.send('敌方数据库更新完毕!')


enemyquery = on_command(
    cmd='enemydetailquery',
    rule=to_me(),
    aliases={'查询敌方'})

@enemyquery.handle()
async def enemyqueryHandler(matcher: Matcher, args: Message = CommandArg()) -> None:
    name = args.extract_plain_text()
    enemy = Enemy(name)
    info = enemy.get_detail_info()
    if info is None:
        await matcher.finish("数据库中没有敌方信息")

    info['pic'] = f"file:///{os.getcwd()}/Arknights-Bot-Resource/enemy/{info['enemyId']}.png"
    
    def untag(string: str) -> str:
        tagpattern = re.compile(r'<.*?>')
        for tag in re.findall(tagpattern, string):
            string = string.replace(tag, '')
        return string

    try:
        info['description'] = untag(info['description'])
    except:
        pass
    try:
        info['ability'] = untag(info['ability'])
    except:
        pass
    try:
        info['Value'][0]['enemyData']['description']['m_value'] = untag(info['Value'][0]['enemyData']['description']['m_value'])
    except:
        pass

    for i in range(1, len(info['Value'])):
        for k, v in info['Value'][i]['enemyData'].items():
            if k != 'attributes':
                if v is None and info['Value'][0]['enemyData'][k] is not None:
                    info['Value'][i]['enemyData'][k] = info['Value'][0]['enemyData'][k]
                elif type(v) == dict and not v['m_defined'] and info['Value'][0]['enemyData'][k]['m_defined']:
                    info['Value'][i]['enemyData'][k] = info['Value'][0]['enemyData'][k]
            else:
                for ak, av in v.items():
                    if not av['m_defined'] and info['Value'][0]['enemyData'][k][ak]['m_defined']:
                        info['Value'][i]['enemyData'][k][ak] = info['Value'][0]['enemyData'][k][ak] 

    environment = jinja2.Environment(loader=jinja2.FileSystemLoader('data/'))
    template = environment.get_template('./enemy_info.jinja')
    html = template.render(args = info)
    with open('enemy_info.html', 'wb') as f:
        f.write(html.encode('utf8'))
    options = {
        'width': 820,
        "enable-local-file-access": None
    }
    with open('enemy_info.html', 'r', encoding='utf8') as f:
        imgkit.from_file(f, 'enemy_info.jpg', options=options)
    await matcher.send(MessageSegment.image(f"file:///{os.getcwd()}/enemy_info.jpg"))
    os.remove('enemy_info.html')
    os.remove('enemy_info.jpg')
