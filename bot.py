# encoding:utf-8

import nonebot
from nonebot.adapters.onebot import V11Adapter as ONEBOT_V11ADAPTER

# You can pass some keyword args config to init function
nonebot.init()

app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11ADAPTER)

# Load plugins
nonebot.load_builtin_plugins("echo")
nonebot.load_from_toml("pyproject.toml")

if __name__ == "__main__":
    nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app="__mp_main__:app")
