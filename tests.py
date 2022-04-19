import unittest

import pygame as pg
import cv2
import numpy as np
from fluentcheck import Is

import palette_creator
import picture_converter


class PaletteCreatorCase(unittest.TestCase):
    def test_get_palette_should_contains_all_symbols(self):
        pg.init()
        font = pg.font.SysFont('arial', 5)
        pal, coeff = palette_creator.get_color_palette('123', 3, font)
        Is(pal).dict.has_keys(*['1', '2', '3'])

    def test_get_palette_should_contains_expected_count_color(self):
        pg.init()
        font = pg.font.SysFont('arial', 5)
        pal, coeff = palette_creator.get_color_palette('123', 3, font)
        for i in pal.values():
            self.assertEqual(27, len(i))


class PictureConverterCase(unittest.TestCase):
    def setUp(self) -> None:
        pg.init()
        self.font = pg.font.SysFont('arial', 5)
        self.test_image = []
        for x in range(800):
            self.test_image.append([])
            for y in range(500):
                for p in range(3):
                    self.test_image[x].append([])
                    self.test_image[x][y].append([1, 2, 3])
        self.test_image = np.array(self.test_image)

    def test_convert_should_be_expected_size(self):
        res = picture_converter.convert_to_asciiart(cv2.imread('./images/example.jpg'), ' 211654561984562', 3, self.font, 1, (50, 50))
        self.assertEqual((res.shape[1], res.shape[0]), (50, 50))


if __name__ == '__main__':
    unittest.main()
