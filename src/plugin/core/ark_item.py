# encoding:utf-8
"""明日方舟物品
"""
import os
from nonebot.log import logger
from tqdm import tqdm
from .data_base import Database
from ..utils import json_to_obj, obj_to_json_str, json_str_to_obj


class ArkItem:
    """明日方舟物品
    """
    @staticmethod
    def update():
        """更新物品数据库
        """
        _db = Database()
        # 1. 更新 item_table.json
        logger.success("开始更新item_table")
        item_table = "./arksrc./gamedata/excel/item_table.json"
        info = json_to_obj(item_table)['items']
        update_row = 0
        for _id, _ in tqdm(info.items()):
            sql = """SELECT `itemId` FROM `item_table`
                WHERE `itemId`=%s""" # 尝试查询一条数据
            args = obj_to_json_str(_id)
            _db.execute(sql, args)
            if _db.fetchone() is not None:
                continue # 条目已存在,直接跳过
            update_row += 1
            keys, values = zip(*_.items())
            sql = f"""INSERT INTO `item_table`
                ({','.join([f"`{key}`" for key in keys])})
                VALUES ({','.join(['%s']*len(values))})"""
            args = tuple(map(obj_to_json_str, values))
            _db.execute(sql, args)
        logger.success("item_table更新完毕!")
        return update_row

    def __init__(self, name=None, item_id=None):
        self.name = name
        self.item_id = item_id

    def get_info(self):
        """获取物品信息
        """
        _db = Database()
        keys = (
            'itemId','name','description','rarity','iconId','overrideBkg',
            'stackIconId','sortId','usage','obtainApproach','classifyType',
            'itemType', 'stageDropList', 'buildingProductList'
        )
        if self.name is not None:
            sql = f"""SELECT {','.join([f"`{key}`" for key in keys[:-1]])} FROM `item_table`
                WHERE `name`=%s"""
            args = obj_to_json_str(self.name)
        elif self.item_id is not None:
            sql = f"""SELECT {','.join([f"`{key}`" for key in keys[:-1]])} FROM `item_table`
                WHERE `itemId`=%s"""
            args = obj_to_json_str(self.item_id)
        _db.execute(sql, args)
        res = _db.fetchone()
        if res is None: # 没有查到相关数据
            return None
        res = dict(zip(keys, map(json_str_to_obj, res)))
        res['pic'] = f"file:///{os.getcwd()}/arksrc/item/{res['iconId']}.png"
        return res
