# encoding:utf-8
from os import path, mkdir
from datetime import datetime

from nonebot import on_message
from nonebot.adapters.onebot.v11 import Event

from .utils import download_async, load_yaml


async def autopicsaveRule(event: Event) -> bool:
    session_id = event.get_session_id()
    info = load_yaml('config.yml')['autopicsave']
    for group_id in info['GROUPS']:
        if f"group_{group_id}" in session_id:
            return True
    return False

autopicsave = on_message(rule=autopicsaveRule)


@autopicsave.handle()
async def autopicsaveHandler(event: Event) -> None:
    _, group_id, user_id = event.get_session_id().split('_')
    if not path.exists(f"cache/autopicsave/{group_id}"):
        mkdir(f"cache/autopicsave/{group_id}")
    message = event.get_message()
    for message_segment in message:
        if message_segment.type == 'image':
            content = await download_async(url=message_segment.data['url'])
            gif_name = datetime.now().strftime(
                r"[%Y-%m-%d]%Hh%Mm%Ss.%f") + f"@{user_id}.gif"
            with open(f"cache/autopicsave/{group_id}/{gif_name}", 'wb') as gif:
                gif.write(content)
