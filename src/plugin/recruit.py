# encoding:utf-8
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.rule import to_me
from nonebot.typing import T_State

from .core.Recruit import Recruit


recruit = on_command(
    cmd='recruit',
    rule=to_me(),
    aliases={"公开招募"})

@recruit.handle()
async def recruitHandler(matcher: Matcher,
                         args: Message = CommandArg()) -> None:
    if len(args) > 0:
        matcher.set_arg('recruit_args', args)

@recruit.got('recruit_args', prompt='请博士发送公招截图')
async def recruitGotter(state: T_State) -> None:
    recruit_args = state['recruit_args']
    if len(recruit_args) == 0:
        await recruit.reject('请博士发送公招截图')

    pic_cnt = 0
    advice = []
    for arg in recruit_args:
        if arg.type == 'image':
            pic_cnt += 1
            advice.append(await Recruit().get_advice(arg.data['url'], 'url'))

    if len(advice) == 1:
        if len(advice[0]) > 0:
            await recruit.finish(advice[0][0:-1])
        else:
            await recruit.finish('都是垃圾tag呢')
    else:
        message = Message('')
        for i in range(len(advice)):
            if i != 0:
                message += Message('\n')
            if len(advice[i]) > 0:
                message += Message(f"图{i+1}公招：\n" + advice[i][0:-1])
            else:
                message += Message(f"图{i+1}公招：\n" + '都是垃圾tag呢')
        await recruit.finish(message)
