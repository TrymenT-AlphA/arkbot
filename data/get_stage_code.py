"""生成stage_code.json~
"""
import json

if __name__ == '__main__':
    res = {}
    with open('../arksrc/gamedata/excel/stage_table.json', 'r', encoding='utf8') as _:
        info = json.load(_)['stages']
    for key in info.keys():
        res[key] = info[key]['code']
    with open('stage_code.json', 'w', encoding='utf8') as _:
        json.dump(res, _, ensure_ascii=False)
