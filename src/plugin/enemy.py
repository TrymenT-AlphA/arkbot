# encoding:utf-8
import os
import re
from cv2 import log

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
    priority=0,
    permission=SUPERUSER)

@enemyupdate.handle()
async def enemyupdateHandler(matcher: Matcher) -> None:
    await matcher.send('开始更新本地仓库...')
    repo = Repo('./Arknights-Bot-Resource')
    # remote = repo.create_remote(name='Arknights-Bot-Resource', url='git@github.com:yuanyan3060/Arknights-Bot-Resource.git')
    logger.info(repo.git.pull())
    await matcher.send('本地仓库更新完毕！')
    await matcher.send('开始更新敌方数据库...')
    Enemy.update()
    await matcher.send('敌方数据库更新完毕!')


# enemysimplequery = on_command(
#     cmd='enemysimplequery',
#     rule=to_me(),
#     aliases={'查询敌方基本信息'},
#     priority=0)

# @enemysimplequery.handle()
# async def enemysimplequeryHandler(matcher: Matcher, args: Message = CommandArg()) -> None:
#     name = args.extract_plain_text()
#     enemy = Enemy(name)
#     simple_info = enemy.get_simple_info()
#     if simple_info is None:
#         await matcher.finish("数据库中没有敌方信息")

#     tagpattern = re.compile(r'<.*?>')
#     for tag in re.findall(tagpattern, simple_info['description']):
#         simple_info['description'] = simple_info['description'].replace(tag, '')
#     if simple_info['ability'] is not None:
#         for tag in re.findall(tagpattern, simple_info['ability']):
#             simple_info['ability'] = simple_info['ability'].replace(tag, '')
#     with open('data/enemy/simple_info_template.html', 'r', encoding='utf8') as f:
#         html = f.read()

#     pic = f"file:///{os.getcwd()}/Arknights-Bot-Resource/enemy/{simple_info['enemyId']}.png"
#     html = html.replace('{{pic}}', pic)
    
#     params = (
#         'enemyIndex',
#         'name',
#         'enemyRace',
#         'attackType',
#         'endure',
#         'attack',
#         'defence',
#         'resistance',
#         'description',
#         'ability',
#     )
#     for each in params:
#         if simple_info[each] is None:
#             html = html.replace('{{'+each+'}}', ' ')
#         else:
#             html = html.replace('{{'+each+'}}', simple_info[each])

#     with open('cache/enemy/simple_info.html', 'wb') as f:
#         f.write(html.encode('utf8'))

#     options = {
#         'width': 600,
#         "enable-local-file-access": None
#     }
#     with open('cache/enemy/simple_info.html', 'r', encoding='utf8') as f:
#         imgkit.from_file(f, 'cache/enemy/simple_info.jpg', options=options)
#     await matcher.send(MessageSegment.image(f"file:///{os.getcwd()}/cache/enemy/simple_info.jpg"))


enemydetailquery = on_command(
    cmd='enemydetailquery',
    rule=to_me(),
    aliases={'查询敌方'})


@enemydetailquery.handle()
async def enemydetailqueryHandler(matcher: Matcher, args: Message = CommandArg()) -> None:
    name = args.extract_plain_text()
    enemy = Enemy(name)
    detail_info = enemy.get_detail_info()
    if detail_info is None:
        await matcher.finish("数据库中没有敌方信息")

    detail_info['pic'] = f"file:///{os.getcwd()}/Arknights-Bot-Resource/enemy/{detail_info['enemyId']}.png"
    tagpattern = re.compile(r'<.*?>')
    for tag in re.findall(tagpattern, detail_info['description']):
        detail_info['description'] = detail_info['description'].replace(tag, '')
    if detail_info['ability'] is not None:
        for tag in re.findall(tagpattern, detail_info['ability']):
            detail_info['ability'] = detail_info['ability'].replace(tag, '')
    for tag in re.findall(tagpattern, detail_info['Value'][0]['enemyData']['description']['m_value']):
            detail_info['Value'][0]['enemyData']['description']['m_value'] = detail_info['Value'][0]['enemyData']['description']['m_value'].replace(tag, '')

    for i in range(1, len(detail_info['Value'])):
        for k, v in detail_info['Value'][i]['enemyData'].items():
            if k != 'attributes':
                if v is None and detail_info['Value'][0]['enemyData'][k] is not None:
                    detail_info['Value'][i]['enemyData'][k] = detail_info['Value'][0]['enemyData'][k]
                elif type(v) == dict and not v['m_defined'] and detail_info['Value'][0]['enemyData'][k]['m_defined']:
                    detail_info['Value'][i]['enemyData'][k] = detail_info['Value'][0]['enemyData'][k]
            else:
                for ak, av in v.items():
                    if not av['m_defined'] and detail_info['Value'][0]['enemyData'][k][ak]['m_defined']:
                        detail_info['Value'][i]['enemyData'][k][ak] = detail_info['Value'][0]['enemyData'][k][ak] 

    environment = jinja2.Environment(loader=jinja2.FileSystemLoader('data/enemy/'))
    template = environment.get_template('./enemy_info.jinja')
    html = template.render(args = detail_info)
    with open('cache/enemy/enemy_info.html', 'wb') as f:
        f.write(html.encode('utf8'))
    options = {
        'width': 820,
        "enable-local-file-access": None
    }
    with open('cache/enemy/enemy_info.html', 'r', encoding='utf8') as f:
        imgkit.from_file(f, 'cache/enemy/enemy_info.jpg', options=options)
    await matcher.send(MessageSegment.image(f"file:///{os.getcwd()}/cache/enemy/enemy_info.jpg"))
