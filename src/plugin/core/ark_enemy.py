"""明日方舟敌方单位
"""
from typing import Optional
import os
from tqdm import tqdm
from nonebot.log import logger
from .data_base import MySQL
from ..utils import json_to_obj
from ..utils import to_html


class ArkEnemy:
    """明日方舟敌方单位
    """

    @staticmethod
    def update() -> int:
        """更新数据库

        返回值:
            int: 更新的条数
        """
        _db = MySQL()
        update_row = 0

        # 更新 enemy_handbook_table.json
        logger.success('开始更新enemy_handbook_table')
        info = json_to_obj('arksrc/gamedata/excel/enemy_handbook_table.json')
        for _key, _val in tqdm(info.items()):
            if _db.select_one(
                    table='enemy_handbook_table',
                    keys=('enemyId',),
                    condition='`enemyId`=%s',
                    args=(_key,)
            ):
                continue
            keys, vals = zip(*_val.items())
            _db.insert('enemy_handbook_table', keys, vals)
            update_row += 1
        logger.success('enemy_handbook_table更新完毕!')

        # 更新 enemy_database.json
        logger.success('开始更新enemy_database')
        info = json_to_obj('arksrc/gamedata/levels/enemydata/enemy_database.json')
        for _val in tqdm(info['enemies']):
            if _db.select_one(
                    table='enemy_database',
                    keys=('Key',),
                    condition='`Key`=%s',
                    args=(_val['Key'],)
            ):
                continue
            keys, vals = zip(*_val.items())
            _db.insert('enemy_database', keys, vals)
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
            'ability'
        )
        _db = MySQL()
        res = _db.select_one(
            table='enemy_handbook_table',
            keys=keys,
            condition=f"`name` LIKE '%{self.name}%'"
        )
        res['Value'] = _db.select_one(
            table='enemy_database',
            keys=('Value',),
            condition="`Key`=%s",
            args=(res['enemyId'],)
        )['Value']
        res['pic'] = f"file:///{os.getcwd()}/arksrc/enemy/{res['enemyId']}.png"
        # 数据二次处理
        try:
            res['description'] = to_html(res['description'])
            res['ability'] = to_html(res['ability'])
            _ = res['Value'][0]['enemyData']['description']
            _['m_value'] = to_html(_['m_value'])
        except KeyError:
            ...
        for i in range(1, len(res['Value'])):
            level_0 = res['Value'][0]['enemyData']
            level_i = res['Value'][i]['enemyData']
            for _k, _v in level_i.items():
                if _k != 'attributes':
                    if level_0[_k] and not level_i[_k]:
                        level_i[_k] = level_0[_k]
                    elif isinstance(_v, dict):
                        if level_0[_k]['m_defined'] and not level_i[_k]['m_defined']:
                            level_i[_k] = level_0[_k]
                else:
                    for _kk, _vv in _v.items():
                        if level_0[_k][_kk]['m_defined'] and not level_i[_k][_kk]['m_defined']:
                            level_i[_k][_kk] = level_0[_k][_kk]
        return res
