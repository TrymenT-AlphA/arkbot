# encoding:utf-8
from nonebot import on_message
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Event, MessageSegment


greeting = on_message(
    rule=to_me(),
    priority=1)


@greeting.handle()
async def greetingHandler(matcher: Matcher, event: Event) -> None:
    """
    打招呼etc
    """
    user_id = event.get_user_id()
    message_to_me = event.get_message().extract_plain_text()
    # 打招呼
    greeting_words = ['早上好', '中午好', '晚上好', '早安', '午安', '晚安']
    for word in greeting_words:
        if word in message_to_me:
            await matcher.finish(MessageSegment.at(user_id)+word)
    # 表扬
    praise_words = ['棒', '强', '厉害', '可爱', '喜欢', '爱你']
    for word in praise_words:
        if word in message_to_me:
            await matcher.finish('高性能ですから!')
