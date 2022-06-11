# encoding:utf-8
from aip import AipOcr

from ..utils import load_yaml


class BaiduOCR:

    def __init__(self) -> None:
        info = load_yaml('config.yml')['baiduocr']
        self.APP_ID = info['APP_ID']
        self.API_KEY = info['API_KEY']
        self.SECRET_KEY = info['SECRET_KEY']
        self.client = AipOcr(self.APP_ID, self.API_KEY, self.SECRET_KEY)

    def general_basic_ocr(self, image: str or bytes) -> dict:
        if type(image) == str:
            func = self.client.basicGeneralUrl
        else:
            func = self.client.basicGeneral
        # 额外参数，详见baidu-api
        options = {}
        return func(image, options)

    def basic_accurate_ocr(self, image: str or bytes) -> dict:
        if type(image) == str:
            func = self.client.basicAccurateUrl
        else:
            func = self.client.basicAccurate
        # 额外参数，详见baidu-api
        options = {}
        return func(image, options)
