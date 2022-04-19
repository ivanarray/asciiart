import numpy as np
import pygame as pg

"""Заранее рендерим строки во всевозможных цветах, для оптимизации
   Parameters: letter_to_render - список строк
               color_level - количество значений в каждом из каналов RGB
               font - шрифт в котором рендерим
   Returns: (dict[str, dict[np.ndarray, pg.Surface]], int)
   """


def get_color_palette(letters_to_render: str, color_level: int, font: pg.font.Font) -> \
        (dict[str, dict[np.ndarray, pg.Surface]], int):
    channel_vals, color_coeff = np.linspace(0, 255, num=color_level, dtype=int, retstep=True)
    color_coeff = int(color_coeff)
    colors = [np.array([r, g, b]) for r in channel_vals for g in channel_vals for b in channel_vals]
    palette = dict.fromkeys(letters_to_render, None)
    for let in palette:
        palette[let] = {}
        for ar in colors:
            key = tuple(ar // color_coeff)
            palette[let][key] = font.render(let, False, ar)
    return palette, color_coeff
