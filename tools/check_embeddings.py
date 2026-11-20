"""Сверка: соседи, аналогии и карта на странице viz/embeddings должны совпадать с numpy.

Запуск:  pip install numpy
         python tools/check_embeddings.py
Слова и векторы — data/embed_words.js (те же, что на странице).
Похожесть — косинус угла между векторами (cosine similarity), на странице в процентах.
Соседи: по убыванию похожести, при равенстве — кто раньше в списке слов.
Аналогия A − B + C: ближайшее по косинусу слово, кроме A, B и C.
Карта — PCA на 2 оси: собственные векторы ковариации; знак оси выбран так,
чтобы самый большой по модулю коэффициент был положительным (sklearn может отразить карту зеркально).
"""
import json
from pathlib import Path

import numpy as np

src = (Path(__file__).parent.parent / 'data' / 'embed_words.js').read_text(encoding='utf-8')
data = json.loads(src[src.index('{'):src.rindex('}') + 1])
words = [d['w'] for d in data['words']]
V = np.array([d['v'] for d in data['words']], dtype=float)
unit = V / np.linalg.norm(V, axis=1, keepdims=True)


def cos_to(vec):
    return unit @ (vec / np.linalg.norm(vec))


def neighbors(i, k=5):
    sims = cos_to(V[i])
    order = sorted((j for j in range(len(words)) if j != i), key=lambda j: (-round(sims[j], 9), j))
    return [(words[j], sims[j]) for j in order[:k]]


for w in ['пингвин', 'король', 'торт', 'самолёт']:
    print(f'{w}: ' + ', '.join(f'{n} {s:.0%}' for n, s in neighbors(words.index(w))))

for a, b, c in [('король', 'мужчина', 'женщина'), ('принц', 'мальчик', 'девочка'),
                ('мужчина', 'мальчик', 'девочка'), ('самолёт', 'воробей', 'рыба')]:
    vec = V[words.index(a)] - V[words.index(b)] + V[words.index(c)]
    sims = cos_to(vec)
    skip = {words.index(a), words.index(b), words.index(c)}
    j = min((j for j in range(len(words)) if j not in skip), key=lambda j: (-round(sims[j], 9), j))
    print(f'{a} − {b} + {c} = {words[j]} ({sims[j]:.0%})')

X = V - V.mean(axis=0)
vals, vecs = np.linalg.eigh(X.T @ X / len(X))
order = np.argsort(vals)[::-1]
vals, vecs = vals[order], vecs[:, order]
for k in range(2):
    if vecs[np.argmax(np.abs(vecs[:, k])), k] < 0:
        vecs[:, k] *= -1
xy = X @ vecs[:, :2]
print(f'Карта сохраняет {vals[:2].sum() / vals.sum():.0%} разброса (ось 1: {vals[0] / vals.sum():.0%}, ось 2: {vals[1] / vals.sum():.0%})')
for w in ['король', 'пингвин', 'торт', 'ракета']:
    i = words.index(w)
    print(f'  {w}: ({xy[i, 0]:.2f}, {xy[i, 1]:.2f})')
