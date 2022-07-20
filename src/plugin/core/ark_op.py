"""明日方舟干员类
"""
from typing import Optional
import os
from tqdm import tqdm
from nonebot.log import logger
from .data_base import Database
from ..utils import json_to_obj, obj_to_json_str, json_str_to_obj


class ArkOp:
    """明日方舟干员
    """

    @staticmethod
    def update():
        """更新干员数据库
        """
        _db = Database()
        update_row = 0
        # 1. 更新 character_table.json
        logger.success('开始更新character_table')
        info = json_to_obj('./arksrc/gamedata/excel/character_table.json')
        for _key, _val in tqdm(info.items()):
            sql = """SELECT `name` FROM `character_table` WHERE `name`=%s"""
            args = obj_to_json_str(_val['name'])
            _db.execute(sql, args)
            if _db.fetchone() is not None:
                continue
            keys, values = zip(*_val.items())
            sql = f"""INSERT INTO `character_table`
                ({','.join([f"`{_}`" for _ in keys])})
                VALUES ({','.join(['%s'] * len(values))})
                """
            args = tuple(map(obj_to_json_str, values))
            _db.execute(sql, args)
            update_row += 1
        logger.success('character_table更新完毕!')
        # 1. 更新 skill_table.json
        logger.success('开始更新skill_table')
        info = json_to_obj('./arksrc/gamedata/excel/skill_table.json')
        for _key, _val in tqdm(info.items()):
            sql = """SELECT `skillId` FROM `skill_table` WHERE `skillId`=%s"""
            args = obj_to_json_str(_key)
            _db.execute(sql, args)
            if _db.fetchone() is not None:
                continue
            keys, values = zip(*_val.items())
            sql = f"""INSERT INTO `skill_table`
                ({','.join([f"`{_}`" for _ in keys])})
                VALUES ({','.join(['%s'] * len(values))})
                """
            args = tuple(map(obj_to_json_str, values))
            _db.execute(sql, args)
            update_row += 1
        logger.success('skill_table更新完毕!')
        return update_row

    def __init__(self, name=None):
        self.name = name

    def get_info(self) -> Optional[dict]:
        """获取干员信息
        """
        keys = (
            'name',
            'description',
            'canUseGeneralPotentialItem',
            'potentialItemId',
            'nationId',
            'groupId',
            'teamId',
            'displayNumber',
            'tokenKey',
            'appellation',
            'position',
            'tagList',
            'itemUsage',
            'itemDesc',
            'itemObtainApproach',
            'isNotObtainable',
            'isSpChar',
            'maxPotentialLevel',
            'rarity',
            'profession',
            'subProfessionId',
            'trait',
            'phases',
            'skills',
            'talents',
            'potentialRanks',
            'favorKeyFrames',
            'allSkillLvlup'
        )
        sql = f"""SELECT {','.join([f"`{_}`" for _ in keys])}
            FROM `character_table` WHERE `name` LIKE '%{self.name}%'
            """
        _db = Database()
        _db.execute(sql)
        res: tuple = _db.fetchone()
        if res is None:
            return None
        res: dict = dict(zip(keys, map(json_str_to_obj, res)))
        keys = (
            'skillId',
            'iconId',
            'hidden',
            'levels'
        )
        for i, _i in enumerate(res['skills']):
            sql = f"""SELECT {','.join([f"`{_}`" for _ in keys])}
                FROM `skill_table` WHERE `skillId`=%s
                """
            args = obj_to_json_str(_i['skillId'])
            _db.execute(sql, args)
            tmp = _db.fetchone()
            assert tmp is not None
            tmp = dict(zip(keys, map(json_str_to_obj, tmp)))
            res['skills'][i]['skillInfo'] = tmp
        res['pic'] = f"file:///{os.getcwd()}/arksrc/avatar/{res['phases'][0]['characterPrefabKey']}.png"
        return res
