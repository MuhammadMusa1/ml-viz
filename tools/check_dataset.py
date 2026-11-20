"""Сверка: цифры на странице viz/dataset должны совпадать с pandas.

Запуск:  pip install palmerpenguins pandas
         python tools/check_dataset.py
Показывает то же, что панель страницы: размер таблицы, сколько каких видов и островов,
минимум, максимум и среднее для числовых столбцов, первые строки и размеры X и y.
Столбец year (год измерения) на странице не показан — для задач курса он не нужен.
"""
from palmerpenguins import load_penguins

raw = load_penguins()
print(f'Исходная таблица: {raw.shape[0]} строк × {raw.shape[1]} столбцов')
df = raw.drop(columns=['sex']).dropna().reset_index(drop=True)
print(f'После drop(sex) и dropna: {df.shape[0]} строк × {df.shape[1]} столбцов')
print(df.head(3).to_string())
for col in ['species', 'island']:
    print(col, dict(df[col].value_counts().sort_index()))
for col in ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']:
    s = df[col]
    print(f'{col}: min {s.min():g}, max {s.max():g}, mean {s.mean():.1f}')
X, y = df.drop(columns=['species', 'year']), df['species']   # год измерения на странице не показываем
print(f'X: {X.shape}, y: {y.shape}')
