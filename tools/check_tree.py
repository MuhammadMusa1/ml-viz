"""Сверка: дерево решений на странице viz/tree должно совпадать с sklearn.

Запуск:  pip install palmerpenguins scikit-learn
         python tools/check_tree.py
Для max_depth = 1..6 выводит точность на train (из 273) и test (из 69)
и сами вопросы дерева (признак и порог) — их же рисует страница в кнопке «Пусть построит модель».
Признаки — длина и глубина клюва, без масштабирования (дереву масштаб не нужен).
"""
from palmerpenguins import load_penguins
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text

df = load_penguins().drop(columns=['sex']).dropna().reset_index(drop=True)
X = df[['bill_length_mm', 'bill_depth_mm']]
y = df['species']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

for depth in range(1, 7):
    model = DecisionTreeClassifier(criterion='gini', max_depth=depth, random_state=42)
    model.fit(X_train, y_train)
    tr = int((model.predict(X_train) == y_train).sum())
    te = int((model.predict(X_test) == y_test).sum())
    print(f'max_depth={depth}: train {tr}/{len(y_train)}, test {te}/{len(y_test)}, листьев {model.get_n_leaves()}')
    if depth <= 2:
        print(export_text(model, feature_names=list(X.columns), decimals=2))
