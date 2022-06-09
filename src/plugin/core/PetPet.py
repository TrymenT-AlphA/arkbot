# encoding:utf-8
from PIL import Image as IMG
from PIL import ImageOps
from moviepy.editor import ImageSequenceClip as imageclip
import numpy


class PetPet:
    """
    PetPet类
    """
    frame_spec = [
        (27, 31, 86, 90),
        (22, 36, 91, 90),
        (18, 41, 95, 90),
        (22, 41, 91, 91),
        (27, 28, 86, 91)
    ]
    squish_factor = [
        (0, 0, 0, 0),
        (-7, 22, 8, 0),
        (-8, 30, 9, 6),
        (-3, 21, 5, 9),
        (0, 0, 0, 0)
    ]
    squish_translation_factor = [0, 20, 34, 21, 0]
    frames = tuple([f'data/petpet/frame{i}.png' for i in range(5)])

    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    @classmethod
    def save_gif(cls, gif_frames, dest, fps=10):
        clip = imageclip(gif_frames, fps=fps)
        clip.write_gif(dest)  # 使用 imageio
        clip.close()

    @classmethod
    def make_frame(cls, avatar, i, squish=0, flip=False):
        # 读入位置
        spec = list(cls.frame_spec[i])
        # 将位置添加偏移量
        for j, s in enumerate(spec):
            spec[j] = int(s + cls.squish_factor[i][j] * squish)
        # 读取手
        hand = IMG.open(cls.frames[i]).convert('RGBA')
        # 反转
        if flip:
            avatar = ImageOps.mirror(avatar)
        # 将头像放缩成所需大小
        avatar = avatar.resize(
            (int((spec[2] - spec[0]) * 1.2), int((spec[3] - spec[1]) * 1.2)), IMG.ANTIALIAS)
        # 并贴到空图像上
        gif_frame = IMG.new('RGB', (112, 112), (255, 255, 255))
        gif_frame.paste(avatar, (spec[0], spec[1]), avatar)
        # 将手覆盖（包括偏移量）
        gif_frame.paste(
            hand, (0, int(squish * cls.squish_translation_factor[i])), hand)
        # 返回
        return numpy.array(gif_frame)

    @classmethod
    def petpet(cls, src, dest, flip=False, squish=0, fps=20) -> None:
        gif_frames = []
        # 打开头像
        avatar = IMG.open(src).convert('RGBA')
        # 生成每一帧
        for i in range(5):
            gif_frames.append(cls.make_frame(avatar, i, squish=squish, flip=flip))
        # 输出
        cls.save_gif(gif_frames, dest, fps=fps)
