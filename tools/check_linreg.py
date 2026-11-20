"""Сверка: «Лучшая прямая» на странице viz/linreg должна совпадать с sklearn.

Запуск:  pip install palmerpenguins scikit-learn
         python tools/check_linreg.py
Предсказываем массу (body_mass_g) по длине крыла (flipper_length_mm), обучение на train (273 пингвина).
Выводит коэффициенты прямой и метрики на train — их показывает страница после кнопки «Лучшая прямая»
(выброс выключен), — и R² на test.
"""
from palmerpenguins import load_penguins
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

df = load_penguins().drop(columns=['sex']).dropna().reset_index(drop=True)
X = df[['flipper_length_mm']]
y = df['body_mass_g']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression().fit(X_train, y_train)
pred = model.predict(X_train)
mse = mean_squared_error(y_train, pred)
print(f'масса = {model.coef_[0]:.4f} * крыло {model.intercept_:+.4f}')
print(f'train: MAE = {mean_absolute_error(y_train, pred):.2f}  MSE = {mse:.2f}  '
      f'RMSE = {mse ** 0.5:.2f}  R2 = {r2_score(y_train, pred):.4f}')
print(f'test:  R2 = {r2_score(y_test, model.predict(X_test)):.4f}')
