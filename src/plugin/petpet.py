# encoding:utf-8
from os import getcwd

from nonebot import get_bot, on_command
from nonebot.adapters.onebot.v11 import Event
from nonebot.rule import to_me

from .core.PetPet import PetPet
from .utils import get_qavatar, img_cut_circle


petpet = on_command(
    cmd='petpet',
    rule=to_me(),
    aliases={'摸摸'},
    priority=0)

@petpet.handle()
async def petpetHandler(event: Event) -> None:
    bot = get_bot()
    _, group_id, user_id = event.get_session_id().split('_')
    avatar = await get_qavatar(user_id)
    with open('cache/petpet/avatar.gif', 'wb') as f:
        f.write(avatar)
    img_cut_circle(
        'cache/petpet/avatar.gif',
        'cache/petpet/avatar.gif',)
    PetPet.petpet(
        'cache/petpet/avatar.gif',
        'cache/petpet/avatar.gif')
    await bot.call_api(
        'send_group_msg',
        group_id = group_id,
        message = f"[CQ:image,file=file:///{getcwd()}/cache/petpet/avatar.gif]")
