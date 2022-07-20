# encoding:utf-8
"""OCR类
"""
from typing import Optional, Union
from aip import AipOcr
from ..utils import yaml_to_obj


class BaiduOCR:
    """OCR类
    """

    def __init__(self) -> None:
        """读取配置
        """
        _ = yaml_to_obj('config.yml')['baiduocr']
        self._app_id = _['APP_ID']
        self._api_key = _['API_KEY']
        self._secret_key = _['SECRET_KEY']
        self.client = AipOcr(self._app_id, self._api_key, self._secret_key)

    def general_basic_ocr(self, image: Union[str, bytes], options: Optional[dict] or None = None) -> list:
        """通用文字识别

        参数:
            image (Union[str, bytes]): 图像url或二进制数据
            options (dictorNone): 额外参数

        返回值:
            dict: 识别结果
        """
        if isinstance(image, str):
            func = self.client.basicGeneralUrl
        else:
            func = self.client.basicGeneral
        default_options = {}
        tmp = func(image, options or default_options)
        return list(each['words'] for each in tmp['words_result'])

    def basic_accurate_ocr(self, image: Union[str, bytes], options: dict or None = None) -> list:
        """通用文字识别(高精度)

        参数:
            image (Union[str, bytes]): 图像url或二进制数据
            options (dictorNone): 额外参数

        返回值:
            dict: 识别结果
        """
        if isinstance(image, str):
            func = self.client.basicAccurateUrl
        else:
            func = self.client.basicAccurate
        default_options = {}
        tmp = func(image, options or default_options)
        return list(each['words'] for each in tmp['words_result'])
