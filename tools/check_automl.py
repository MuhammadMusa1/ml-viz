"""Сверка: рейтинг мини-AutoML на странице viz/automl (урок 19) должен совпадать с sklearn.

Запуск:  pip install palmerpenguins scikit-learn
         python tools/check_automl.py

AutoML здесь — перебор моделей и настроек по кросс-валидации на train (cross_val_score, cv=5), как в главе 19:
  * пары признаков: длина + глубина клюва (01), длина клюва + крыло (02);
  * KNN в Pipeline со StandardScaler, K = 1, 3, 5, 11, 15; дерево решений, max_depth = 1, 2, 3.
Для каждой настройки печатает среднюю точность по 5 проверкам и число верных на test. Рейтинг — по убыванию
средней точности, округлённой до 0.1% (при равенстве — порядок перебора). Те же настройки сверяет tools/check_project.py (урок 12).

Режим «утечка»: к длине клюва добавлен столбец «номер вида в базе» — это сам ответ, записанный числом.
Печатает тот же рейтинг и проверяет «на прочность» (algorithm у KNN, random_state у дерева).
"""
import numpy as np
from palmerpenguins import load_penguins
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

df = load_penguins().drop(columns=['sex']).dropna().reset_index(drop=True)
df['species_code'] = df['species'].map({'Adelie': 0, 'Chinstrap': 1, 'Gentoo': 2})   # утечка: ответ числом
y = df['species']
idx_train, idx_test = train_test_split(df.index, test_size=0.2, random_state=42)
y_train, y_test = y[idx_train], y[idx_test]

PAIRS = {'01': ['bill_length_mm', 'bill_depth_mm'], '02': ['bill_length_mm', 'flipper_length_mm'],
         'leak': ['bill_length_mm', 'species_code']}


def candidates(pair):
    out = [(f'{pair} knn{k}', lambda k=k, alg='auto': make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k, algorithm=alg)))
           for k in (1, 3, 5, 11, 15)]
    out += [(f'{pair} tree{d}', lambda d=d, rs=42: DecisionTreeClassifier(max_depth=d, random_state=rs)) for d in (1, 2, 3)]
    return out


def evaluate(make, cols):
    Xtr, Xte = df.loc[idx_train, cols], df.loc[idx_test, cols]
    cv = cross_val_score(make(), Xtr, y_train, cv=5).mean()
    t = int((make().fit(Xtr, y_train).predict(Xte) == y_test).sum())
    return cv, t


def board(pairs):
    rows = []
    for pair in pairs:
        for name, make in candidates(pair):
            cv, t = evaluate(make, PAIRS[pair])
            rows.append((name, cv, t))
    # Рейтинг: по средней точности, округлённой до 0.1% (как на странице); при равенстве — порядок перебора.
    # Без округления порядок равных моделей решали бы доли процента, которые JS и numpy считают чуть по-разному.
    rows.sort(key=lambda r: -round(100 * r[1], 1))
    for i, (name, cv, t) in enumerate(rows, 1):
        print(f'  {i:2d}. {name:10s} CV {100 * cv:.1f}%  test {t}')


print('Обычный AutoML (16 настроек):')
board(['01', '02'])
print('С утечкой (длина клюва + номер вида):')
board(['leak'])

unstable = []
for name, make in candidates('leak'):
    res = set()
    variants = [{'alg': a} for a in ('brute', 'kd_tree', 'ball_tree')] if 'knn' in name else [{'rs': r} for r in range(10)]
    for v in variants:
        m = lambda: make(**v)
        res.add(evaluate(m, PAIRS['leak']))
    if len(res) > 1:
        unstable.append(name)
print('Неустойчивые настройки с утечкой:', unstable or 'нет')
