"""Сверка: веса внимания на странице viz/attention должны совпадать с numpy.

Запуск:  pip install numpy
         python tools/check_attention.py
Предложения, признаки слов и матрица запросов WQ — data/attention_sentences.js.
Self-attention одной «головы»:  Q = X·WQᵀ,  K = X,  веса = softmax(Q·Kᵀ / √d · резкость), d = 8.
Маска «только назад» (как в GPT): слово не видит слова справа.
Выводит для каждого слова, на кого оно смотрит сильнее всего (и сколько процентов),
при резкости 1 без маски и с маской, а также полную строку для пары примеров.
"""
import json
from pathlib import Path

import numpy as np

src = (Path(__file__).parent.parent / 'data' / 'attention_sentences.js').read_text(encoding='utf-8')
data = json.loads(src[src.index('{'):src.rindex('}') + 1])
WQ = np.array(data['WQ'], dtype=float)
D = len(data['features'])


def pct(x):
    return f'{int(x * 100 + 0.5)}%'   # обычное округление, как на странице (12.5% → 13%)


def attention(X, sharp=1.0, causal=False):
    Q, K = X @ WQ.T, X
    S = Q @ K.T / np.sqrt(D) * sharp
    if causal:
        S = np.where(np.tril(np.ones_like(S)) == 1, S, -np.inf)
    S = S - S.max(axis=1, keepdims=True)
    W = np.exp(S)
    return W / W.sum(axis=1, keepdims=True)


for s in data['sentences']:
    words = [t['t'] for t in s['tokens']]
    X = np.array([t['x'] for t in s['tokens']], dtype=float)
    print(' '.join(words))
    for causal in (False, True):
        A = attention(X, causal=causal)
        best = [f'{w}→{words[int(np.argmax(A[i]))]} {pct(A[i].max())}' for i, w in enumerate(words)]
        print(('  только назад: ' if causal else '  все слова:    ') + ', '.join(best))

X = np.array([t['x'] for t in data['sentences'][0]['tokens']], dtype=float)
words = [t['t'] for t in data['sentences'][0]['tokens']]
for sharp in (1, 2, 0.5):
    row = attention(X, sharp)[5]
    print(f'«он» при резкости {sharp}: ' + ', '.join(f'{w} {pct(p)}' for w, p in zip(words, row)))
