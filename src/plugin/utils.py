# encoding:utf-8
import aiohttp
from PIL import Image, ImageDraw
from fake_useragent import UserAgent


default_headers = {
    'User-Agent': UserAgent().chrome
}


async def download_async(url: str,
                         headers: dict = None,
                         stringify: bool = False) -> bytes or str:
    """一部下载

    Args:
        url (str): 下载链接
        headers (dict, optional): 请求头. Defaults to None.
        stringify (bool, optional): 是否返回字符串. Defaults to False.

    Returns:
        bytes or str: 下载内容
    """
    async with aiohttp.ClientSession() as sess:
        async with sess.get(url, headers=headers or default_headers) as resp:
            if resp.status == 200:
                if stringify:
                    return await resp.text()
                else:
                    return await resp.read()



async def get_qavatar(user_id: str,
                      spec: str = '5',
                      headers: dict = None) -> bytes:
    """获取用户头像

    Args:
        user_id (str): QQ号
        spec (str): 图像尺寸. Defaults to 5
        headers (dict, optional): 请求头. Defaults to None.

    Returns:
        bytes: 字节图像
    """
    url = 'http://q.qlogo.cn/g'
    async with aiohttp.ClientSession(headers=headers or default_headers) as sess:
        params = {
            'b':'qq',
            's':spec,
            'nk':user_id
        }
        async with sess.get(url, params=params) as resp:
            if resp.status == 200:
                return await resp.read()


def img_cut_circle(src,dest):
    # 读取图片
    src_img = Image.open(src).convert("RGBA")
    bg_img = Image.new('RGBA', src_img.size, color=(0,0,0,0))
    # 新建一个蒙板图, 注意必须是 RGBA 模式
    mask = Image.new('RGBA', src_img.size, color=(0,0,0,0))
    # 画一个圆
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0,0, src_img.size[0], src_img.size[1]), fill=(0,0,0,255))
    # box 为头像在 bg 中的位置
    # box(x1, y1, x2, y2)
    # x1,y1 为头像左上角的位置
    # x2,y2 为头像右下角的位置
    box = (0, 0, src_img.size[0], src_img.size[1])
    # 以下使用到paste(img, box=None, mask=None)方法
    #   img 为要粘贴的图片对你
    #   box 为图片 头像在 bg 中的位置
    #   mask 为蒙板，原理同 ps， 只显示 mask 中 Alpha 通道值大于等于1的部分
    bg_img.paste(src_img, box, mask)
    bg_img.save(dest)
