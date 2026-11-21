"""Обучает сеть из главы 14 на MNIST и выгружает её для страницы viz/mnist (урок 14) в data/mnist.js.

Запуск:  pip install scikit-learn numpy
         python tools/export_mnist.py путь/к/mnist.npz
mnist.npz — тот же файл, что скачивает Keras в Colab (mnist.load_data()):
https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz

Сеть как в книге: 784 → 128 (ReLU) → 10 (softmax), Adam, 5 эпох, пиксели / 255.
Учим через sklearn MLPClassifier (TensorFlow не нужен), random_state=42 — результат повторяется.
На сайт идут:
  * веса, сжатые до целых от −127 до 127 (int8) с множителем на слой — так файл в 4 раза меньше;
  * первые 300 картинок test как есть (0..255) и их правильные ответы.
Браузер сам считает ответы сети по этим весам. Сверка — tools/check_mnist.py.
"""
import base64
import json
import os
import sys
import warnings

import numpy as np
from sklearn.exceptions import ConvergenceWarning
from sklearn.neural_network import MLPClassifier

N_SITE = 300
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with np.load(sys.argv[1], allow_pickle=False) as d:
    x_train, y_train, x_test, y_test = d['x_train'], d['y_train'], d['x_test'], d['y_test']
X_train = x_train.reshape(-1, 784) / 255.0
X_test = x_test.reshape(-1, 784) / 255.0

net = MLPClassifier(hidden_layer_sizes=(128,), activation='relu', solver='adam', batch_size=32,
                    max_iter=5, random_state=42)
with warnings.catch_warnings():
    warnings.simplefilter('ignore', ConvergenceWarning)   # 5 эпох — нарочно, как в книге
    net.fit(X_train, y_train)
print('sklearn: точность на всём test (10 000):', round(net.score(X_test, y_test), 4))


def q8(w):
    """Целые −127..127 и множитель: w ≈ q * s."""
    s = float(np.abs(w).max()) / 127
    q = np.clip(np.round(w / s), -127, 127).astype(np.int8)
    return q, s


W1, s1 = q8(net.coefs_[0])           # 784 × 128
W2, s2 = q8(net.coefs_[1])           # 128 × 10
b1 = [round(float(v), 6) for v in net.intercepts_[0]]
b2 = [round(float(v), 6) for v in net.intercepts_[1]]

# Галерея «где сеть уверенно ошибается»: 12 самых уверенных ошибок сжатой сети на всём test.
# Это подборка, а не честная проверка — точность страница считает только по первым N_SITE картинкам.
h = np.maximum(0, X_test @ (W1 * s1) + np.array(b1))
z = h @ (W2 * s2) + np.array(b2)
p = np.exp(z - z.max(axis=1, keepdims=True))
p /= p.sum(axis=1, keepdims=True)
pred = p.argmax(axis=1)
wrong = np.where(pred != y_test)[0]
top = wrong[np.argsort(-p[wrong, pred[wrong]])][:12]
print('Сжатая сеть: точность на всём test:', round(float((pred == y_test).mean()), 4), '; ошибок:', len(wrong))

data = {
    'w1': base64.b64encode(W1.tobytes()).decode(), 's1': s1, 'b1': b1,
    'w2': base64.b64encode(W2.tobytes()).decode(), 's2': s2, 'b2': b2,
    'test': base64.b64encode(x_test[:N_SITE].astype(np.uint8).tobytes()).decode(),
    'labels': [int(v) for v in y_test[:N_SITE]],
    'err': base64.b64encode(x_test[top].astype(np.uint8).tobytes()).decode(),
    'errLabels': [int(v) for v in y_test[top]],
    'errIndex': [int(v) for v in top],        # номер картинки в X_test — найти её в Colab
}
with open(os.path.join(ROOT, 'data', 'mnist.js'), 'w', encoding='utf-8', newline='\n') as f:
    f.write('// MNIST (LeCun, Cortes, Burges): первые %d картинок test и веса сети 784 → 128 → 10 из урока 14.\n' % N_SITE)
    f.write('// Собрано tools/export_mnist.py. Веса int8 построчно (вход × выход), картинки uint8 построчно 28 × 28.\n')
    f.write('// Подключается через <script>, а не fetch(), чтобы работало офлайн с file://\n')
    f.write('window.MNIST = ' + json.dumps(data, separators=(',', ':')) + ';\n')
print('data/mnist.js: %.0f КБ' % (os.path.getsize(os.path.join(ROOT, 'data', 'mnist.js')) / 1024))
