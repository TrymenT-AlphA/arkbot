"""明日方舟物品
"""
from typing import Optional
import os
from tqdm import tqdm
from nonebot.log import logger
from .data_base import MySQL
from ..utils import json_to_obj


class ArkItem:
    """明日方舟物品
    """
    occ_per_dict = {
        'ALWAYS': '固定掉落',
        'ALMOST': '大概率',
        'USUAL': '概率掉落',
        'OFTEN': '小概率',
        'SOMETIMES': '罕见'
    }

    @staticmethod
    def update():
        """更新数据库
        """
        _db = MySQL()
        update_row = 0

        # 更新 item_table.json
        logger.success('开始更新item_table')
        info = json_to_obj('./arksrc/gamedata/excel/item_table.json')['items']
        for _key, _val in tqdm(info.items()):
            if _db.select_one(
                    table='item_table',
                    keys=('itemId',),
                    condition='`itemId`=%s',
                    args=(_key,)
            ):
                continue
            keys, vals = zip(*_val.items())
            _db.insert('item_table', keys, vals)
            update_row += 1
        logger.success('item_table更新完毕!')
        return update_row

    def __init__(self, name=None, item_id=None):
        self.name = name
        self.item_id = item_id

    def get_info(self) -> Optional[dict]:
        """获取物品信息
        """
        _db = MySQL()
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
        if not self.name and not self.item_id:
            return
        if self.name:
            res = _db.select_one(
                table='item_table',
                keys=keys,
                condition='`name`=%s',
                args=(self.name,)
            )
        elif self.item_id:
            res = _db.select_one(
                table='item_table',
                keys=keys,
                condition='`itemId`=%s',
                args=(self.item_id,)
            )
        else:
            res = None
        res['pic'] = f"file:///{os.getcwd()}/arksrc/item/{res['iconId']}.png"
        # 计算stage code
        stage_code_dict = json_to_obj('data/stage_code.json')
        for _ in res['stageDropList']:
            _['stageCode'] = stage_code_dict[_['stageId']]
        # 计算occ_per
        for _ in res['stageDropList']:
            _['occPer'] = self.occ_per_dict[_['occPer']]
        return res
