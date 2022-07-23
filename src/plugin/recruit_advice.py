"""公开招募
"""
from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Message
from .core.ark_recruit import ArkRecruit

RecruitAdvice = on_command(
    cmd='recruit',
    rule=to_me(),
    aliases={"公开招募"})


@RecruitAdvice.handle()
async def _handler(matcher: Matcher, args: Message = CommandArg()) -> None:
    """如果首次带参就直接设置参数
    """
    if len(args) > 0:
        matcher.set_arg('recruit_args', args)


@RecruitAdvice.got('recruit_args', prompt='请博士发送公招截图')
async def _gotter(state: T_State) -> None:
    """获取公招建议
    """
    recruit_args = state['recruit_args']
    if len(recruit_args) == 0:
        await RecruitAdvice.reject('请博士发送公招截图')
    pic_cnt = 0
    advice = []
    for arg in recruit_args:
        if arg.type == 'image':
            pic_cnt += 1
            advice.append(await ArkRecruit().get_advice(arg.data['url'], 'url'))
    if len(advice) == 1:
        if len(advice[0]) > 0:
            await RecruitAdvice.finish(advice[0][0:-1])
        else:
            await RecruitAdvice.finish('都是垃圾tag呢')
    else:
        message = Message('')
        for i, each in enumerate(advice):
            if i != 0:
                message += Message('\n')
            if len(each) > 0:
                message += Message(f"图{i + 1}公招：\n" + each[0:-1])
            else:
                message += Message(f"图{i + 1}公招：\n" + '都是垃圾tag呢')
        await RecruitAdvice.finish(message)
