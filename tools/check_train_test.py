"""Сверка: точность на train и test на странице viz/train-test должна совпадать с sklearn.

Запуск:  pip install palmerpenguins scikit-learn
         python tools/check_train_test.py
Выводит число правильных ответов на train (из 273), validation (из 69) и test (из 69) для K = 1..50.
Признаки — длина клюва и масса тела, StandardScaler обучается только на той части, где учится модель.
Те же числа показывает страница (большие числа в панели и три линии на графике),
а в конце — лучшее K по validation (как в игре «Выбери K честно») и «ленивая» модель для сравнения.
"""
from palmerpenguins import load_penguins
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

df = load_penguins().drop(columns=['sex']).dropna().reset_index(drop=True)
X = df[['bill_length_mm', 'body_mass_g']]
y = df['species']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Пробный экзамен: train ещё раз делим на учёбу и validation (как на странице)
X_tr, X_val, y_tr, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=42)

val_correct = {}
print(f'  K  train/{len(y_train)}  validation/{len(y_val)}  test/{len(y_test)}')
for k in range(1, 51):
    model = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k))
    model.fit(X_train, y_train)
    tr = int((model.predict(X_train) == y_train).sum())
    te = int((model.predict(X_test) == y_test).sum())
    small = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k)).fit(X_tr, y_tr)
    va = int((small.predict(X_val) == y_val).sum())
    val_correct[k] = va
    print(f' {k:2d}  {tr:9d}  {va:14d}  {te:7d}')

best_k = max(val_correct, key=val_correct.get)   # при равенстве — меньшее K, как на странице
print(f'Лучшее K по validation: {best_k} ({val_correct[best_k]}/{len(y_val)})')
print(f'Ленивая модель (всегда самый частый вид train): '
      f'{int((y_test == y_train.mode()[0]).sum())}/{len(y_test)} на test')
