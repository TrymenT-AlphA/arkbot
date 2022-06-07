# encoding:utf-8
import json
import pymysql

from .Database import Database


class Enemy:
    """明日方舟敌方单位
    """
    database = Database()

    @classmethod
    def update(cls) -> None:
        # 两个文件待更新
        # Arknights-Bot-Resource/gamedata/excel/enemy_handbook_table.json
        # Arknights-Bot-Resource/gamedata/levels/enemydata/enemy_database.json
        # 连接数据库
        db = pymysql.connect(
            host=cls.database.host,
            user=cls.database.user,
            password=cls.database.password,
            database=cls.database.database)
        if db is None:
            return
        cursor = db.cursor()
        # update enemy_handbook_table.json
        with open('Arknights-Bot-Resource/gamedata/excel/enemy_handbook_table.json', 'rb') as f:
            info = json.load(f)
        for enemyId, value in info.items():
            sql, args = f"SELECT enemyId FROM enemy_handbook_table WHERE enemyId=%s", enemyId
            try:
                cursor.execute(sql, args)
            except Exception as e:
                print(e)
                cursor.close(), db.close()
                return
            if cursor.fetchone() is None:
                keys = tuple(map(str,value.keys()))
                values = tuple(map(str,value.values()))
                sql = f"""INSERT INTO enemy_handbook_table ({','.join(keys)}) 
                          VALUES ({','.join(['%s']*len(values))})"""
                args = values
                try:
                    cursor.execute(sql, args)
                except Exception as e:
                    print(e)
                    db.rollback(), cursor.close(), db.close()
                    return
        db.commit()
        # update enemy_database.json
        with open('Arknights-Bot-Resource/gamedata/levels/enemydata/enemy_database.json', 'rb') as f:
            info = json.load(f)
        for enemy in info['enemies']:
            enemyId = enemy['Key']
            sql, args = f"SELECT enemyId FROM enemy_database WHERE enemyId=%s", enemyId
            try:
                cursor.execute(sql, args)
            except Exception as e:
                print(e)
                cursor.close(), db.close()
                return
            if cursor.fetchone() is None:
                keys = ('enemyId',)+tuple(map(str,enemy.keys()))[1:]
                values = tuple(map(str,enemy.values()))
                sql = f"""INSERT INTO enemy_database ({','.join(keys)}) 
                          VALUES ({','.join(['%s']*len(values))})"""
                args = values
                try:
                    cursor.execute(sql, args)
                except Exception as e:
                    print(e)
                    db.rollback(), cursor.close(), db.close()
                    return
        db.commit()
        # 关闭数据库
        cursor.close(), db.close()

    def __init__(self, name = None):
        self.name = name
