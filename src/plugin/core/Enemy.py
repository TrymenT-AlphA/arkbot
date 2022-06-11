# encoding:utf-8
from nonebot.log import logger
from tqdm import tqdm

from ..utils import dumps_json, load_json, loads_json
from .Database import Database


class Enemy:

    @classmethod
    def update(cls) -> int:
        db = Database()
        enemy_handbook_table = 'Arknights-Bot-Resource/gamedata/excel/enemy_handbook_table.json'
        enemy_database = 'Arknights-Bot-Resource/gamedata/levels/enemydata/enemy_database.json'
        # 更新 enemy_handbook_table.json
        info = load_json(enemy_handbook_table)
        logger.info("开始更新enemy_handbook_table")
        cnt = 0
        for enemyId, value in tqdm(info.items()):
            db.execute(
                "SELECT enemyId FROM enemy_handbook_table WHERE enemyId=%s", dumps_json(enemyId))
            if db.fetchone() is not None:
                continue
            cnt += 1
            keys, values = zip(*value.items())
            sql = f"""INSERT INTO enemy_handbook_table ({','.join(keys)}) 
                      VALUES ({','.join(['%s']*len(values))})"""
            args = tuple(map(dumps_json, values))
            db.execute(sql, args)
        logger.success("enemy_handbook_table更新完毕！")
        # 更新 enemy_database.json
        info = load_json(enemy_database)
        logger.info("开始更新enemy_database")
        for enemy in tqdm(info['enemies']):
            enemyId = enemy['Key']
            db.execute(
                "SELECT enemyId FROM enemy_database WHERE enemyId=%s", dumps_json(enemyId))
            if db.fetchone() is not None:
                continue
            cnt += 1
            keys, values = zip(*enemy.items())
            keys = ('enemyId',)+keys[1:]  # !
            sql = f"""INSERT INTO enemy_database ({','.join(keys)}) 
                      VALUES ({','.join(['%s']*len(values))})"""
            args = tuple(map(dumps_json, values))
            db.execute(sql, args)
        logger.success("enemy_database更新完毕！")
        return cnt

    def __init__(self, name=None):
        self.name = name

    def get_info(self):
        db = Database()
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
        sql = f"SELECT {','.join(keys[:-1])} FROM enemy_handbook_table WHERE name=%s"
        args = dumps_json(self.name)
        db.execute(sql, args)
        values = db.fetchone()
        if values is None:
            return None
        sql = f"SELECT Value FROM enemy_database WHERE enemyId=%s"
        args = dumps_json(loads_json(values[0]))  # enemyId
        db.execute(sql, args)
        values += db.fetchone()
        return dict(zip(keys, map(loads_json, values)))
