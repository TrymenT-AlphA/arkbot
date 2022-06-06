# encoding:utf-8
import nonebot
from nonebot.adapters.onebot import V11Adapter as ONEBOT_V11ADAPTER

# You can pass some keyword args config to init function
nonebot.init()
# get app
app = nonebot.get_asgi()
# get driver
driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11ADAPTER)

# Load plugins
nonebot.load_builtin_plugins("echo")
nonebot.load_from_toml("Pipfile")


@driver.on_bot_connect
async def onBotConnect():
    bot = nonebot.get_bot()
    await bot.call_api(
        'send_group_msg',
        group_id = '645350897',
        message = '连接成功！高性能ですから!'
    )


@driver.on_bot_disconnect
async def onBotDisconnect():
    print('失联中...')


if __name__ == "__main__":
    nonebot.logger.warning(
        "Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app="__mp_main__:app")
