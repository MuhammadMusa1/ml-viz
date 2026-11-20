"""Сверка: точность KNN на сайте (viz/knn) должна совпадать с sklearn.

Запуск:  pip install palmerpenguins scikit-learn
         python tools/check_knn.py
Выводит точность (из 69 тестовых пингвинов) для K = 1..25 без масштаба и с StandardScaler.
Те же числа должна показывать панель «Точность на новых пингвинах» на странице KNN.
"""
from palmerpenguins import load_penguins
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

df = load_penguins().drop(columns=['sex']).dropna().reset_index(drop=True)
X = df[['bill_length_mm', 'bill_depth_mm']]
y = df['species']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

for scaled in (False, True):
    print('С масштабом' if scaled else 'Без масштаба')
    for k in range(1, 26):
        model = KNeighborsClassifier(n_neighbors=k)
        if scaled:
            model = make_pipeline(StandardScaler(), model)
        model.fit(X_train, y_train)
        correct = int((model.predict(X_test) == y_test).sum())
        print(f'  K={k:2d}: {correct}/{len(y_test)}')
