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
        with open('config/recruit.yml', 'rb') as f:
            info = yaml.load(f.read(), Loader=yaml.FullLoader)
        self.normal_ops = info['普通干员']
        self.special_ops = info['高级资深干员']
        self.words_white_list = [
            '辅助干员', '狙击干员', '术师干员', '重装干员', '近卫干员', '特种干员', '先锋干员', '医疗干员', 
            '资深干员', '高级资深干员', '群攻', '生存', '位移', '爆发', '输出', '治疗', '削弱', '减速', '新手', 
            '召唤', '防护', '支援', '控场', '近战位', '远程位', '快速复活', '费用回复', '支援机械',
        ]
    
    async def get_ocr_file(self, file):
        """
        通过文件请求api识别
        """
        with open(file, 'rb') as f:
            image = f.read()
        return await self.ocr.get_general_basic_ocr(image)

    async def get_ocr_url(self, url):
        """
        通过url请求api识别
        """
        image = await download_async(url)
        return await self.ocr.get_general_basic_ocr(image)
    
    async def get_tags(self, src):
        """
        获取识别结果中的tag
        如果以'file:///'开头，调用文件识别
        否则调用url识别
        """
        if 'file:///' in src:
            info = await self.get_ocr_file(src[8:])
        else:
            info = await self.get_ocr_url(src)
        
        words_result = info['words_result']
        tags = []
        for each in words_result:
            words = each['words']
            if '高级资' in words:
                words = '高级资深干员'
            if words in self.words_white_list:
                tags.append(words)
        return tags
    
    async def get_advice(self, src):
        """
        获取公开招募建议
        """
        tags: list = await self.get_tags(src)
        if '高级资深干员' in tags:

            if '资深干员' in tags:
                tags.remove('资深干员')
            tags.remove('高级资深干员')

            selections = []
            for i in range(1, 3):
                for each in combinations(tags, i):
                    selections.append(each)
            selections.reverse()

            results = []
            for selection in selections:
                hit = []
                for op_name, op_info in self.special_ops.items():
                    if set(selection).issubset(set(op_info['tags'])):
                        hit.append(op_name)
                if len(hit) > 0:
                    results.append((selection, hit))
            results.sort(key=cmp_to_key(lambda x, y: len(x[1]) - len(y[1])))

            string = ''
            for result in results:
                string += '[高级资深干员]'
                for tag in result[0]:
                    string += f"[{tag}]"
                string += ':\n'
                for op_name in result[1]:
                    string += f"[{'★'*6}] {op_name}\n"
            return string

        else:

            selections = []
            for i in range(1, 4):
                for each in combinations(tags, i):
                    selections.append(each)
            selections.reverse()

            results = []
            for selection in selections:
                hit = []
                min_level = 5
                for op_name, op_info in self.normal_ops.items():
                    if set(selection).issubset(set(op_info['tags'])):
                        if op_info['level'] < 4:
                            hit = []
                            break
                        else:
                            min_level = min(min_level, op_info['level'])
                            hit.append(op_name)
                if len(hit) > 0:
                    results.append((selection, hit, min_level))
            results.sort(key=cmp_to_key(lambda x, y: y[2]-x[2] if x[2]!=y[2] else len(x[1])-len(y[1])))

            string = ''
            for result in results:
                for tag in result[0]:
                    string += f"[{tag}]"
                string += ':\n'
                result[1].sort(key=lambda x: self.normal_ops[x]['level'])
                for op_name in result[1]:
                    level = self.normal_ops[op_name]['level']
                    string += f"[{'★'*level+'☆'*(6-level)}] {op_name}\n"
            return string
