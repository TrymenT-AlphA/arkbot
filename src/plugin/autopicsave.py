# encoding:utf-8
import os
from datetime import datetime

from nonebot.plugin import on_message
from nonebot.matcher import Matcher
from nonebot.adapters import Event
from fake_useragent import UserAgent
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
async def autoPicSaveHandler(matcher: Matcher, event: Event) -> None:
    _, group_id, user_id = event.get_session_id().split('_')
    if not os.path.exists(f"data/autopicsave/{group_id}"):
        os.mkdir(f"data/autopicsave/{group_id}")
    message = event.get_message()
    for message_segment in message:
        if message_segment.type == 'image':
            content = await download_async(url = message_segment.data['url'])
            gif_name = datetime.now().strftime(r"[%Y-%m-%d]%Hh%Mm%Ss.%f") + f"@{user_id}.gif"
            with open(f"data/autopicsave/{group_id}/{gif_name}", 'wb') as gif:
                gif.write(content)
