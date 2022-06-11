# encoding:utf-8
import numpy
from moviepy.editor import ImageSequenceClip as imageclip
from PIL import Image as IMG
from PIL import ImageOps

from .Singleton import Singleton


@Singleton
class PetPet:

    def __init__(self) -> None:
        self.frame_spec = [
            (27, 31, 86, 90),
            (22, 36, 91, 90),
            (18, 41, 95, 90),
            (22, 41, 91, 91),
            (27, 28, 86, 91)
        ]
        self.squish_factor = [
            (0, 0, 0, 0),
            (-7, 22, 8, 0),
            (-8, 30, 9, 6),
            (-3, 21, 5, 9),
            (0, 0, 0, 0)
        ]
        self.squish_translation_factor = [0, 20, 34, 21, 0]
        self.frames = tuple([f'data/petpet_frame{i}.png' for i in range(5)])

    def save_gif(self, gif_frames, dest, fps=10):
        clip = imageclip(gif_frames, fps=fps)
        clip.write_gif(dest)  # 使用 imageio
        clip.close()

    def make_frame(self, avatar, i, squish=0, flip=False):
        spec = list(self.frame_spec[i])
        for j, s in enumerate(spec):
            spec[j] = int(s + self.squish_factor[i][j] * squish)
        hand = IMG.open(self.frames[i]).convert('RGBA')
        if flip:
            avatar = ImageOps.mirror(avatar)
        avatar = avatar.resize(
            (int((spec[2] - spec[0]) * 1.2), int((spec[3] - spec[1]) * 1.2)), IMG.ANTIALIAS)
        gif_frame = IMG.new('RGB', (112, 112), (255, 255, 255))
        gif_frame.paste(avatar, (spec[0], spec[1]), avatar)
        gif_frame.paste(
            hand, (0, int(squish * self.squish_translation_factor[i])), hand)
        return numpy.array(gif_frame)

    def petpet(self, src, dest, flip=False, squish=0, fps=20) -> None:
        gif_frames = []
        avatar = IMG.open(src).convert('RGBA')
        for i in range(5):
            gif_frames.append(self.make_frame(avatar, i, squish=squish, flip=flip))
        self.save_gif(gif_frames, dest, fps=fps)
