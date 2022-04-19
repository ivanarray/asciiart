import cv2
import pygame as pg
import pygame.font

from palette_creator import get_color_palette


def convert_to_asciiart(picture, symbols: str,
                        color_level: int,
                        font: pygame.font.Font, space: int,
                        result_size: tuple = None):
    width = picture.shape[1]
    height = picture.shape[0]
    if not len(result_size):
        result_size = (width, height)

    gray_coeff = len(symbols)
    palette, color_coeff = get_color_palette(symbols, color_level, font)
    gray_indexes = cv2.transpose(cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY) // gray_coeff)
    color_indexes = cv2.transpose(picture // color_coeff)
    surface = pg.Surface((width, height))
    surface.fill('black')
    for x in range(0, width, space):
        for y in range(0, height, space):
            symbol_index = gray_indexes[x, y]
            if symbol_index:
                color = color_indexes[x, y]
                symbol = symbols[symbol_index]
                surface.blit(palette[symbol][tuple(color)], (x, y))

    return cv2.resize(cv2.transpose(pg.surfarray.array3d(surface)), result_size)
