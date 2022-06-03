# encoding:utf-8
import yaml
from functools import cmp_to_key
from itertools import combinations

from .BaiduOCR import BaiduOCR
from ..utils.download import download_async


class Recruit:
    """
    公开招募类
    """
    def __init__(self):
        """
        初始化百度ocr和白名单
        """
        self.ocr = BaiduOCR()
        with open('data/recruit.yml', 'rb') as f:
            info = yaml.load(f.read(), Loader=yaml.FullLoader)
        self.normal_ops = info['普通干员']
        self.special_ops = info['高级资深干员']
        self.words_white_list = [
            '辅助干员', '狙击干员', '术师干员', '重装干员', '近卫干员', '特种干员', '先锋干员', '医疗干员',
            '资深干员', '高级资深干员', '群攻', '生存', '位移', '爆发', '输出', '治疗', '削弱', '减速',
            '新手', '召唤', '防护', '支援', '控场', '近战位', '远程位', '快速复活', '费用回复', '支援机械',
        ]

    async def get_ocr_file(self, file: str, accurate: bool = False) -> dict:
        """
        通过文件请求api识别
        """
        with open(file, 'rb') as f:
            image = f.read()
        # 是否采用高精度识别
        if accurate:
            return await self.ocr.get_basic_accurate_ocr(image)
        else:
            return await self.ocr.get_general_basic_ocr(image)

    async def get_ocr_url(self, url: str, accurate: bool = False) -> dict:
        """
        通过url请求api识别
        """
        image = await download_async(url)
        # 是否采用高精度识别
        if accurate:
            return await self.ocr.get_basic_accurate_ocr(image)
        else:
            return await self.ocr.get_general_basic_ocr(image)

    async def get_tags(self,
                       src: str,
                       src_t: str,
                       accurate: bool = False) -> list:
        """
        获取识别结果中的tag
        """
        if src_t == 'file':
            info = await self.get_ocr_file(src, accurate)
        elif src_t == 'url':
            info = await self.get_ocr_url(src, accurate)
        else:
            return []
        # 获取白名单中的tag
        tags = []
        words_result = info['words_result']
        for each in words_result:
            words = each['words']
            if '高级资' in words:
                words = '高级资深干员'
            if words in self.words_white_list:
                tags.append(words)
        return tags

    async def get_advice(self,
                         src: str,
                         src_t: str,
                         accurate: bool = False) -> str:
        """
        获取公开招募建议
        """
        tags = await self.get_tags(src, src_t, accurate)
        # 有高资直接考虑高资
        if '高级资深干员' in tags:
            if '资深干员' in tags:
                tags.remove('资深干员')
            tags.remove('高级资深干员')
            # 除高资外，额外选择1~2个tag
            selections = []
            for i in range(1, 3):
                for each in combinations(tags, i):
                    selections.append(each)
            selections.reverse()
            # 获取所有结果
            results = []
            for selection in selections:
                hit = []  # tag命中的干员
                for op_name, op_info in self.special_ops.items():
                    if set(selection).issubset(set(op_info['tags'])):
                        hit.append(op_name)
                if len(hit) > 0:
                    results.append((selection, hit))

            # 按hit数量升序
            def cmp1(x, y):
                return len(x[1]) - len(y[1])
            results.sort(key=cmp_to_key(cmp1))
            # 生成公招建议
            advice = ''
            for result in results:
                advice += '[高级资深干员]'
                for tag in result[0]:
                    advice += f"[{tag}]"
                advice += ':\n'
                for op_name in result[1]:
                    advice += f"[{'★'*6}] {op_name}\n"
            return advice
        # 没有高资
        else:
            # 选择1~3个tag
            selections = []
            for i in range(1, 4):
                for each in combinations(tags, i):
                    selections.append(each)
            selections.reverse()
            # 获取所有结果
            results = []
            for selection in selections:
                hit = []  # tag命中的干员
                min_level = 5  # 最低星级
                for op_name, op_info in self.normal_ops.items():
                    if set(selection).issubset(set(op_info['tags'])):
                        if op_info['level'] < 4:  # 最低小于4星忽略
                            hit = []
                            break
                        else:
                            min_level = min(min_level, op_info['level'])
                            hit.append(op_name)
                if len(hit) > 0:
                    results.append((selection, hit, min_level))

            # 优先星级降序，hit数量升序
            def cmp2(x, y):
                if x[2] != y[2]:
                    return y[2]-x[2]
                else:
                    return len(x[1])-len(y[1])
            results.sort(key=cmp_to_key(cmp2))
            # 生成公招建议
            advice = ''
            for result in results:
                for tag in result[0]:
                    advice += f"[{tag}]"
                advice += ':\n'
                result[1].sort(key=lambda x: self.normal_ops[x]['level'])
                for op_name in result[1]:
                    level = self.normal_ops[op_name]['level']
                    advice += f"[{'★'*level+'☆'*(6-level)}] {op_name}\n"
            return advice
