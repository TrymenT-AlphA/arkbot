"""明日方舟敌方单位
"""
from typing import Optional
import os
from tqdm import tqdm
from nonebot.log import logger
from .data_base import Database
from ..utils import json_to_obj, obj_to_json_str, json_str_to_obj


class ArkEnemy:
    """明日方舟敌方单位
    """

    @staticmethod
    def update() -> int:
        """更新数据库

        返回值:
            int: 更新的条数
        """
        _db = Database()
        update_row = 0
        # 1. 更新 enemy_handbook_table.json
        logger.success('开始更新enemy_handbook_table')
        info = json_to_obj('arksrc/gamedata/excel/enemy_handbook_table.json')
        for _key, _val in tqdm(info.items()):
            sql = """SELECT `enemyId` FROM `enemy_handbook_table` WHERE `enemyId`=%s"""
            args = obj_to_json_str(_key)
            _db.execute(sql, args)
            if _db.fetchone() is not None:
                continue
            keys, vals = zip(*_val.items())
            sql = f"""INSERT INTO `enemy_handbook_table`
                ({','.join([f"`{_}`" for _ in keys])})
                VALUES ({','.join(['%s'] * len(vals))})
                """
            args = tuple(map(obj_to_json_str, vals))
            _db.execute(sql, args)
            update_row += 1
        logger.success('enemy_handbook_table更新完毕!')
        # 2. 更新 enemy_database.json
        logger.success('开始更新enemy_database')
        info = json_to_obj('arksrc/gamedata/levels/enemydata/enemy_database.json')
        for _val in tqdm(info['enemies']):
            sql = """SELECT `Key` FROM `enemy_database` WHERE `Key`=%s"""
            args = obj_to_json_str(_val['Key'])
            _db.execute(sql, args)
            if _db.fetchone() is not None:
                continue
            keys, vals = zip(*_val.items())
            sql = f"""INSERT INTO `enemy_database`
                ({','.join([f"`{_}`" for _ in keys])})
                VALUES ({','.join(['%s'] * len(vals))})
                """
            args = tuple(map(obj_to_json_str, vals))
            _db.execute(sql, args)
            update_row += 1
        logger.success('enemy_database更新完毕!')
        return update_row

    def __init__(self, name=None):
        self.name = name

    def get_info(self) -> Optional[dict]:
        """获取敌方信息

        返回值:
            dict: 敌方信息
        """
        keys = (
            'enemyId',
            'enemyIndex',
            'name',
            'enemyRace',
            'enemyLevel',
            'attackType',
            'endure',
            'attack',
            'defence',
            'resistance',
            'description',
            'ability',
            'Value'
        )
        _db = Database()
        sql = f"""SELECT {','.join([f"`{key}`" for key in keys[:-1]])}
            FROM `enemy_handbook_table` WHERE `name` LIKE '%{self.name}%'
            """
        _db.execute(sql)
        res = _db.fetchone()
        if res is None:
            return None
        sql = """SELECT `Value` FROM `enemy_database` WHERE `Key`=%s"""
        args = obj_to_json_str(json_str_to_obj(res[0]))  # enemyId
        _db.execute(sql, args)
        res += _db.fetchone()
        res = dict(zip(keys, map(json_str_to_obj, res)))
        res['pic'] = f"file:///{os.getcwd()}/arksrc/enemy/{res['enemyId']}.png"
        return res
