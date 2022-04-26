import argparse

import cv2
import os.path
import pygame as pg
import os
from screeninfo import get_monitors

from converter_settings import ConverterSettings
from picture_converter import convert_to_asciiart


def transform_picture_to_show(image_res):
    width = image_res.shape[1]
    height = image_res.shape[0]
    screen = get_monitors()[0]
    if width > height:
        coeff = width / height
        w = screen.width - 100 if screen.width < width else width
        h = w / coeff
    else:
        coeff = height / width
        h = screen.height - 100 if screen.height < height else height
        w = h / coeff
    screen_size = int(w), int(h)
    return cv2.resize(image_res, screen_size, interpolation=cv2.INTER_CUBIC)


def open_ansi(path: str):
    if os.name == 'nt':
        from ctypes import windll
        k = windll.kernel32
        k.SetConsoleMode(k.GetStdHandle(-11), 7)
    with open(path, 'r', encoding='utf8') as image:
        im = image.readlines()
        for i in im:
            print(i)


def argparse_init(ap):
    group = ap.add_mutually_exclusive_group()
    ap.add_argument('-o',
                    '--open',
                    required=False,
                    help='Открыть ansi art')
    ap.add_argument(
        '-i',
        '--image',
        required=False,
        help='Путь до исходного изображения',
        default='./images/example.jpg',
    )
    ap.add_argument(
        '-p',
        '--path',
        required=False,
        help='Путь до результата',
        default='./images/result_example.jpg',
    )
    group.add_argument(
        '--size',
        '-s',
        required=False,
        help='Установить размер результирующей картинки  в формате [width]:[height]'
    )
    group.add_argument(
        '-r',
        '--reset',
        required=False,
        action="store_true",
        help='Сбрасывает настройки к дефолтным'
    )


def save_image(image, path):
    try:
        cv2.imwrite(path, image)
    except:
        print(f"Не удалось сохранить файл по пути {path}")
        exit()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    argparse_init(ap)
    pg.init()
    args = ap.parse_args()
    if args.size:
        ConverterSettings().set_size(args.size)
    elif args.reset:
        ConverterSettings().reset_settings()
    elif args.open:
        open_ansi(args.open)
    else:
        if not os.path.exists(args.image):
            print(f'Файл {args.image} не существует')
            exit()
        image = cv2.imread(args.image)
        settings = ConverterSettings().settings
        font = pg.font.SysFont(settings['font'], settings['font size'], bold=True)
        size = settings['picture size']
        image_res = convert_to_asciiart(image, settings['ascii table'], settings['color level'], font,
                                        int(settings['font size']), tuple(settings['picture size']))
        save_image(image_res, args.path)
        cv2.imshow('after', transform_picture_to_show(image))
        cv2.imshow('before', transform_picture_to_show(image_res))
        cv2.waitKey(0)

# чб картинка
# .ansi возможность просматривать
