"""实用工具集
"""
from typing import Any
from typing import Union
from typing import Optional
import re
import os
import json
import yaml
import imgkit
import jinja2
from aiohttp import ClientSession
from fake_useragent import UserAgent


def json_to_obj(path: str) -> Any:
    """json文件转换为python对象

    参数:
        path: json文件

    返回值:
        Any: python对象
    """
    with open(path, 'r', encoding='utf8') as _:
        return json.load(_)


def obj_to_json(obj: Any, path: str) -> None:
    """python对象转换为json文件

    参数:
        obj: python对象
        path: json文件
    """
    with open(path, 'w', encoding='utf8') as _:
        json.dump(obj, _, ensure_ascii=False)


def yaml_to_obj(path: str) -> Any:
    """yaml文件转换为python对象


    参数:
        path: yaml文件

    返回值:
        Any: python对象
    """
    with open(path, 'r', encoding='utf8') as _:
        return yaml.load(_, Loader=yaml.FullLoader)


def obj_to_yaml(obj: Any, path: str) -> None:
    """python对象转换为yaml文件

    参数:
        obj: python对象
        path: yaml文件
    """
    with open(path, 'w', encoding='utf8') as _:
        yaml.dump(obj, _, allow_unicode=True)


def json_to_yaml(json_path: str, yaml_path: str) -> None:
    """json文件转换为yaml文件

    参数:
        json_path: json文件路径
        yaml_path: yaml文件路径
    """
    obj = json_to_obj(json_path)
    obj_to_yaml(obj, yaml_path)


def yaml_to_json(yaml_path: str, json_path: str) -> None:
    """yaml文件转换为json文件

    参数:
        yaml_path: yaml文件路径
        json_path: json文件路径
    """
    obj = json_to_obj(yaml_path)
    obj_to_json(obj, json_path)


def obj_to_json_str(obj: Any) -> str:
    """python对象转换为json格式字符串

    参数:
        obj: python对象

    返回值:
        str: json格式字符串
    """
    return json.dumps(obj, ensure_ascii=False)


def json_str_to_obj(json_str: str) -> Any:
    """json格式字符串转换为python对象

    参数:
        json_str: json格式字符串

    返回值:
        Any: python对象
    """
    if isinstance(json_str, str) or isinstance(json_str, bytes):
        return json.loads(json_str)
    return json_str


async def download_async(
        url: str,
        headers: Optional[dict] = None,
        stringify: bool = False
) -> Optional[Union[bytes, str]]:
    """异步下载

    参数:
        url: 下载url
        headers: 请求头
        stringify = False: 是否以字符串形式返回

    返回值:
        Optional[Union[bytes, str]]: 获取的数据
    """
    default_headers = {
        'User-Agent': UserAgent().chrome
    }
    hdrs = headers or default_headers
    async with ClientSession() as sess:
        async with sess.get(url, headers=hdrs) as resp:
            if resp.status == 200:
                if stringify:
                    return await resp.text()
                return await resp.read()
            return None


def render_jinja(
        root: str,
        template: str,
        args: Optional[dict] = None,
        options: Optional[dict] = None
) -> None:
    """渲染jinja模板

    参数:
        template_name: 模板名称
        args: 模板参数
    """
    venv = jinja2.Environment(loader=jinja2.FileSystemLoader(root))
    temp = venv.get_template(f'{template}.jinja')
    html = temp.render(args=args)
    with open(f'{root}/{template}.html', 'w', encoding='utf8') as _:
        _.write(html)
    default_options = {
        'width': 1020,
        "enable-local-file-access": None
    }
    with open(f'{root}/{template}.html', 'r', encoding='utf8') as _:
        imgkit.from_file(
            _,
            f'{root}/{template}.jpg',
            options=options or default_options
        )
    os.remove(f'{root}/{template}.html')


def untag(string: str) -> str:
    """消去标签

    参数:
        string: 含tag字符串

    返回值:
        str: 无tag字符串
    """
    tag_p = re.compile(r'<.*?>')
    for tag in re.findall(tag_p, string):
        string = string.replace(tag, '')
    return string


def to_html(string: str) -> str:
    """富文本转换为html

    参数:
        string: 富文本

    返回值:
        str: html
    """
    def _find_style(_tag: str, _rich_text_dict: dict) -> list:
        """找到tag对应的style

        参数:
            _tag: _tag
            _rich_text_dict: _rich_text_dict

        返回值:
            str: 对应的style
        """
        for _key, _val in _rich_text_dict.items():
            if _key in _tag:
                return _val.split('{0}')

    rich_text_dict = json_to_obj('data/rich_text_styles.json')
    tag_p = re.compile(r'<.*?>')
    stk_tag = []
    seq_tag = re.findall(tag_p, string)
    seq_str = re.split(tag_p, string)
    for i, cur_tag in enumerate(seq_tag):
        if cur_tag != '</>':
            stk_tag.append(i)
        else:
            _l, _r = stk_tag.pop(), i
            if seq_tag[_l][1] == '$':
                seq_tag[_l], seq_tag[_r] = '', ''
            else:
                seq_tag[_l], seq_tag[_r] = _find_style(seq_tag[_l], rich_text_dict)
    res = seq_str[0]
    for i, _ in enumerate(seq_tag):
        res += seq_tag[i] + seq_str[i + 1]
    return res


def bring_in_blackboard(args: dict) -> str:
    """将blackboard中的值带入description中

    参数:
        args: 含description和blackboard的字典

    返回值:
        str: 带入后的description
    """
    res = to_html(args['description'])
    _p = re.compile("{.*?}")
    for i in re.findall(_p, args['description']):
        for j in args['blackboard']:
            if j['key'].upper() in i.upper():
                if '%' in i:
                    res = res.replace(i, str(round(j['value'] * 100, 1)) + '%')
                else:
                    res = res.replace(i, str(j['value']))
    return res
