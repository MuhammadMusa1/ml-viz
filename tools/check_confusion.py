"""Сверка: матрица ошибок на странице viz/confusion должна совпадать с sklearn.

Запуск:  pip install palmerpenguins scikit-learn
         python tools/check_confusion.py
Задача: «Это Chinstrap?» (да / нет). Признаки — глубина клюва, длина крыла и масса,
StandardScaler + KNN с 10 соседями. Порог t: тревога, если хотя бы t соседей из 10 — Chinstrap
(то же, что predict_proba(X)[:, 1] >= t / 10). Обычный model.predict() — это t = 6 (больше половины).
Для каждого t выводится матрица (TN FP / FN TP) на test (модель учится на 273 train)
и на validation (модель учится на 204), как в игре «Настрой тревогу».
"""
import numpy as np
from palmerpenguins import load_penguins
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

K = 10
df = load_penguins().drop(columns=['sex']).dropna().reset_index(drop=True)
X = df[['bill_depth_mm', 'flipper_length_mm', 'body_mass_g']]
y = (df['species'] == 'Chinstrap').astype(int)          # 1 = Chinstrap
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_tr, X_val, y_tr, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=42)

full = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=K)).fit(X_train, y_train)
small = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=K)).fit(X_tr, y_tr)
# Число соседей-Chinstrap из 10 (доля * 10, округляем, чтобы не мешали дроби)
votes_test = np.rint(full.predict_proba(X_test)[:, 1] * K).astype(int)
votes_val = np.rint(small.predict_proba(X_val)[:, 1] * K).astype(int)


def report(name, votes, truth, t):
    pred = (votes >= t).astype(int)
    tn, fp, fn, tp = confusion_matrix(truth, pred, labels=[0, 1]).ravel()
    acc = (tp + tn) / len(truth)
    prec = f'{tp / (tp + fp):.0%}' if tp + fp else '—'
    rec = tp / (tp + fn)
    print(f'  {name:4s} TN {tn:2d} FP {fp:2d} FN {fn:2d} TP {tp:2d} | '
          f'accuracy {acc:.0%} precision {prec:>4s} recall {rec:.0%}')
    return tn, fp, fn, tp


print(f'Chinstrap: в test {y_test.sum()} из {len(y_test)}, в validation {y_val.sum()} из {len(y_val)}')
val = {}
for t in range(1, K + 1):
    print(f't = {t}')
    report('test', votes_test, y_test, t)
    val[t] = report('val', votes_val, y_val, t)

assert (full.predict(X_test) == (votes_test >= 6)).all(), 'predict() должен совпасть с t = 6'
lazy = np.zeros(len(y_test), dtype=int)
print('Ленивая модель (всегда «не Chinstrap»):', confusion_matrix(y_test, lazy).ravel(),
      f'accuracy {(lazy == y_test).mean():.0%}')

# Игра: лучшие пороги на validation (при равенстве — меньший t, как на странице)
need = int(np.ceil(0.9 * y_val.sum()))
a = min((t for t in val if val[t][3] >= need), key=lambda t: (val[t][1], t))
b = max((t for t in val if val[t][1] <= 5), key=lambda t: (val[t][3], -t))
print(f'Задание 1 (recall >= 90%, меньше ложных тревог): t = {a}')
print(f'Задание 2 (не больше 5 ложных тревог, больше найденных): t = {b}')
