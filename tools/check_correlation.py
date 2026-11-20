"""Сверка: коэффициенты корреляции на странице viz/correlation должны совпадать с pandas.

Запуск:  pip install palmerpenguins pandas
         python tools/check_correlation.py
Выводит матрицу корреляций Пирсона (df.corr()) для четырёх числовых признаков — её показывает
таблица на странице, — и r для каждой пары отдельно по видам (переключатель «по видам»).
"""
from palmerpenguins import load_penguins

df = load_penguins().drop(columns=['sex']).dropna().reset_index(drop=True)
cols = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']
print(df[cols].corr().round(2).to_string())
for i, a in enumerate(cols):
    for b in cols[i + 1:]:
        per = ', '.join(f'{sp} {g[a].corr(g[b]):.2f}' for sp, g in df.groupby('species'))
        print(f'{a} × {b}: все {df[a].corr(df[b]):.2f} | {per}')
