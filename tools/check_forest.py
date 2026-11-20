"""Сверка: случайный лес на странице viz/forest должен совпадать с sklearn.

Запуск:  pip install palmerpenguins scikit-learn
         python tools/check_forest.py
Признаки — длина и глубина клюва. Выводит:
  * точность на test каждого из 100 деревьев (дерево №k на странице = model.estimators_[k-1]);
  * точность на test леса из N деревьев для N = 1..100 (ползунок «Деревьев в лесу»).
Страница строит те же деревья сама: повторяет генератор случайных чисел numpy и алгоритм sklearn.
"""
import numpy as np
from palmerpenguins import load_penguins
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

df = load_penguins().drop(columns=['sex']).dropna().reset_index(drop=True)
X = df[['bill_length_mm', 'bill_depth_mm']]
y = df['species']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

full = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_train, y_train)
y_test_idx = np.searchsorted(full.classes_, y_test)
per_tree = [int((t.predict(X_test.values) == y_test_idx).sum()) for t in full.estimators_]
print(f'Деревья по отдельности (из {len(y_test)}):')
for k in range(0, 100, 10):
    print('  №{:<3d}'.format(k + 1) + ' '.join(f'{c:3d}' for c in per_tree[k:k + 10]))
print(f'  от {min(per_tree)} до {max(per_tree)}, в среднем {np.mean(per_tree):.1f}')

print(f'Лес из N деревьев (из {len(y_test)}):')
row = []
for n in range(1, 101):
    # Лес из N деревьев с random_state=42 — это первые N деревьев большого леса
    m = RandomForestClassifier(n_estimators=n, random_state=42).fit(X_train, y_train)
    row.append(f'{n}:{int((m.predict(X_test) == y_test).sum())}')
    if n % 10 == 0:
        print('  ' + ' '.join(row)); row = []
