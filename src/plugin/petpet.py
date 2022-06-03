# encoding:utf-8
from nonebot import on_command, get_bot
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Event
from os import getcwd

from .utils import get_qavatar, img_cut_circle
from .core.PetPet import PetPet


petpet = on_command(
    cmd='petpet',
    rule=to_me(),
    aliases={'摸摸', 'rua'},
    priority=0)


@petpet.handle()
async def petpetHandler(event: Event) -> None:
    bot = get_bot()
    _, group_id, user_id = event.get_session_id().split('_')
    avatar = await get_qavatar(user_id)
    with open('data/petpet/avatar.gif', 'wb') as f:
        f.write(avatar)
    img_cut_circle(
        'data/petpet/avatar.gif',
        'data/petpet/avatar.gif',)
    PetPet.petpet(
        'data/petpet/avatar.gif',
        'data/petpet/avatar.gif')
    await bot.call_api(
        'send_group_msg',
        group_id = group_id,
        message = f"[CQ:image,file=file:///{getcwd()}/data/petpet/avatar.gif]")
