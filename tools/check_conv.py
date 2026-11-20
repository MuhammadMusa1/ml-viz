"""Сверка: карта признаков на странице viz/convolution должна совпадать с numpy/scipy.

Запуск:  pip install numpy scipy
         python tools/check_conv.py
Картинки берутся из data/conv_shapes.js (те же, что на странице), фильтры 3×3 — те же, что в панели.
Свёртка «valid» без переворота фильтра (correlate2d) — так считают свёрточные слои PyTorch и Keras.
Для каждой картинки и фильтра выводит самый сильный и самый отрицательный отклик и его клетку
(строка, столбец с 1; при равенстве — первая слева-сверху), как в панели страницы,
и одну подробную клетку (строка 9, столбец 5), как в расчёте под графиком.
"""
import json
from pathlib import Path

import numpy as np
from scipy.signal import correlate2d

src = (Path(__file__).parent.parent / 'data' / 'conv_shapes.js').read_text(encoding='utf-8')
shapes = json.loads(src[src.index('{'):src.rindex('}') + 1])['shapes']

KERNELS = {
    'vertical':   np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=float),
    'horizontal': np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=float),
    'blur':       np.ones((3, 3)) / 9,
    'sharpen':    np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=float),
}


def fmt(v):
    v = round(v, 2) + 0.0          # без «-0.0»
    return f'{v:.2f}'.rstrip('0').rstrip('.')


for sh in shapes:
    img = np.array([[1.0 if ch == '#' else 0.0 for ch in row] for row in sh['rows']])
    for name, k in KERNELS.items():
        out = np.round(correlate2d(img, k, mode='valid'), 9)   # 14×14 → 12×12
        r1, c1 = np.unravel_index(np.argmax(out), out.shape)
        r2, c2 = np.unravel_index(np.argmin(out), out.shape)
        print(f'{sh["id"]:6s} {name:10s} max {fmt(out[r1, c1])} ({r1 + 1},{c1 + 1})  '
              f'min {fmt(out[r2, c2])} ({r2 + 1},{c2 + 1})  клетка (9,5) = {fmt(out[8, 4])}')
