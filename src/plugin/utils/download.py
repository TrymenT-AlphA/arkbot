# encoding:utf-8

import aiohttp


default_headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) '
                  'AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'
}


async def download_async(url, headers=None, stringify=False):
    """
    异步下载
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers or default_headers) as response:
            if response.status == 200:
                if stringify:
                    return await response.text()
                else:
                    return await response.read()