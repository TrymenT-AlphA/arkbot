"""明日方舟干员类
"""
from nonebot.log import logger
from tqdm import tqdm
from .data_base import Database
from ..utils import json_to_obj, obj_to_json_str


class ArkOp:
    """明日方舟干员
    """
    @staticmethod
    def update():
        """更新干员数据库
        """
        _db = Database()
        # 1. 更新 character_table.json
        logger.success("开始更新character_table")
        character_table = "./arksrc/gamedata/excel/character_table.json"
        info = json_to_obj(character_table)
        update_row = 0
        for _id, _ in tqdm(info.items()):
            sql = """SELECT `name` FROM `character_table`
                WHERE `name`=%s""" # 尝试查询一条数据
            args = obj_to_json_str(_['name'])
            _db.execute(sql, args)
            if _db.fetchone() is not None:
                continue # 条目已存在,直接跳过
            update_row += 1
            keys, values = zip(*_.items())
            sql = f"""INSERT INTO `character_table`
                ({','.join([f"`{key}`" for key in keys])})
                VALUES ({','.join(['%s']*len(values))})"""
            args = tuple(map(obj_to_json_str, values))
            _db.execute(sql, args)
        logger.success("character_table更新完毕!")
        # 1. 更新 skill_table.json
        logger.success("开始更新skill_table")
        skill_table = "./arksrc/gamedata/excel/skill_table.json"
        info = json_to_obj(skill_table)
        update_row = 0
        for _id, _ in tqdm(info.items()):
            sql = """SELECT `skillId` FROM `skill_table`
                WHERE `skillId`=%s""" # 尝试查询一条数据
            args = obj_to_json_str(_id)
            _db.execute(sql, args)
            if _db.fetchone() is not None:
                continue # 条目已存在,直接跳过
            update_row += 1
            keys, values = zip(*_.items())
            sql = f"""INSERT INTO `skill_table`
                ({','.join([f"`{key}`" for key in keys])})
                VALUES ({','.join(['%s']*len(values))})"""
            args = tuple(map(obj_to_json_str, values))
            _db.execute(sql, args)
        logger.success("skill_table更新完毕!")
        return update_row

    def __init__(self, name=None):
        self.name = name

    def getinfo(self):
        """获取干员信息
        """
        # do sth.
