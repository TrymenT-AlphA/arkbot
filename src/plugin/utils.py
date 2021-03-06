"""实用工具集
1. 提供python对象,json文件,yaml文件的相互转换
2. 提供异步url下载
"""
from typing import Any, Optional
import jinja2
import re
import os
import json
import imgkit
import yaml
from aiohttp import ClientSession
from fake_useragent import UserAgent
from PIL import Image


# json文件与python对象的转换
def json_to_obj(path: str) -> Any:
    """读取json文件,并返回一个python对象

    参数:
        path (str): 文件路径

    返回值:
        Any: python对象
    """
    with open(path, 'r', encoding='utf8') as _:
        return json.load(_)


def obj_to_json(obj: Any, path: str) -> None:
    """传入一个python对象,并写入json文件保存

    参数:
        obj (Any): python对象
        path (str): 文件路径
    """
    with open(path, 'w', encoding='utf8') as _:
        json.dump(obj, _, ensure_ascii=False)


# yaml文件与python对象的转换
def yaml_to_obj(path: str) -> Any:
    """读取yaml文件,并返回一个python对象


    参数:
        path (str): 文件路径

    返回值:
        Any: python对象
    """
    with open(path, 'r', encoding='utf8') as _:
        return yaml.load(_, Loader=yaml.FullLoader)


def obj_to_yaml(obj: Any, path: str) -> None:
    """传入一个python对象,并写入yaml文件保存

    参数:
        obj (Any): python对象
        path (str): 文件路径
    """
    with open(path, 'w', encoding='utf8') as _:
        yaml.dump(obj, _, allow_unicode=True)


# json文件与yaml文件的转换
def json_to_yaml(json_path: str, yaml_path: str) -> None:
    """json文件转换为yaml文件

    参数:
        json_path (str): json文件路径
        yaml_path (str): yaml文件路径
    """
    obj = json_to_obj(json_path)
    obj_to_yaml(obj, yaml_path)


def yaml_to_json(yaml_path: str, json_path: str) -> None:
    """yaml文件转换为json文件

    参数:
        yaml_path (str): yaml文件路径
        json_path (str): json文件路径
    """
    obj = json_to_obj(yaml_path)
    obj_to_json(obj, json_path)


# json与string相互转换
def obj_to_json_str(obj: Any) -> str:
    """python对象转换为json格式字符串

    参数:
        obj (Any): python对象

    返回值:
        str: json格式字符串
    """
    return json.dumps(obj, ensure_ascii=False)


def json_str_to_obj(json_str: str) -> Any:
    """json格式字符串转换为python对象

    参数:
        json_str (str): json格式字符串

    返回值:
        Any: python对象
    """
    if isinstance(json_str, str) or isinstance(json_str, bytes):
        return json.loads(json_str)
    return json_str


def untag(string: str) -> str:
    """消去标签

    参数:
        string (str): 含tag字符串

    返回值:
        str: 无tag字符串
    """
    tag_p = re.compile(r'<.*?>')
    for tag in re.findall(tag_p, string):
        string = string.replace(tag, '')
    return string


def bring_in_blackboard(args: dict) -> str:
    """将blackboard中的值带入description中

    参数:
        args (dict): 含description和blackboard的字典

    返回值:
        str: 带入后的description
    """
    res = untag(args['description'])
    _p = re.compile("{.*?}")
    for i in re.findall(_p, args['description']):
        for j in args['blackboard']:
            if j['key'].upper() in i.upper():
                if '%' in i:
                    res = res.replace(i, str(round(j['value'] * 100, 1)) + '%')
                else:
                    res = res.replace(i, str(j['value']))
    return res


def img_paste(_fp: str, _bp: str, _op: str) -> None:
    """合并前景图和背景图

    参数:
        fp (str): 前景图路径
        bp (str): 背景图路径
        op (str): 输出图片路径
    """
    # return 1
    f_img = Image.open(_fp)
    b_img = Image.open(_bp)
    b_img.paste(f_img, mask=f_img)
    b_img.save(_op)


async def download_async(
        url: str, headers: Optional[dict] = None, stringify: bool = False) -> bytes or str or None:
    """异步下载url

    参数:
        url (str): 等待下载的url
        headers (dict, optional): 请求头. 默认为None,使用内部默认请求头.
        stringify (bool, optional): 是否以字符串形式返回. 默认为False.

    返回值:
        bytes or str or None: 获取的数据
    """
    default_headers = {
        'User-Agent': UserAgent().chrome
    }
    hdr = headers or default_headers
    async with ClientSession() as sess:
        async with sess.get(url, headers=hdr) as resp:
            if resp.status == 200:
                if stringify:
                    return await resp.text()
                return await resp.read()


def render_jinja(template_name: str, args: Optional[dict] = None, options: Optional[dict] = None) -> None:
    """根据模板生成页面并渲染成图片

    参数:
        template_name (str): 模板名称
        info (Any): 模板参数
    """
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('data/'))
    temp = env.get_template(f'{template_name}.jinja')
    html = temp.render(args=args)
    with open(f'data/{template_name}.html', 'w', encoding='utf8') as _:
        _.write(html)
    default_options = {
        'width': 1020,
        "enable-local-file-access": None
    }
    with open(f'data/{template_name}.html', 'r', encoding='utf8') as _:
        imgkit.from_file(_, f'data/{template_name}.jpg', options=options or default_options)
    os.remove(f'data/{template_name}.html')
