# encoding:utf-8
import os
from datetime import datetime

from nonebot.plugin import on_message
from nonebot.matcher import Matcher
from nonebot.adapters import Event
import yaml

from .utils import download_async


async def autoPicSaveRule(event: Event) -> bool:
    session_id = event.get_session_id()
    with open('config/autopicsave.yml', 'rb') as f:
        info = yaml.load(f.read(), Loader=yaml.FullLoader)
    for group_id in info['enabledgroups']:
        if f"group_{group_id}" in session_id:
            return True
    return False


AutoPicSave = on_message(rule=autoPicSaveRule)


@AutoPicSave.handle()
async def handleAutoPicSave(matcher: Matcher, event: Event) -> None:
    _, group_id, user_id = event.get_session_id().split('_')
    message = event.get_message()
    if message[0].type == 'image':
        content = await download_async(message[0].data['url'])
        if not os.path.exists(f"data/autopicsave/{group_id}"):
            os.mkdir(f"data/autopicsave/{group_id}")
        with open(f"data/autopicsave/{group_id}/{int(datetime.now().timestamp())}-{user_id}.gif", 'wb') as gif:
            gif.write(content)
