# encoding:utf-8
"""明日方舟敌方单位,提供地方数据的更新查询
"""
from nonebot.log import logger
from tqdm import tqdm
from .data_base import Database
from ..utils import json_to_obj, obj_to_json_str, json_str_to_obj


class ArkEnemy:
    """明日方舟敌方单位,提供敌方数据的更新查询
    """
    @staticmethod
    def update() -> int:
        """根据json文件更新数据库

        返回值:
            int: 更新的条数
        """
        _db = Database()
        # 1. 更新 enemy_handbook_table.json
        logger.success("开始更新enemy_handbook_table")
        enemy_handbook_table = 'arksrc/gamedata/excel/enemy_handbook_table.json'
        info = json_to_obj(enemy_handbook_table)
        update_row = 0
        for _id, _ in tqdm(info.items()):
            sql = """SELECT `enemyId` FROM `enemy_handbook_table`
                WHERE `enemyId`=%s""" # 尝试查询一条数据
            args = obj_to_json_str(_id)
            _db.execute(sql, args)
            if _db.fetchone() is not None:
                continue # 条目已存在,直接跳过
            update_row += 1
            keys, values = zip(*_.items())
            sql = f"""INSERT INTO `enemy_handbook_table`
                ({','.join([f"`{key}`" for key in keys])})
                VALUES ({','.join(['%s']*len(values))})"""
            args = tuple(map(obj_to_json_str, values))
            _db.execute(sql, args)
        logger.success("enemy_handbook_table更新完毕!")
        # 2. 更新 enemy_database.json
        logger.success("开始更新enemy_database")
        enemy_database = 'arksrc/gamedata/levels/enemydata/enemy_database.json'
        info = json_to_obj(enemy_database)
        for _ in tqdm(info['enemies']):
            sql = """SELECT `Key` FROM `enemy_database`
                WHERE `Key`=%s"""
            args = obj_to_json_str(_['Key'])
            _db.execute(sql, args)
            if _db.fetchone() is not None:
                continue # 条目已存在,直接跳过
            update_row += 1
            keys, values = zip(*_.items())
            sql = f"""INSERT INTO `enemy_database`
                ({','.join([f"`{key}`" for key in keys])})
                VALUES ({','.join(['%s']*len(values))})"""
            args = tuple(map(obj_to_json_str, values))
            _db.execute(sql, args)
        logger.success("enemy_database更新完毕!")
        return update_row

    def __init__(self, name=None):
        self.name = name

    def get_info(self) -> dict:
        """获取敌方信息

        Returns:
            dict: 地方信息
        """
        keys = (
            'enemyId','enemyIndex','name','enemyRace','enemyLevel','attackType',
            'endure','attack','defence','resistance','description','ability',
            'Value' # *这个是特殊的
        )
        _db = Database()
        sql = f"""SELECT {','.join([f"`{key}`" for key in keys[:-1]])} FROM `enemy_handbook_table`
            WHERE name LIKE '%{self.name}%'""" # 从enemy_handbook_table查询
        _db.execute(sql)
        res = _db.fetchone()
        if res is None: # 没有查到相关数据
            return None
        sql = """SELECT `Value` FROM `enemy_database`
            WHERE `Key`=%s""" # 从enemy_database查询
        args = obj_to_json_str(json_str_to_obj(res[0])) # enemyId
        _db.execute(sql, args)
        res += _db.fetchone()
        return dict(zip(keys, map(json_str_to_obj, res)))
