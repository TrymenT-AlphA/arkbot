from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.typing import T_State
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message

from .core.Recruit import Recruit


recruit = on_command("recruit", rule=to_me(), aliases={"公开招募"}, priority=0)


@recruit.handle()
async def recruitHandle(matcher: Matcher, args: Message = CommandArg()):
    if len(args) > 0:
        matcher.set_arg('recruit_args', args)


@recruit.got('recruit_args', prompt='请博士发送公招截图')
async def recruitGot(state: T_State):
    recruit_args = state['recruit_args']

    if len(recruit_args) == 0:
        await recruit.reject('请博士发送公招截图')

    recruit_cnt = 0
    advices = []
    for arg in recruit_args:
        if arg.type == 'image':
            recruit_cnt += 1
            advice = await Recruit().select_tags(arg.data['url'])
            advices.append(advice)

    if len(advices) == 1:
        if len(advices[0]) > 0:
            await recruit.finish(advices[0][0:-1])
        else:
            await recruit.finish('都是垃圾tag呢')
    else:
        message = Message('')
        for i in range(len(advices)):
            if i != 0:
                message += Message('\n')
            if len(advices[i]) > 0:
                message += Message(f'图{i+1}公招：\n' + advices[i][0:-1])
            else:
                message += Message(f'图{i+1}公招：\n' + '都是垃圾tag呢')
        await recruit.finish(message)




