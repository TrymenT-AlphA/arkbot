# encoding:utf-8
import json

import pymysql
from nonebot.log import logger
from tqdm import tqdm

from .Database import Database


class Enemy:

    database = Database()

    @classmethod
    def update(cls) -> int:
        path_1 = 'Arknights-Bot-Resource/gamedata/excel/enemy_handbook_table.json'
        path_2 = 'Arknights-Bot-Resource/gamedata/levels/enemydata/enemy_database.json'
        # 连接数据库
        cnt = 0
        db = pymysql.connect(
            host=cls.database.host,
            user=cls.database.user,
            password=cls.database.password,
            database=cls.database.database)
        if db is None:
            logger.error("数据库连接失败")
            return False
        cursor = db.cursor()
        # 更新 enemy_handbook_table.json
        with open(path_1, 'rb') as f:
            info = json.load(f)
        logger.info("开始更新enemy_handbook_table")
        for enemyId, value in tqdm(info.items()):
            sql = f"SELECT enemyId FROM enemy_handbook_table WHERE enemyId=%s"
            args = json.dumps(enemyId)
            cursor.execute(sql, args)
            if cursor.fetchone() is None:
                cnt += 1
                keys, values = zip(*value.items())
                sql = f"""INSERT INTO enemy_handbook_table ({','.join(keys)}) 
                          VALUES ({','.join(['%s']*len(values))})"""
                args = tuple(map(json.dumps, values))
                cursor.execute(sql, args)
        db.commit()
        logger.success("enemy_handbook_table更新完毕！")
        # 更新 enemy_database.json
        with open(path_2, 'rb') as f:
            info = json.load(f)
        logger.info("开始更新enemy_database")
        for enemy in tqdm(info['enemies']):
            enemyId = enemy['Key']
            sql = f"SELECT enemyId FROM enemy_database WHERE enemyId=%s"
            args = json.dumps(enemyId)
            cursor.execute(sql, args)
            if cursor.fetchone() is None:
                cnt += 1
                keys, values = zip(*enemy.items())
                keys = ('enemyId',)+keys[1:]  # !
                sql = f"""INSERT INTO enemy_database ({','.join(keys)}) 
                          VALUES ({','.join(['%s']*len(values))})"""
                args = tuple(map(json.dumps, values))
                cursor.execute(sql, args)
        db.commit()
        logger.success("enemy_database更新完毕！")
        # 关闭数据库
        cursor.close(), db.close()
        return cnt

    def __init__(self, name=None):
        self.name = name

    def get_simple_info(self):
        # 连接数据库
        db = pymysql.connect(
            host=self.database.host,
            user=self.database.user,
            password=self.database.password,
            database=self.database.database)
        if db is None:
            logger.error("数据库连接失败")
            return False
        cursor = db.cursor()
        # 查询name==self.name
        params = (
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
        )
        sql = f"SELECT {','.join(params)} FROM enemy_handbook_table WHERE name=%s"
        args = json.dumps(self.name)
        cursor.execute(sql, args)
        simple_info = cursor.fetchone()
        if simple_info is None:
            return None
        else:
            return dict(zip(params, map(json.loads, simple_info)))

    def get_detail_info(self):
        # 连接数据库
        db = pymysql.connect(
            host=self.database.host,
            user=self.database.user,
            password=self.database.password,
            database=self.database.database)
        if db is None:
            logger.error("数据库连接失败")
            return False
        cursor = db.cursor()
        # 查询name==self.name
        detail_info = self.get_simple_info()
        if detail_info is None:
            return None
        sql = f"SELECT Value FROM enemy_database WHERE enemyId=%s"
        args = json.dumps(detail_info['enemyId'])
        cursor.execute(sql, args)
        detail_info['Value'] = json.loads(cursor.fetchone()[0])
        return detail_info
