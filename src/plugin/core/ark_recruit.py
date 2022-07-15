# encoding:utf-8
"""明日方舟公招系统
"""
from functools import cmp_to_key
from itertools import combinations
from .baidu_ocr import BaiduOCR
from ..utils import download_async, json_to_obj


class ArkRecruit:
    """公开招募类,识别图片并生成公招建议
    """
    words_white_list = [
        '辅助干员','狙击干员','术师干员','重装干员','近卫干员','特种干员','先锋干员','医疗干员',
        '资深干员','高级资深干员','群攻','生存','位移','爆发','输出','治疗','削弱','减速','新手',
        '召唤','防护','支援','控场','近战位','远程位','快速复活','费用回复','支援机械'
    ]
    def __init__(self):
        """读取公招文件,初始化白名单
        """
        self.ocr = BaiduOCR()
        info = json_to_obj('data/recruit.json')
        self.n_ops = info['普通干员']
        self.s_ops = info['高级资深干员']

    def _ocr_file(self, file: str, accurate: bool = False) -> dict:
        """识别文件

        参数:
            file (str): 文件路径
            accurate (bool, optional): 是否启用高精度. Defaults to False.

        返回值:
            dict: 识别结果
        """
        with open(file, 'rb') as _:
            image = _.read()
        if accurate:
            return self.ocr.basic_accurate_ocr(image)
        return self.ocr.general_basic_ocr(image)

    async def _ocr_url(self, url: str, accurate: bool = False) -> dict:
        """识别url

        参数:
            url (str): url
            accurate (bool, optional): 是否启用高精度. Defaults to False.

        返回值:
            dict: 识别结果
        """
        image = await download_async(url)
        if accurate:
            return self.ocr.basic_accurate_ocr(image)
        return self.ocr.general_basic_ocr(image)

    async def get_tags(self, src: str, src_t: str, accurate: bool = False) -> list:
        """识别公招图片,获取Tag

        参数:
            src (str): 源文件
            src_t (str): 源文件类型
            accurate (bool, optional): 是否启用高精度. Defaults to False.

        返回值:
            list: Tags的列表
        """
        if src_t == 'file':
            words_result = self._ocr_file(src, accurate)
        elif src_t == 'url':
            words_result = await self._ocr_url(src, accurate)
        else:
            return []
        tags = [] # 获取白名单中的tag
        for each in words_result:
            words = each.strip().replace(' ', '')
            if '高级资' in words:
                words = '高级资深干员'
            elif '资深' in words:
                words = '资深干员'
            if words in self.words_white_list:
                tags.append(words)
        return tags

    async def get_advice(self, src: str, src_t: str, accurate: bool = False) -> str:
        """根据Tags自动生成公招建议

        参数:
            src (str): _description_
            src_t (str): _description_
            accurate (bool, optional): _description_. Defaults to False.

        返回值:
            str: _description_
        """
        tags = await self.get_tags(src, src_t, accurate)
        if '高级资深干员' in tags: # 有高资直接考虑高资
            if '资深干员' in tags: # 不再考虑资深
                tags.remove('资深干员')
            tags.remove('高级资深干员')
            pick_tags = []
            for i in range(1, 3): # 除高资外，额外选择1~2个tag
                for each in combinations(tags, i):
                    pick_tags.append(each)
            pick_tags.reverse()
            results = [] # 获取所有结果
            for each in pick_tags:
                hit_op = []  # tag命中的干员
                for op_name, op_info in self.s_ops.items():
                    if set(each).issubset(set(op_info['tags'])):
                        hit_op.append(op_name)
                if len(hit_op) > 0:
                    results.append((each, hit_op))
            def cmp_1(_x, _y): # 按hit数量升序
                return len(_x[1]) - len(_y[1])
            results.sort(key=cmp_to_key(cmp_1))
            advice = '' # 生成公招建议
            for result in results:
                advice += '[高级资深干员]'
                for tag in result[0]:
                    advice += f"[{tag}]"
                advice += ':\n'
                for op_name in result[1]:
                    advice += f"[{'★'*6}] {op_name}\n"
            return advice
        else: # 没有高资
            pick_tags = []
            for i in range(1, 4): # 选择1~3个tag
                for each in combinations(tags, i):
                    if each == ('资深干员',):
                        continue
                    pick_tags.append(each)
            pick_tags.reverse()
            results = [] # 获取所有结果
            for each in pick_tags:
                hit_op = []  # tag命中的干员
                min_level = 5  # 最低星级
                for op_name, op_info in self.n_ops.items():
                    if set(each).issubset(set(op_info['tags'])):
                        if op_info['level'] < 4:  # 最低小于4星忽略
                            hit_op = []
                            break
                        min_level = min(min_level, op_info['level'])
                        hit_op.append(op_name)
                if len(hit_op) > 0:
                    results.append((each, hit_op, min_level))
            def cmp_2(_x, _y):
                if _x[2] != _y[2]:
                    return _y[2]-_x[2]
                return len(_x[1])-len(_y[1])
            results.sort(key=cmp_to_key(cmp_2))
            advice = '' # 生成公招建议
            for result in results:
                for tag in result[0]:
                    advice += f"[{tag}]"
                advice += ':\n'
                result[1].sort(key=lambda x: self.n_ops[x]['level'])
                for op_name in result[1]:
                    level = self.n_ops[op_name]['level']
                    advice += f"[{'★'*level+'☆'*(6-level)}] {op_name}\n"
            return advice
