# encoding:utf-8
from nonebot.log import logger
import pymysql
import json
from tqdm import tqdm

from .Database import Database


class Enemy:
    """明日方舟敌方单位
    """
    database = Database()

    @classmethod
    def update(cls) -> bool:
        path_1 = 'Arknights-Bot-Resource/gamedata/excel/enemy_handbook_table.json'
        path_2 = 'Arknights-Bot-Resource/gamedata/levels/enemydata/enemy_database.json'
        # 连接数据库
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
            args = str(enemyId)
            cursor.execute(sql, args)
            if cursor.fetchone() is None:
                keys, values = zip(*value.items())
                sql = f"""INSERT INTO enemy_handbook_table ({','.join(keys)}) 
                          VALUES ({','.join(['%s']*len(values))})"""
                args = tuple(map(str,values))
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
            args = str(enemyId)
            cursor.execute(sql, args)
            if cursor.fetchone() is None:
                keys, values = zip(*enemy.items())
                keys = ('enemyId',)+keys[1:] #!
                sql = f"""INSERT INTO enemy_database ({','.join(keys)}) 
                          VALUES ({','.join(['%s']*len(values))})"""
                args = tuple(map(str,values))
                cursor.execute(sql, args)
        db.commit()
        logger.success("enemy_database更新完毕！")
        # 关闭数据库
        cursor.close(), db.close()
        return True

    def __init__(self, name = None):
        self.name = name
    
    def get_handbook_info(self):
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
            'enemyTags',
            'name',
            'enemyRace',
            'enemyLevel',
            'description',
            'attackType',
            'attack',
            'defencce',
            'resistance',
            'ability',
        )
        sql = f"SELECT ({','.join(params)}) FROM enemy_handbook_table WHERE name=%s"
        args = str(self.name)
        cursor.execute(sql, args)
        result = cursor.fetchone()
        if result is None:
            return None
        else:
            return dict(zip(params, result))
