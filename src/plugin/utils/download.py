# encoding:utf-8
import aiohttp
from fake_useragent import UserAgent


default_headers = {
    'User-Agent': UserAgent().chrome
}


async def download_async(url,
                         headers: dict = None,
                         stringify: bool = False) -> None:
    """
    异步下载
    """
    async with aiohttp.ClientSession() as sess:
        async with sess.get(url, headers=headers or default_headers) as resp:
            if resp.status == 200:
                if stringify:
                    return await resp.text()
                else:
                    return await resp.read()
