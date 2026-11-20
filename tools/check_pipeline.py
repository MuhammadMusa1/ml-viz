"""Сверка: точность конвейеров на странице viz/pipeline должна совпадать с sklearn.

Запуск:  pip install palmerpenguins scikit-learn
         python tools/check_pipeline.py
Признаки — длина клюва (мм) и масса (г): у них очень разный масштаб.
Для каждого конвейера выводит число правильных ответов на test (из 69):
  * KNN, K = 1..25: без масштаба, с Pipeline(StandardScaler, KNN), и с «утечкой» (scaler обучен на всех данных);
  * дерево, max_depth = 1..6: без масштаба и с масштабом.
"""
from palmerpenguins import load_penguins
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

df = load_penguins().drop(columns=['sex']).dropna().reset_index(drop=True)
X = df[['bill_length_mm', 'body_mass_g']]
y = df['species']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

sc = StandardScaler().fit(X_train)
print('StandardScaler на train: mean =', sc.mean_.round(4).tolist(), ' std =', sc.scale_.round(4).tolist())
leak = StandardScaler().fit(X)   # ОШИБКА: масштаб «подсмотрел» test
print('StandardScaler на всех:  mean =', leak.mean_.round(4).tolist(), ' std =', leak.scale_.round(4).tolist())


def score(model):
    return int((model.predict(X_test) == y_test).sum())


print('\nKNN:  K  без масштаба  Pipeline  утечка')
for k in range(1, 26):
    raw = KNeighborsClassifier(n_neighbors=k).fit(X_train, y_train)
    pipe = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k)).fit(X_train, y_train)
    lk = KNeighborsClassifier(n_neighbors=k).fit(leak.transform(X_train), y_train)
    leak_score = int((lk.predict(leak.transform(X_test)) == y_test).sum())
    print(f'     {k:2d}  {score(raw):12d}  {score(pipe):8d}  {leak_score:6d}')

print('\nДерево: max_depth  без масштаба  с масштабом')
for d in range(1, 7):
    raw = DecisionTreeClassifier(max_depth=d, random_state=42).fit(X_train, y_train)
    pipe = make_pipeline(StandardScaler(), DecisionTreeClassifier(max_depth=d, random_state=42)).fit(X_train, y_train)
    print(f'        {d}  {score(raw):12d}  {score(pipe):11d}')

# Игра на странице: конвейеры сравниваются на validation (train ещё раз поделён), test — один раз в конце
X_tr, X_val, y_tr, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=42)


def val_score(model):
    return int((model.fit(X_tr, y_tr).predict(X_val) == y_val).sum())


print(f'\nValidation (из {len(y_val)}), конвейер учится на {len(y_tr)} пингвинах:')
print('KNN:  K  без масштаба  Pipeline')
for k in range(1, 26):
    print(f'     {k:2d}  {val_score(KNeighborsClassifier(n_neighbors=k)):12d}  '
          f'{val_score(make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k))):8d}')
print('Дерево: max_depth  без масштаба  с масштабом')
for d in range(1, 7):
    print(f'        {d}  {val_score(DecisionTreeClassifier(max_depth=d, random_state=42)):12d}  '
          f'{val_score(make_pipeline(StandardScaler(), DecisionTreeClassifier(max_depth=d, random_state=42))):11d}')
