"""Выгружает ИСХОДНУЮ таблицу Palmer Penguins (344 строки, с пропусками) в data/penguins_raw.js.

Нужна странице «Выбросы и пропуски» (урок 4): там пропуски показываются как есть.
Запуск:  pip install palmerpenguins pandas
         python tools/export_penguins_raw.py
Пропуск (NaN) записывается как null. Столбец year не нужен и не выгружается.
"""
import json
import math
from pathlib import Path

from palmerpenguins import load_penguins

df = load_penguins()
cols = ['species', 'island', 'bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g', 'sex']
rows = []
for rec in df[cols].itertuples(index=False):
    row = []
    for v in rec:
        if isinstance(v, float) and math.isnan(v):
            row.append(None)
        elif isinstance(v, float) and v.is_integer():
            row.append(int(v))
        else:
            row.append(v if not isinstance(v, float) else round(v, 1))
    rows.append(row)
out = Path(__file__).parent.parent / 'data' / 'penguins_raw.js'
out.write_text(
    '/* Исходная таблица Palmer Penguins: 344 строки, пропуски = null. Создано tools/export_penguins_raw.py. */\n'
    'window.PENGUINS_RAW = ' + json.dumps({'columns': cols, 'rows': rows}, ensure_ascii=False) + ';\n',
    encoding='utf-8', newline='\n')
print(len(rows), 'строк записано в', out.name)
