"""Сверка: градиентный спуск на странице viz/gd должен совпадать с Python.

Запуск:  pip install palmerpenguins scikit-learn
         python tools/check_gd.py
Задача: «Это Gentoo?» по массе тела (после StandardScaler, обученного на train).
Нейрон с сигмоидой: p = 1 / (1 + e^(−(w·z + b))). Ошибка — средний log-loss на train (273 пингвина).
Спуск: w −= lr · mean((p − y)·z),  b −= lr · mean(p − y), старт w = −1, b = 3 (как на странице).
Выводит w, b и ошибку после 1, 5 и 20 шагов для каждого размера шага, число шагов до «дна»
(ошибка не больше минимума + 0.01, не больше 100 шагов — как в игре), и минимум из sklearn.
"""
import numpy as np
from palmerpenguins import load_penguins
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

df = load_penguins().drop(columns=['sex']).dropna().reset_index(drop=True)
X = df[['body_mass_g']]
y = (df['species'] == 'Gentoo').to_numpy(dtype=float)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler().fit(X_train)
z = scaler.transform(X_train)[:, 0]
z_test = scaler.transform(X_test)[:, 0]


def loss(w, b):
    t = w * z + b
    return np.mean(np.logaddexp(0, t) - y_train * t)   # log-loss без переполнения


sk = LogisticRegression(C=np.inf).fit(z[:, None], y_train)   # C = ∞ — без штрафа за большие веса
W, B = sk.coef_[0, 0], sk.intercept_[0]
L_MIN = loss(W, B)
print(f'Дно (sklearn): w = {W:.2f}, b = {B:.2f}, ошибка = {L_MIN:.3f}, '
      f'train {int(((W * z + B > 0) == y_train).sum())}/{len(z)}, '
      f'test {int(((W * z_test + B > 0) == y_test).sum())}/{len(z_test)}')
print(f'Старт w = -1, b = 3: ошибка {loss(-1, 3):.3f}')
print(f'Ленивая модель (всегда «нет»): train {int((y_train == 0).sum())}/{len(z)}, test {int((y_test == 0).sum())}/{len(z_test)}')

for lr in [0.1, 0.3, 1, 3, 10, 30, 60]:
    w, b, reached, marks = -1.0, 3.0, None, []
    for step in range(1, 101):
        p = 1 / (1 + np.exp(-(w * z + b)))
        w, b = w - lr * np.mean((p - y_train) * z), b - lr * np.mean(p - y_train)
        if step in (1, 5, 20):
            marks.append(f'{step}: w={w:.2f} b={b:.2f} L={loss(w, b):.3f}')
        if reached is None and loss(w, b) <= L_MIN + 0.01:
            reached = step
    print(f'lr {lr:>4}: до дна {reached if reached else "не дошёл за 100"} шагов | ' + ' | '.join(marks))
