# encoding:utf-8
import yaml
import asyncio
from aip import AipOcr
from typing import Union, ByteString

from .Singleton import Singleton

@Singleton
class BaiduOCR:
        
    def __init__(self) -> None:
        """
        初始化配置
        """
        with open('config.yml', 'rb') as f:
            info = yaml.load(f, Loader=yaml.FullLoader)['baiduocr']
        self.APP_ID = info['APP_ID']
        self.API_KEY = info['API_KEY']
        self.SECRET_KEY = info['SECRET_KEY']
        self.client = AipOcr(self.APP_ID, self.API_KEY, self.SECRET_KEY)

    async def get_general_basic_ocr(self,
                                    image: Union[str, ByteString]) -> dict:
        """
        通用文字识别
        """
        if type(image) == str:
            func = self.client.basicGeneralUrl
        else:
            func = self.client.basicGeneral
        # 额外参数，详见baidu-api
        options = {}
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, func, image, options)

    async def get_basic_accurate_ocr(self,
                                     image: Union[str, bytes]) -> dict:
        """
        通用文字识别（高精度版）
        """
        if type(image) == str:
            func = self.client.basicAccurateUrl
        else:
            func = self.client.basicAccurate
        # 额外参数，详见baidu-api
        options = {}
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, func, image, options)
