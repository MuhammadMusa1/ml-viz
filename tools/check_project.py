"""Сверка: страница viz/project (урок 12, мини-проект «Предсказатель») должна совпадать с sklearn.

Запуск:  pip install palmerpenguins scikit-learn
         python tools/check_project.py

Проект: вид пингвина по двум признакам. Для каждой пары признаков печатает число верных ответов
в каждой из 5 проверок кросс-валидации на train — cross_val_score(model, X_train, y_train, cv=5),
то есть StratifiedKFold(5) без перемешивания — и на test (модель учится на всём train):
  * baseline — DummyClassifier(strategy='most_frequent');
  * KNN в Pipeline со StandardScaler, K = 1..15;
  * дерево решений, max_depth = 1..6, random_state=42.
Те же числа показывает страница. В конце — проверка «на прочность»: настройки, где sklearn отвечает
по-разному при другом algorithm у KNN или другом random_state у дерева (ничьи), страница не показывает.
"""
from itertools import combinations

import numpy as np
from palmerpenguins import load_penguins
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

FEATURES = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']
df = load_penguins().drop(columns=['sex']).dropna().reset_index(drop=True)
y = df['species']
idx_train, idx_test = train_test_split(df.index, test_size=0.2, random_state=42)
y_train, y_test = y[idx_train], y[idx_test]
skf = StratifiedKFold(n_splits=5)
folds = [len(v) for _, v in skf.split(np.zeros(len(y_train)), y_train)]
print('Проверки (размер validation):', folds)


def fold_counts(model, X_train):
    out = []
    for tr, va in skf.split(X_train, y_train):
        model.fit(X_train.iloc[tr], y_train.iloc[tr])
        out.append(int((model.predict(X_train.iloc[va]) == y_train.iloc[va]).sum()))
    return out


def line(name, model, X_train, X_test):
    f = fold_counts(model, X_train)
    # Совпадает ли наш подсчёт с cross_val_score (на всякий случай)
    acc = cross_val_score(model, X_train, y_train, cv=5)
    assert np.allclose(acc, np.array(f) / np.array(folds))
    model.fit(X_train, y_train)
    t = int((model.predict(X_test) == y_test).sum())
    print(f'  {name:7s} ' + ' '.join(f'{v:2d}' for v in f) + f' | test {t}')


unstable = []
for a, b in combinations(range(4), 2):
    cols = [FEATURES[a], FEATURES[b]]
    X_train, X_test = df.loc[idx_train, cols], df.loc[idx_test, cols]
    print(f'{a}{b} {cols[0]} + {cols[1]}')
    line('base', DummyClassifier(strategy='most_frequent'), X_train, X_test)
    for k in range(1, 16):
        line(f'knn{k}', make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k)), X_train, X_test)
        res = set()
        for alg in ('brute', 'kd_tree', 'ball_tree'):
            m = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k, algorithm=alg))
            f = fold_counts(m, X_train)
            m.fit(X_train, y_train)
            res.add((tuple(f), tuple(m.predict(X_test))))
        if len(res) > 1:
            unstable.append(f'{a}{b} knn{k}')
    for d in range(1, 7):
        line(f'tree{d}', DecisionTreeClassifier(max_depth=d, random_state=42), X_train, X_test)
        res = set()
        for rs in range(10):
            m = DecisionTreeClassifier(max_depth=d, random_state=rs)
            f = fold_counts(m, X_train)
            m.fit(X_train, y_train)
            res.add((tuple(f), tuple(m.predict(X_test))))
        if len(res) > 1:
            unstable.append(f'{a}{b} tree{d}')
print('Неустойчивые настройки (ничьи):', unstable or 'нет')

# Страница предлагает только устойчивые настройки: пары 01 и 02, K = 1, 3, 5, 11, 15, глубина 1–3
OFFERED = [f'{p} knn{k}' for p in ('01', '02') for k in (1, 3, 5, 11, 15)] + \
          [f'{p} tree{d}' for p in ('01', '02') for d in (1, 2, 3)]
bad = [c for c in OFFERED if c in unstable]
assert not bad, f'на странице есть настройки с ничьими: {bad}'
print('Все настройки страницы устойчивы:', len(OFFERED))
