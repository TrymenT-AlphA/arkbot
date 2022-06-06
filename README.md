# 部署

## 克隆仓库

> git clone https://github.com/TrymenT-AlphA/arknightsbot.git

## 创建虚拟环境

> pipenv install

## 配置

.env
```
ENVIRONMENT=dev # 或者 ENVIRONMENT=prod
```
.env.dev 示例
```
HOST=127.0.0.1
PORT= # 端口

FASTAPI_RELOAD=true

LOG_LEVEL=DEBUG

SUPERUSERS=[你的超管账号]
NICKNAME=[你的机器人昵称]
COMMAND_START=[命令开始标识符]
COMMAND_SEP=[命令参数分割符]

# 如果用到定时任务需添加以下参数
# APSCHEDULER_AUTOSTART=true
# APSCHEDULER_CONFIG={"apscheduler.timezone": "Asia/Shanghai"}

```

b站动态推送
```
accounts:
- recent_did:
  uid: # 订阅账号的uid
enabledgroups:
- # 启用功能的群聊
```

数据库
```
database:
  host: # 主机ip  
  user: # 用户名
  password: # 密码
  database: # 数据库名称
```

百度OCR
```
baidu-ocr:
  app_name: # 应用名称
  APP_ID: # app_id
  API_KEY: # api_key
  SECRET_KEY: # secret_key
```

入群提醒
```
enabledgroups:
- # 启用功能的群聊
```

## 运行

> pipenv python bot.py

首次运行需进入gocqhttp网页添加账户信息(http://127.0.0.1:port/go-cqhttp/)

# 更新日志

## 2022/6/6

[+] 自动保存群聊图片
## 2022/6/3

[+] 自动摸头

[+] 使用Pipenv虚拟环境
## 2022/6/2

[+] 优化动态推送逻辑
## 2022/6/1

[+] 入群提醒

[+] 简单问候
## 2022/5/31

[+] 更新日志输出

[+] 实现b站动态推送

[+] 实现机器人重启功能

## 2022/5/28

[+] 实现公开招募功能
