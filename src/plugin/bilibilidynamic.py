from nonebot import require, get_bot
from bilibili_api.user import User
import yaml


bilibilidynamic = require('nonebot_plugin_apscheduler').scheduler

@bilibilidynamic.scheduled_job('interval', minutes=1)
async def bilibiliDynamicScheduledJob() -> None:
    bot = get_bot()

    with open('config/bilibilidynamic.yml', 'rb') as f:
        info = yaml.load(f.read(), Loader=yaml.FullLoader)

    for i in range(len(info['accounts'])):
        uid, recent_dynamic_id = info['accounts'][i]['uid'], info['accounts'][i]['recent_dynamic_id']
        user = User(uid)
        dynamic_info = await user.get_dynamics()
        latest_dynamic_id = dynamic_info['cards'][0]['desc']['dynamic_id']

        if latest_dynamic_id != recent_dynamic_id:
            card = dynamic_info['cards'][0]['card']
            message = f"{card['user']['name']}有新动态：\n"
            message += card['item']['description'] + '\n'
            for pic in card['item']['pictures']:
                message += '[CQ:image,file=' + pic['img_src'] + ']\n'

            for group_id in info['enabledgroups']:
                await bot.call_api('send_group_msg', group_id=group_id, message=message)
            
            info['accounts'][i]['recent_dynamic_id'] = latest_dynamic_id
            with open('config/bilibilidynamic.yml', 'w') as f:
                yaml.dump(info, f)
