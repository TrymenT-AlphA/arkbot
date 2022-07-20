# encoding:utf-8
"""
启动机器人的入口程序
"""
import os
import yaml
import nonebot
from nonebot.adapters.onebot import V11Adapter as ONEBOT_V11ADAPTER

# 初始代码
nonebot.init()
app = nonebot.get_asgi()
driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11ADAPTER)
# 导入的插件
nonebot.load_builtin_plugins("echo")  # 内置插件
nonebot.load_from_toml("Pipfile")  # bot运行元信息，集成在Pipfile中


# 下面是我的函数,通过测试,没有问题
def guide():
    """引导程序,完成机器人基本设置
    """
    nonebot.logger.info('第一次启动机器人，现在开始初次运行的配置')
    config = {
        'database': {},  # 数据库配置
        'baiduocr': {}  # 文字识别配置
    }  # 用于保存配置信息
    # 开始配置数据库
    print('现在开始配置数据库设置,请提供足够权限的用户以自动创建不存在的数据表')
    # HOST USER PASSWORD
    for key, default in [('HOST', 'localhost'), ('USER', 'root'), ('PASSWORD', '')]:
        print(f'{key}(默认:{default or "空"}):', end=' ')
        config['database'][key] = input()
        if len(config['database'][key]) == 0:
            config['database'][key] = default
    # DATABASE 非空
    while True:
        print('DATABASE(非空):', end=' ')
        config['database']['DATABASE'] = input()
        if len(config['database']['DATABASE']):
            break
    # 开始配置百度OCR
    print('现在开始配置百度OCR设置')
    # APP_ID API_KEY SECRET_KEY 均为非空
    for key in ['APP_ID', 'API_KEY', 'SECRET_KEY']:
        while True:
            print(f'{key}(非空):', end=' ')
            config['baiduocr'][key] = input()
            if len(config['baiduocr'][key]):
                break
    # 写入文件
    with open('config.yml', 'w', encoding='utf8') as _:
        yaml.dump(config, _, allow_unicode=True)
    print(f"配置文件保存在{os.getcwd()}/config.yml,以便随时修改")


if __name__ == "__main__":
    if not os.path.exists('./config.yml'):  # 启动时不存在配置文件,尝试进入引导程序
        guide()
    # 配置完毕后运行机器人
    nonebot.run(app="__mp_main__:app")
