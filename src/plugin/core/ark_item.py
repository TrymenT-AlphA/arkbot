"""明日方舟物品
"""
from typing import Optional
import os
from tqdm import tqdm
from nonebot.log import logger
from .data_base import Database
from ..utils import json_to_obj, obj_to_json_str, json_str_to_obj


class ArkItem:
    """明日方舟物品
    """

    @staticmethod
    def update():
        """更新数据库
        """
        _db = Database()
        update_row = 0
        # 1. 更新 item_table.json
        logger.success('开始更新item_table')
        info = json_to_obj('./arksrc/gamedata/excel/item_table.json')['items']
        for _key, _val in tqdm(info.items()):
            sql = """SELECT `itemId` FROM `item_table` WHERE `itemId`=%s"""
            args = obj_to_json_str(_key)
            _db.execute(sql, args)
            if _db.fetchone() is not None:
                continue
            update_row += 1
            keys, values = zip(*_val.items())
            sql = f"""INSERT INTO `item_table`
                ({','.join([f"`{_}`" for _ in keys])})
                VALUES ({','.join(['%s'] * len(values))})
                """
            args = tuple(map(obj_to_json_str, values))
            _db.execute(sql, args)
        logger.success('item_table更新完毕!')
        return update_row

    def __init__(self, name=None, item_id=None):
        self.name = name
        self.item_id = item_id

    def get_info(self) -> Optional[dict]:
        """获取物品信息
        """
        _db = Database()
        keys = (
            'itemId',
            'name',
            'description',
            'rarity',
            'iconId',
            'overrideBkg',
            'stackIconId',
            'sortId',
            'usage',
            'obtainApproach',
            'classifyType',
            'itemType',
            'stageDropList',
            'buildingProductList'
        )
        if self.name is None and self.item_id is None:
            return None
        if self.name is not None:
            sql = f"""SELECT {','.join([f"`{_}`" for _ in keys[:-1]])} 
                FROM `item_table` WHERE `name`=%s
                """
            args = obj_to_json_str(self.name)
        else:
            sql = f"""SELECT {','.join([f"`{_}`" for _ in keys[:-1]])} 
                FROM `item_table` WHERE `itemId`=%s
                """
            args = obj_to_json_str(self.item_id)
        _db.execute(sql, args)
        res = _db.fetchone()
        if res is None:
            return None
        res = dict(zip(keys, map(json_str_to_obj, res)))
        res['pic'] = f"file:///{os.getcwd()}/arksrc/item/{res['iconId']}.png"
        return res
