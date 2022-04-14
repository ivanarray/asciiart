import argparse

import cv2
import numpy as np
import pygame as pg
from screeninfo import get_monitors


class ImageConverter:
    def __init__(
            self,
            source_path: str,
            save_path: str,
            font_size: int = 4,
            color_lvl: int = 8,
    ):
        pg.init()
        self.save_path = save_path
        self.font_size = font_size
        self.color_level = color_lvl
        self.picture = cv2.imread(source_path)
        self.gray_picture = cv2.cvtColor(self.picture, cv2.COLOR_BGR2GRAY)
        self.width = self.picture.shape[1]
        self.height = self.picture.shape[0]
        self.font = pg.font.SysFont('arial', font_size, bold=True)
        self.char_space = int(self.font_size * 0.6)
        self.ascii_table = ' `.itfxzahao*#MW&8%B@$'
        self.renderer_ascii, self.color_coeff = self.get_palette()
        self.ascii_coeff = 255 // (len(self.ascii_table) - 1)
        self.gray_picture = cv2.transpose(self.gray_picture)
        self.picture = cv2.transpose(self.picture)

    def get_palette(self):
        colors, color_coeff = np.linspace(0, 255, num=self.color_level, dtype=int, retstep=True)
        color_palette = [np.array([r, g, b]) for r in colors for g in colors for b in colors]
        palette = dict.fromkeys(self.ascii_table, None)
        color_coeff = int(color_coeff)
        for char in palette:
            char_palette = {}
            for color in color_palette:
                color_key = tuple(color // color_coeff)
                char_palette[color_key] = self.font.render(char, False, tuple(color))
            palette[char] = char_palette
        return palette, color_coeff

    def convert(self):
        color_indices = self.picture // self.color_coeff
        ascii_indices = self.gray_picture // self.ascii_coeff
        screen = pg.Surface((self.width, self.height))
        screen.fill("black")
        for x in range(0, self.width, self.char_space):
            for y in range(0, self.height, self.char_space):
                char_index = ascii_indices[x, y]
                if char_index:
                    char = self.ascii_table[char_index]
                    color = tuple(color_indices[x, y])
                    screen.blit(self.renderer_ascii[char][color], (x, y))
        self.save_picture_and_show(screen)

    def save_picture_and_show(self, screen):
        image_to_save = pg.surfarray.array3d(screen)
        image_to_save = cv2.transpose(image_to_save)
        cv2.imwrite(self.save_path, image_to_save)
        pictures_to_show = self.get_picture_to_show(image_to_save)
        cv2.imshow("after", pictures_to_show[0])
        cv2.imshow("before", pictures_to_show[1])
        cv2.waitKey(0)

    def get_picture_to_show(self, image):
        screen = get_monitors()[0]
        if self.width > self.height:
            coeff = self.width / self.height
            w = screen.width - 100 if screen.width < self.width else self.width
            h = w / coeff
        else:
            coeff = self.height / self.width
            h = screen.height - 100 if screen.height < self.height else self.height
            w = h / coeff
        screen_size = int(w), int(h)
        return cv2.resize(image, screen_size, interpolation=cv2.INTER_CUBIC), \
               cv2.resize(cv2.transpose(self.picture), screen_size, interpolation=cv2.INTER_CUBIC)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()

    ap.add_argument(
        "-s",
        "--source",
        required=False,
        help="Путь до исходного изображения",
        default="./images/example.jpg",
    )

    ap.add_argument(
        "-p",
        "--path",
        required=False,
        help="Путь до результата",
        default="./images/result_example.jpg",
    )
    args = ap.parse_args()
    converter = ImageConverter(args.source, args.path)
    converter.convert()
