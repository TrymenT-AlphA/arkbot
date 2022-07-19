# encoding:utf-8
"""攻击范围
"""
from tqdm import tqdm
from nonebot.log import logger
from .data_base import Database
from ..utils import json_to_obj, obj_to_json_str, json_str_to_obj


class ArkRange:
    """攻击范围类
    """
    @staticmethod
    def update() -> int:
        """更新攻击范围数据库

        返回值:
            int: 更新的条目数
        """
        _db = Database()
        # 1. 更新 range_table.json
        logger.success("开始更新range_table")
        range_table = 'arksrc/gamedata/excel/range_table.json'
        info = json_to_obj(range_table)
        update_row = 0
        for _id, _ in tqdm(info.items()):
            sql = """SELECT `id` FROM `range_table`
                WHERE `id`=%s""" # 尝试查询一条数据
            args = obj_to_json_str(_id)
            _db.execute(sql, args)
            if _db.fetchone() is not None:
                continue # 条目已存在,直接跳过
            update_row += 1
            keys, values = zip(*_.items())
            sql = f"""INSERT INTO `range_table`
                ({','.join([f"`{key}`" for key in keys])})
                VALUES ({','.join(['%s']*len(values))})"""
            args = tuple(map(obj_to_json_str, values))
            _db.execute(sql, args)
        logger.success("range_table更新完毕!")
        return update_row

    def __init__(self, _id: str) -> None:
        self._id = _id

    def get_html(self) -> str or None:
        """获取对应的html代码

        返回值:
            str: 对应的html代码
        """
        _db = Database()
        sql = """SELECT `grids` FROM `range_table`
            WHERE id =%s"""
        args = obj_to_json_str(self._id)
        _db.execute(sql, args)
        res = _db.fetchone()
        if res is None:
            return
        res = json_str_to_obj(res[0])
        coordinates = []
        min_row, min_col = 0, 0
        max_x, max_y = 0, 0
        for each in res:
            min_row = min(min_row, each['row'])
            min_col = min(min_col, each['col'])
            if each['row'] == 0 and each['col'] == 0:
                coordinates.append([1, 1])
            else:
                coordinates.append([2+each['col']*26, 2+each['row']*26])
        for i, _ in enumerate(coordinates):
            coordinates[i][0] -= 26 * min_col
            max_x = max(max_x, coordinates[i][0])
            coordinates[i][1] -= 26 * min_row
            max_y = max(max_y, coordinates[i][1])
        res = f"""
        <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="vertical-align:top;width:{max_x+24}px;height:{max_y+24}px">
        <defs>
            <rect id="1" fill="#27a6f3" width="22" height="22"></rect>
            <rect id="2" fill="none" stroke="gray" stroke-width="2" width="20" height="20"></rect>
        </defs>"""
        for each in coordinates:
            if each[0] == 1 - 26*min_col and each[1] == 1 - 26*min_row:
                res += f"""
        <use xlink:href="#1" x="{each[0]}" y="{each[1]}"></use>"""
            else:
                res += f"""
        <use xlink:href="#2" x="{each[0]}" y="{each[1]}"></use>"""
        res += """
        </svg>"""
        return res
