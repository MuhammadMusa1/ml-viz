"""Пересобирает data/penguins.js из пакета palmerpenguins.

Запуск:  pip install palmerpenguins scikit-learn
         python tools/export_penguins.py
"""
import json
from pathlib import Path

from palmerpenguins import load_penguins
from sklearn.model_selection import train_test_split

df = load_penguins().drop(columns=['sex']).dropna().reset_index(drop=True)
idx_train, idx_test = train_test_split(df.index, test_size=0.2, random_state=42)
pos = {i: n for n, i in enumerate(idx_train)}
pos.update({i: n for n, i in enumerate(idx_test)})
test = set(idx_test)
# Честный подбор параметров: train ещё раз делим на «учёбу» и проверочную часть (validation), как в Colab:
# X_tr, X_val, y_tr, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=42)
idx_tr, idx_val = train_test_split(idx_train, test_size=0.25, random_state=42)
vpos = {i: n for n, i in enumerate(idx_tr)}
vpos.update({i: n for n, i in enumerate(idx_val)})
val = set(idx_val)

rows = [
    [r.species, r.island, r.bill_length_mm, r.bill_depth_mm,
     int(r.flipper_length_mm), int(r.body_mass_g), 1 if i in test else 0, pos[i],
     1 if i in val else 0, vpos.get(i, -1)]
    for i, r in zip(df.index, df.itertuples())
]

js = f'''// Palmer Penguins (Horst, Hill, Gorman, 2020), CC0.
// Стандарт курса: load_penguins().drop(columns=["sex"]).dropna().reset_index(drop=True) -> {len(df)} строки.
// is_test   = разбиение train_test_split(df.index, test_size=0.2, random_state=42)
// split_pos = позиция строки внутри X_train / X_test после этого разбиения.
//             Сортируя по ней, получаем тот же порядок, что в sklearn, и те же ответы при ничьих.
// is_val    = train ещё раз поделён: train_test_split(X_train, test_size=0.25, random_state=42) -> 204 «учёба» + 69 validation
// val_pos   = позиция внутри X_tr / X_val (у test-строк -1)
// Подключается через <script>, а не fetch(), чтобы работало офлайн с file://
window.PENGUINS = {{
  columns: ["species","island","bill_length_mm","bill_depth_mm","flipper_length_mm","body_mass_g","is_test","split_pos","is_val","val_pos"],
  rows: {json.dumps(rows, separators=(',', ':'))}
}};
'''
out = Path(__file__).resolve().parent.parent / 'data' / 'penguins.js'
out.write_text(js, encoding='utf-8')
print(f'Записано {len(rows)} строк в {out}')
