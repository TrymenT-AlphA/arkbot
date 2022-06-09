# encoding:utf-8
import bilibili_api.user
import yaml
from nonebot import get_bot, require


bilibilidynamic = require('nonebot_plugin_apscheduler').scheduler

@bilibilidynamic.scheduled_job('interval', minutes=5)
async def bilibiliDynamicScheduledJob() -> None:
    bot = get_bot()
    with open('config/bilibilidynamic.yml', 'rb') as f:
        info = yaml.load(f.read(), Loader=yaml.FullLoader)
    for i, account in enumerate(info['accounts']):
        # 读取当前用户信息
        uid = account['uid']
        recent_did = account['recent_did']
        # 获取最新动态
        user = bilibili_api.user.User(uid)
        latest_dynamic = (await user.get_dynamics())['cards'][0]
        latest_did = latest_dynamic['desc']['dynamic_id']
        # 没有动态更新
        if recent_did == latest_did:
            continue
        messages = []
        # 文字+图片动态
        if latest_dynamic['desc']['type'] == 2:
            # 文字信息忽略
            messages.append(latest_dynamic['card']['item']['description'])
            for picture in latest_dynamic['card']['item']['pictures']:
                messages.append(f"[CQ:image,file={picture['img_src']}]")
        # 视频动态
        elif latest_dynamic['desc']['type'] == 8:
            # 文字信息忽略
            messages.append(latest_dynamic['card']['dynamic'])
            messages.append(
                latest_dynamic['card']['title']
                +f"\n[CQ:image,file={latest_dynamic['card']['pic']}]"
                +f"\n➥{latest_dynamic['card']['short_link']}")
        # 发送消息
        for group_id in info['enabledgroups']:
            for message in messages:
                await bot.call_api(
                    'send_group_msg',
                    group_id=group_id,
                    message=message)
        # 更新最近动态id
        info['accounts'][i]['recent_did'] = latest_did
        with open('config/bilibilidynamic.yml', 'w') as f:
            yaml.dump(info, f)
