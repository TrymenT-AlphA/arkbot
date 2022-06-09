# encoding:utf-8
from aiohttp import ClientSession
from PIL import Image, ImageDraw
from fake_useragent import UserAgent

default_headers = {
    'User-Agent': UserAgent().chrome
}


async def download_async(
    url: str,
    headers: dict = None,
    stringify: bool = False) -> bytes or str or None:
    """异步下载

    Args:
        url (str): 下载链接
        headers (dict, optional): 请求头. Defaults to None.
        stringify (bool, optional): 是否返回字符串. Defaults to False.

    Returns:
        bytes or str: 下载内容
    """
    async with ClientSession() as sess:
        async with sess.get(url, headers=headers or default_headers) as resp:
            if resp.status == 200:
                if stringify:
                    return await resp.text()
                else:
                    return await resp.read()
            else:
                return None



async def get_qavatar(
    user_id: str,
    spec: str = '5',
    headers: dict = None) -> bytes or None:
    """获取用户QQ头像

    Args:
        user_id (str): QQ号
        spec (str): 图像尺寸. Defaults to 5
            spec	px
            1	    40x40
            2	    40x40
            3	    100x100
            4	    140x140
            5	    640x640
            40	    40x40
            100	    100x100
        headers (dict, optional): 请求头. Defaults to None.

    Returns:
        bytes: 图像二进制数据
    """
    url = 'http://q.qlogo.cn/g'
    async with ClientSession(headers=headers or default_headers) as sess:
        params = {
            'b':'qq',
            's':spec,
            'nk':user_id
        }
        async with sess.get(url, params=params) as resp:
            if resp.status == 200:
                return await resp.read()
            else:
                return None


def img_cut_circle(
    src: str,
    dest: str) -> None:
    """将图像裁剪成圆形

    Args:
        src (str): 输入图像
        dest (str): 输出图像
    
    Returns:
        None: 无
    """
    src_img = Image.open(src).convert("RGBA")
    bg_img = Image.new('RGBA', src_img.size, color=(0,0,0,0))
    mask = Image.new('RGBA', src_img.size, color=(0,0,0,0))
    ImageDraw.Draw(mask).ellipse((0,0, *src_img.size), fill=(0,0,0,255))
    bg_img.paste(src_img, (0, 0, *src_img.size), mask)
    bg_img.save(dest)
