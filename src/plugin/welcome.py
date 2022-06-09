# encoding:utf-8
import yaml
from nonebot import on_notice
from nonebot.adapters.onebot.v11 import (GroupIncreaseNoticeEvent,
                                         MessageSegment)
from nonebot.matcher import Matcher

welcome = on_notice()

@welcome.handle()
async def welcomeHandler(matcher: Matcher, event: GroupIncreaseNoticeEvent):
    _, group_id, user_id = event.get_session_id().split('_')
    with open('config/welcome.yml', 'rb') as f:
        info = yaml.load(f.read(), Loader=yaml.FullLoader)
    
    if group_id in info['enabledgroups']:
        message = MessageSegment.at(user_id) + '欢迎新博士加入研究所的大家庭！\n'
        message += '为了方便博士们交流线索，请先将群昵称改成\'官服|b服 昵称#编号\'的形式哦，\n'
        message += '有什么需要帮忙的事也可以随时找兔兔，兔兔一定会尽力帮助博士的！'
        
        await matcher.finish(message)
