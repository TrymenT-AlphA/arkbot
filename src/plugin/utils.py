# encoding:utf-8
from typing import Any

import yaml
import json
from aiohttp import ClientSession
from fake_useragent import UserAgent


default_headers = {
    'User-Agent': UserAgent().chrome
}


def load_yaml(path: str) -> Any:
    with open(path, 'r', encoding='utf8') as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def dump_yaml(obj: Any, path: str) -> None:
    with open(path, 'w', encoding='utf8') as f:
        yaml.dump(obj, f, allow_unicode=True)


def load_json(path: str) -> Any:
    with open(path, 'r', encoding='utf8') as f:
        return json.load(f)


def dump_json(obj: Any, path: str) -> None:
    with open(path, 'w', encoding='utf8') as f:
        json.dump(obj, f, ensure_ascii=False)


def dumps_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False)


def loads_json(json_str: str) -> Any:
    return json.loads(json_str)


async def download_async(url: str, headers: dict = None, stringify: bool = False) -> bytes or str or None:
    async with ClientSession() as sess:
        async with sess.get(url, headers=headers or default_headers) as resp:
            if resp.status == 200:
                if stringify:
                    return await resp.text()
                else:
                    return await resp.read()
            else:
                return None
