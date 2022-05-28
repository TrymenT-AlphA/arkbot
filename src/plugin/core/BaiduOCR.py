# encoding:utf-8

import yaml
import asyncio
from aip import AipOcr


class BaiduOCR:
    """
    百度OCR类
    """
    def __init__(self):
        """
        从recruit.yml读取配置，获取api接口
        """
        with open('config/ocr.yml', 'rb') as config: 
            recruit_config = yaml.load(config, Loader=yaml.FullLoader)['baidu-ocr']
        self.APP_ID = recruit_config['APP_ID']
        self.API_KEY = recruit_config['API_KEY']
        self.SECRET_KEY = recruit_config['SECRET_KEY']
        self.client = AipOcr(self.APP_ID, self.API_KEY, self.SECRET_KEY)

    async def get_general_basic_ocr(self, image):
        """
        通用文字识别
        """
        if type(image) == str:
            func = self.client.basicGeneralUrl
        else:
            func = self.client.basicGeneral
        
        options = {}
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, func, image, options)
    
    async def get_basic_accurate_ocr(self, image):
        """
        通用文字识别（高精度版）
        """
        if type(image) == str:
            func = self.client.basicAccurateUrl
        else:
            func = self.client.basicAccurate

        options = {}
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, func, image, options)

