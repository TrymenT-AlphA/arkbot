# encoding:utf-8
"""OCR类,提供文字识别
"""
from aip import AipOcr
from ..utils import json_to_obj


class BaiduOCR:
    """OCR类,提供文字识别
    """
    def __init__(self) -> None:
        """读取配置,创建实例
        """
        _ = json_to_obj('config.yml')['baiduocr'] # OCR配置信息
        self._app_id = _['APP_ID']
        self._api_key = _['API_KEY']
        self._secret_key = _['SECRET_KEY']
        # client实例用于实现各种操作
        self.client = AipOcr(self._app_id, self._api_key, self._secret_key)

    def get_app_id(self) -> str:
        """获取当前OCR应用的APP_ID
        """
        return self._app_id

    def get_api_key(self) -> str:
        """获取当前OCR应用的API_KEY
        """
        return self._api_key

    def get_secret_key(self) -> str:
        """获取当前OCR应用的SECRET_KEY
        """
        return self._secret_key

    def general_basic_ocr(self, image: str or bytes, options: dict or None = None) -> dict:
        """通用文字识别

        参数:
            image (strorbytes): 图像url或二进制数据
            options (dictorNone): 额外参数,详见baidu-api

        返回值:
            dict: 识别结果
        """
        if isinstance(image, str):
            func = self.client.basicGeneralUrl # 通过url定位图片
        else:
            func = self.client.basicGeneral # 直接传入二进制数据
        default_options = {} # 额外参数，详见baidu-api
        tmp = func(image, options or default_options)
        return list(each['words'] for each in tmp['words_result'])

    def basic_accurate_ocr(self, image: str or bytes, options: dict or None = None) -> dict:
        """通用文字识别(高精度)

        参数:
            image (strorbytes): 图像url或二进制数据
            options (dictorNone): 额外参数,详见baidu-api

        返回值:
            dict: 识别结果
        """
        if isinstance(image, str):
            func = self.client.basicAccurateUrl # 通过url定位图片
        else:
            func = self.client.basicAccurate # 直接传入二进制数据
        default_options = {} # 额外参数，详见baidu-api
        tmp = func(image, options or default_options)
        return list(each['words'] for each in tmp['words_result'])
