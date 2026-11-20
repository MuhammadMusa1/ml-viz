"""Сверка: числа на странице viz/outliers должны совпадать с pandas.

Запуск:  pip install palmerpenguins pandas
         python tools/check_outliers.py
1) Выбросы: для каждого числового признака (342 пингвина) — среднее, медиана, квартили Q1 и Q3,
   границы «усов» Q1 − 1.5·IQR и Q3 + 1.5·IQR и сколько точек за ними. То же — с одним «великаном»
   (опечатка: значение первого пингвина × 10), как переключатель на странице,
   и для «маленькой группы» — первых 10 пингвинов.
2) Пропуски: сколько NaN в каждом столбце исходной таблицы и что дают три способа их обработать.
"""
import pandas as pd
from palmerpenguins import load_penguins

raw = load_penguins().drop(columns=['year'])
df = raw.drop(columns=['sex']).dropna().reset_index(drop=True)
cols = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']


def describe(s):
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    lo, hi = q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1)
    out = int(((s < lo) | (s > hi)).sum())
    return f'mean {s.mean():.1f}, median {s.median():g}, Q1 {q1:g}, Q3 {q3:g}, усы [{lo:g}; {hi:g}], выбросов {out}'


for c in cols:
    s = df[c]
    print(f'{c}: {describe(s)}')
    giant = pd.concat([s, pd.Series([s.iloc[0] * 10])], ignore_index=True)
    print(f'   + великан {s.iloc[0] * 10:g}: {describe(giant)}')
    h = s.head(10)   # «маленькая группа» на странице — первые 10 пингвинов таблицы
    hg = pd.concat([h, pd.Series([s.iloc[0] * 10])], ignore_index=True)
    print(f'   первые 10: mean {h.mean():.1f}, median {h.median():g} | + великан: mean {hg.mean():.1f}, median {hg.median():g}')

print('Пропуски:', dict(raw.isna().sum()))
print('Строк с хотя бы одним пропуском:', int(raw.isna().any(axis=1).sum()))
print('1) dropna():', raw.dropna().shape)
print('2) drop(sex).dropna():', raw.drop(columns=['sex']).dropna().shape)
filled = raw.copy()
for c in cols:
    filled[c] = filled[c].fillna(filled[c].mean())
filled['sex'] = filled['sex'].fillna(filled['sex'].mode()[0])
print('3) fillna (числа — средним, sex — самым частым):', filled.shape,
      f"среднее длины клюва {filled['bill_length_mm'].mean():.2f}, sex заполнен значением {raw['sex'].mode()[0]}")
