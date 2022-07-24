"""明日方舟干员类
"""
from typing import Optional
import os
from tqdm import tqdm
from nonebot.log import logger
from .data_base import MySQL
from .ark_item import ArkItem
from .ark_range import ArkRange
from ..utils import json_to_obj
from ..utils import to_html
from ..utils import bring_in_blackboard


class ArkOp:
    """明日方舟干员
    """

    @staticmethod
    def update():
        """更新干员数据库
        """
        _db = MySQL()
        update_row = 0

        # 更新 character_table.json
        logger.success('开始更新character_table')
        info = json_to_obj('./arksrc/gamedata/excel/character_table.json')
        for _key, _val in tqdm(info.items()):
            if _db.select_one(
                    table='character_table',
                    keys=('name',),
                    condition='`name`=%s',
                    args=(_val['name'],)
            ):
                continue
            keys, vals = zip(*_val.items())
            _db.insert('character_table', keys, vals)
            update_row += 1
        logger.success('character_table更新完毕!')

        # 更新 skill_table.json
        logger.success('开始更新skill_table')
        info = json_to_obj('./arksrc/gamedata/excel/skill_table.json')
        for _key, _val in tqdm(info.items()):
            if _db.select_one(
                    table='skill_table',
                    keys=('skillId',),
                    condition='`skillId`=%s',
                    args=(_key,)
            ):
                continue
            keys, vals = zip(*_val.items())
            _db.insert('skill_table', keys, vals)
            update_row += 1
        logger.success('skill_table更新完毕!')

        return update_row

    def __init__(self, name=None):
        self.name = name

    def get_info(self) -> Optional[dict]:
        """获取干员信息
        """
        _db = MySQL()
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
        res = _db.select_one(
            table='character_table',
            keys=keys,
            condition=f"`name` LIKE '%{self.name}%'"
        )
        keys = (
            'skillId',
            'iconId',
            'hidden',
            'levels'
        )
        for i, _i in enumerate(res['skills']):
            res['skills'][i]['skillInfo'] = _db.select_one(
                table='skill_table',
                keys=keys,
                condition=f"`skillId`=%s",
                args=(_i['skillId'],)
            )
        # 数据预处理
        try:
            res['description'] = res['description'].replace('\\n', '</br>')
            res['description'] = to_html(res['description'])
        except KeyError:
            ...  # 忽略
        # 处理tagList
        if res['tagList'] is not None:
            res['tagList'] = ','.join(res['tagList'])
        # 处理职业信息，pass
        # 处理攻击范围信息
        for i, _ in enumerate(res['phases']):
            res['phases'][i]['range'] = ArkRange(_['rangeId']).get_html()
        # 处理天赋信息
        try:
            for i, _i in enumerate(res['talents']):
                for j, _j in enumerate(_i['candidates']):
                    res['talents'][i]['candidates'][j]['description'] = \
                        bring_in_blackboard(res['talents'][i]['candidates'][j]).replace('\\n', '</br>')
        except TypeError:
            ...
        # 处理技能信息
        for i, _i in enumerate(res['skills']):
            if _i['skillInfo']['iconId'] is None:
                res['skills'][i]['skillPic'] = \
                    f"file:///{os.getcwd()}/arksrc/skill/skill_icon_{_i['skillId']}.png"
            else:
                res['skills'][i]['skillPic'] = \
                    f"file:///{os.getcwd()}/arksrc/skill/skill_icon_{_i['skillInfo']['iconId']}.png"
            for j, _j in enumerate(_i['skillInfo']['levels']):
                res['skills'][i]['skillInfo']['levels'][j]['description'] = \
                    bring_in_blackboard(_i['skillInfo']['levels'][j]).replace('\\n', '</br>')
                if _i['skillInfo']['levels'][j]['rangeId'] is not None:
                    res['skills'][i]['skillInfo']['levels'][j]['range'] = \
                        ArkRange(_i['skillInfo']['levels'][j]['rangeId']).get_html()
        # 处理精英化材料信息
        for i, _i in enumerate(res['phases']):
            if _i['evolveCost'] is not None:
                for j, _j in enumerate(_i['evolveCost']):
                    res['phases'][i]['evolveCost'][j]['pic'] = \
                        ArkItem(item_id=_j['id']).get_info()['pic']
        # 处理技能升级表
        try:
            for i, _i in enumerate(res['allSkillLvlup']):
                for j, _j in enumerate(_i['lvlUpCost']):
                    res['allSkillLvlup'][i]['lvlUpCost'][j]['pic'] = \
                        ArkItem(item_id=_j['id']).get_info()['pic']
        except TypeError:
            ...
        # 处理技能专精表
        try:
            for i, _i in enumerate(res['skills']):
                for j, _j in enumerate(_i['levelUpCostCond']):
                    for k, _k in enumerate(_j['levelUpCost']):
                        res['skills'][i]['levelUpCostCond'][j]['levelUpCost'][k]['pic'] = \
                            ArkItem(item_id=_k['id']).get_info()['pic']
        except TypeError:
            ...
        # 处理职业信息
        profession_dict = json_to_obj('data/profession_dict.json')
        res['professionName'] = profession_dict[f"{res['profession']}_{res['subProfessionId']}"]
        res['professionIcon'] = f"file:///{os.getcwd()}/data/profession_icon/职业分支图标_{res['professionName']}.png"
        res['pic'] = f"file:///{os.getcwd()}/arksrc/avatar/{res['phases'][0]['characterPrefabKey']}.png"
        return res
