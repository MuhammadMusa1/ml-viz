"""Сверка: один нейрон на странице viz/neuron должен совпадать с sklearn.

Запуск:  pip install palmerpenguins scikit-learn
         python tools/check_neuron.py
Задача: «Это Chinstrap?». Входы — длина и глубина клюва после StandardScaler (обучен на train).
Нейрон: сумма = w1·x1 + w2·x2 + b, ответ «Chinstrap», если сумма > 0 (так решает и sklearn).
1) Точность для нескольких наборов весов, которые можно поставить ползунками на странице.
2) LogisticRegression (это тот же нейрон с сигмоидой): веса, смещение, точность на train и test —
   их показывает игра «Обыграй sklearn».
"""
import numpy as np
from palmerpenguins import load_penguins
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

df = load_penguins().drop(columns=['sex']).dropna().reset_index(drop=True)
X = df[['bill_length_mm', 'bill_depth_mm']]
y = df['species'] == 'Chinstrap'
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler().fit(X_train)
Z_train, Z_test = scaler.transform(X_train), scaler.transform(X_test)

print('Ручные веса (w1, w2, b): верных на train / test')
for w1, w2, b in [(1, 0, 0), (0, 0, 0), (1, 1, -1), (2, 1.5, -2), (-1, 0.5, 0.3)]:
    s_tr = Z_train @ [w1, w2] + b
    s_te = Z_test @ [w1, w2] + b
    print(f'  ({w1}, {w2}, {b}): {int(((s_tr > 0) == y_train).sum())}/{len(y_train)}'
          f'  {int(((s_te > 0) == y_test).sum())}/{len(y_test)}')

model = LogisticRegression().fit(Z_train, y_train)
w = model.coef_[0]
print(f'LogisticRegression: w1 = {w[0]:.2f}, w2 = {w[1]:.2f}, b = {model.intercept_[0]:.2f}')
print(f'  train {int((model.predict(Z_train) == y_train).sum())}/{len(y_train)}, '
      f'test {int((model.predict(Z_test) == y_test).sum())}/{len(y_test)}')
print(f'Ленивая модель (всегда «нет»): train {int((~y_train).sum())}/{len(y_train)}, '
      f'test {int((~y_test).sum())}/{len(y_test)}')
