"""Сверка: мини-модель и температура на странице viz/temperature должны совпадать с этим скриптом.

Запуск:  python tools/check_temperature.py      (нужен только Python)
Модель — биграммы: вероятность следующего слова по тому, как часто оно шло после текущего
в учебном тексте data/lm_corpus.js. К каждому слову словаря добавлено ALPHA = 0.001 «на всякий случай»,
поэтому любое слово возможно, но очень редко.
Температура T: вес слова = (число + ALPHA)^(1/T), потом делим на сумму. T = 0 — всегда самое частое слово.
Случайность — генератор mulberry32 с номером броска (как MLViz.rng на странице), чтобы тексты совпадали.
"""
import json
import re
from pathlib import Path

ALPHA, MAX_WORDS = 0.001, 14
src = (Path(__file__).parent.parent / 'data' / 'lm_corpus.js').read_text(encoding='utf-8')
corpus = json.loads(src[src.index('{'):src.rindex('}') + 1])
tokens = re.findall(r'[а-яё]+|\.', corpus['text'].lower())
vocab = sorted(set(tokens))
counts = {}
for a, b in zip(tokens, tokens[1:]):
    counts.setdefault(a, {}).setdefault(b, 0)
    counts[a][b] += 1


def dist(prev, T):
    c = counts.get(prev, {})
    if T == 0:   # самое частое слово, при равенстве — раньше по алфавиту
        best = max(vocab, key=lambda w: (c.get(w, 0), [-ord(ch) for ch in w]))
        best = min((w for w in vocab if c.get(w, 0) == c.get(best, 0)))
        return [1.0 if w == best else 0.0 for w in vocab]
    wts = [(c.get(w, 0) + ALPHA) ** (1 / T) for w in vocab]
    s = sum(wts)
    return [x / s for x in wts]


def mulberry32(seed):
    a = seed & 0xFFFFFFFF
    M = 0xFFFFFFFF

    def imul(x, y):
        return (x * y) & M

    def rnd():
        nonlocal a
        a = (a + 0x6D2B79F5) & M
        x = imul(a ^ (a >> 15), 1 | a)
        x = ((x + imul(x ^ (x >> 7), 61 | x)) & M) ^ x
        return ((x ^ (x >> 14)) & M) / 4294967296
    return rnd


def generate(start, T, seed):
    rnd, out = mulberry32(seed), [start]
    for _ in range(MAX_WORDS):
        p = dist(out[-1], T)
        u, acc, pick = rnd(), 0.0, vocab[-1]
        for w, pw in zip(vocab, p):
            acc += pw
            if u < acc:
                pick = w
                break
        out.append(pick)
        if pick == '.':
            break
    return ' '.join(out)


print(f'Слов в тексте: {len(tokens)}, словарь: {len(vocab)}')
for T in (0.5, 1, 2, 3):
    p = dist('пингвин', T)
    top = sorted(zip(vocab, p), key=lambda x: (-round(x[1], 12), x[0]))[:5]
    rest = 1 - sum(x[1] for x in top)
    print(f'после «пингвин», T = {T}: ' + ', '.join(f'{w} {q:.1%}' for w, q in top) + f', остальные {rest:.1%}')
for s in corpus['starts']:
    print(f'T = 0, {s}: {generate(s, 0, 1)}')
for T in (1, 2, 3):
    for seed in (1, 2, 3):
        print(f'T = {T}, бросок {seed}: {generate("пингвин", T, seed)}')
