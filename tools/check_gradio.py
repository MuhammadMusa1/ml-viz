"""Сверка: модель в приложении на странице viz/gradio (урок 20) должна совпадать с sklearn.

Запуск:  pip install palmerpenguins scikit-learn
         python tools/check_gradio.py
Приложение предсказывает массу пингвина по длине крыла: LinearRegression на train (как в уроке 8).
Печатает коэффициенты, диапазон длины крыла в train (в нём модели можно верить) и прогнозы для разных
длин крыла — те же числа показывает приложение на странице (масса округлена до грамма).
"""
from palmerpenguins import load_penguins
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

df = load_penguins().drop(columns=['sex']).dropna().reset_index(drop=True)
X = df[['flipper_length_mm']]
y = df['body_mass_g']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression().fit(X_train, y_train)
print(f'масса = {model.coef_[0]:.4f} × крыло {model.intercept_:+.3f}')
lo, hi = int(X_train['flipper_length_mm'].min()), int(X_train['flipper_length_mm'].max())
print(f'Длина крыла в train: от {lo} до {hi} мм')
for x in (0, 100, 150, lo, 190, 200, 210, hi, 250, 300, 500):
    pred = model.predict(X_train.iloc[:1].assign(flipper_length_mm=x))[0]   # с именем столбца, как при обучении
    print(f'  крыло {x:3d} мм → {round(float(pred)):6d} г')
