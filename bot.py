"""启动机器人的入口程序
"""
import os
import json
import nonebot
from nonebot.adapters.onebot import V11Adapter as ONEBOT_V11ADAPTER

# 初始代码
nonebot.init()
app = nonebot.get_asgi()
driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11ADAPTER)
# 导入的插件
nonebot.load_builtin_plugins("echo")
nonebot.load_from_toml("Pipfile")


def guide():
    """引导程序
    """
    nonebot.logger.info('首次启动机器人，现在开始初次运行的配置')
    config = {
        'database': {},
        'baiduocr': {}
    }
    print('现在开始配置数据库(请提供足够权限的用户以自动创建不存在的数据表)')
    # HOST USER PASSWORD
    for key, default in [('HOST', 'localhost'), ('USER', 'root'), ('PASSWORD', '')]:
        print(f'{key}(默认:{default or "空"}):', end=' ')
        config['database'][key] = input().strip()
        if not len(config['database'][key]):
            config['database'][key] = default
    # DATABASE 非空
    while True:
        print('DATABASE(非空):', end=' ')
        config['database']['DATABASE'] = input().strip()
        if len(config['database']['DATABASE']):
            break
    # 开始配置百度OCR
    print('现在开始配置百度OCR')
    # APP_ID API_KEY SECRET_KEY 均为非空
    for key in ['APP_ID', 'API_KEY', 'SECRET_KEY']:
        while True:
            print(f'{key}(非空):', end=' ')
            config['baiduocr'][key] = input().strip()
            if len(config['baiduocr'][key]):
                break
    with open('config.json', 'w', encoding='utf8') as _:
        json.dump(config, _, ensure_ascii=False)
    print(f"配置文件保存在{os.getcwd()}/config.json,以便随时修改")


if __name__ == "__main__":
    if not os.path.exists('config.json'):
        guide()
    nonebot.run(app="__mp_main__:app")
