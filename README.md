# 部署

## 克隆仓库

> git clone https://github.com/TrymenT-AlphA/arknightsbot.git

## 安装依赖

> pip install -r requirements.txt

## 配置

.env
```
ENVIRONMENT=dev
```
.env.dev
```
HOST=127.0.0.1
PORT= # 端口
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

## 运行

> nb run

# 更新日志

## 2022/5/28
+ 实现公开招募功能
