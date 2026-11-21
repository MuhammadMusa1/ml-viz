"""Сверка: ответы сети на странице viz/mnist (урок 14) должны совпадать с этим расчётом на numpy.

Запуск:  python tools/check_mnist.py
Берёт data/mnist.js (веса int8 и 300 картинок test), считает сеть 784 → 128 (ReLU) → 10 (softmax)
и печатает: сколько из 300 угадано, ошибки сети (номер, правда, ответ, уверенность) и ответ на картинку 0.
Те же числа показывает страница. Сеть обучает tools/export_mnist.py.
"""
import base64
import json
import os
import re

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, 'data', 'mnist.js'), encoding='utf-8').read()
D = json.loads(re.search(r'window\.MNIST = (\{.*\});', src).group(1))

W1 = np.frombuffer(base64.b64decode(D['w1']), dtype=np.int8).reshape(784, 128) * D['s1']
W2 = np.frombuffer(base64.b64decode(D['w2']), dtype=np.int8).reshape(128, 10) * D['s2']
b1, b2 = np.array(D['b1']), np.array(D['b2'])
X = np.frombuffer(base64.b64decode(D['test']), dtype=np.uint8).reshape(-1, 784) / 255.0
y = np.array(D['labels'])

h = np.maximum(0, X @ W1 + b1)
z = h @ W2 + b2
p = np.exp(z - z.max(axis=1, keepdims=True))
p /= p.sum(axis=1, keepdims=True)
pred = p.argmax(axis=1)

print(f'Угадано: {(pred == y).sum()} из {len(y)}')
print('Ошибки сети (номер: правда → ответ, уверенность):')
for i in np.where(pred != y)[0]:
    print(f'  {i}: {y[i]} → {pred[i]}, {100 * p[i, pred[i]]:.1f}%')
print('Картинка 0: правда', y[0], '→ ответ', pred[0], 'вероятности', ' '.join(f'{100 * v:.1f}' for v in p[0]))
E = np.frombuffer(base64.b64decode(D['err']), dtype=np.uint8).reshape(-1, 784) / 255.0
he = np.maximum(0, E @ W1 + b1)
ze = he @ W2 + b2
pe = np.exp(ze - ze.max(axis=1, keepdims=True))
pe /= pe.sum(axis=1, keepdims=True)
print('Галерея уверенных ошибок (X_test[номер]: правда → ответ, уверенность):')
for k, i in enumerate(D['errIndex']):
    print(f'  X_test[{i}]: {D["errLabels"][k]} → {pe[k].argmax()}, {100 * pe[k].max():.1f}%')
# Самый частый ответ среди 300 — точка отсчёта «ленивой» модели
vals, cnt = np.unique(y, return_counts=True)
print(f'«Ленивая» модель (всегда цифра {vals[cnt.argmax()]}): {cnt.max()} из {len(y)}')
