# encoding:utf-8
from nonebot import require, get_bot
import bilibili_api.user
import yaml


bilibilidynamic = require('nonebot_plugin_apscheduler').scheduler


@bilibilidynamic.scheduled_job('interval', minutes=1)
async def bilibiliDynamicScheduledJob() -> None:
    """
    定时获取b站动态并推送
    """
    bot = get_bot()
    with open('config/bilibilidynamic.yml', 'rb') as f:
        info = yaml.load(f.read(), Loader=yaml.FullLoader)

    for i in range(len(info['accounts'])):
        uid = info['accounts'][i]['uid']
        recent_dynamic_id = info['accounts'][i]['recent_dynamic_id']
        bilibili_user = bilibili_api.user.User(uid)
        dynamic_info = await bilibili_user.get_dynamics()
        latest_dynamic_id = dynamic_info['cards'][0]['desc']['dynamic_id']
        # 没有新动态，跳过
        if latest_dynamic_id == recent_dynamic_id:
            continue
        # 根据动态信息生成消息
        latest_dynamic_card = dynamic_info['cards'][0]['card']
        message = f"{latest_dynamic_card['user']['name']}有新动态：\n"
        message += latest_dynamic_card['item']['description'] + '\n'
        for pic in latest_dynamic_card['item']['pictures']:
            message += f"[CQ:image,file={pic['img_src']}]\n"
        # 发送消息
        for group_id in info['enabledgroups']:
            await bot.call_api(
                'send_group_msg',
                group_id=group_id,
                message=message)
        # 更新最近动态id
        info['accounts'][i]['recent_dynamic_id'] = latest_dynamic_id
        with open('config/bilibilidynamic.yml', 'w') as f:
            yaml.dump(info, f)
