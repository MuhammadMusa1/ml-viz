"""Сверка: токенизатор BPE на странице viz/tokens должен совпадать с этим скриптом.

Запуск:  python tools/check_tokenizer.py      (нужен только Python, без библиотек)
Учебный текст — data/tok_corpus.js (тот же, что на странице).
Алгоритм (Byte Pair Encoding на буквах, как в коде «Для любопытных»):
  1) текст в нижнем регистре режем на слова и знаки препинания;
     слово = «▁» (пробел перед словом) + его буквы, знак препинания — один символ;
  2) считаем все пары соседних символов во всех словах;
  3) самую частую пару склеиваем в новый токен (при равенстве — пара раньше по алфавиту);
  4) повторяем, пока самая частая пара встречается хотя бы 2 раза, но не больше MAX_MERGES раз.
Выводит первые слияния, число слияний, размер словаря и разбиение примеров при 0, 20 и всех слияниях.
"""
import json
import re
from collections import Counter
from pathlib import Path

MAX_MERGES = 150
SPACE = '▁'
src = (Path(__file__).parent.parent / 'data' / 'tok_corpus.js').read_text(encoding='utf-8')
corpus = json.loads(src[src.index('{'):src.rindex('}') + 1])['text']

WORD = re.compile(r'[a-zа-яё0-9]+|[^\sa-zа-яё0-9]')


def pieces(text):
    """Слова и знаки: слово получает «▁» спереди, знак остаётся одним символом."""
    out = []
    for w in WORD.findall(text.lower()):
        out.append([SPACE] + list(w) if w[0].isalnum() else [w])
    return out


def merge_word(sym, a, b):
    out, i = [], 0
    while i < len(sym):
        if i + 1 < len(sym) and sym[i] == a and sym[i + 1] == b:
            out.append(a + b); i += 2
        else:
            out.append(sym[i]); i += 1
    return out


def train(text):
    words = Counter(tuple(p) for p in pieces(text))
    words = {k: v for k, v in words.items()}
    merges = []
    while len(merges) < MAX_MERGES:
        pairs = Counter()
        for w, n in words.items():
            for x, y in zip(w, w[1:]):
                pairs[(x, y)] += n
        if not pairs:
            break
        best = min(pairs, key=lambda p: (-pairs[p], p))   # чаще всего, при равенстве — по алфавиту
        if pairs[best] < 2:
            break
        merges.append((best, pairs[best]))
        words = {tuple(merge_word(list(w), *best)): n for w, n in words.items()}
    return merges


def encode(text, merges, limit):
    rank = {p: i for i, (p, _) in enumerate(merges[:limit])}
    tokens = []
    for sym in pieces(text):
        while len(sym) > 1:
            cand = [(rank[(x, y)], (x, y)) for x, y in zip(sym, sym[1:]) if (x, y) in rank]
            if not cand:
                break
            sym = merge_word(sym, *min(cand)[1])
        tokens += sym
    return tokens


merges = train(corpus)
base = sorted({ch for p in pieces(corpus) for ch in p})
print(f'Символов в начале: {len(base)}, слияний: {len(merges)}, словарь: {len(base) + len(merges)}')
for i, ((a, b), n) in enumerate(merges[:25], 1):
    print(f'  {i:2d}. {a} + {b} → {a + b}  ({n} раз)')
print(f'  ... последнее: {merges[-1][0][0]} + {merges[-1][0][1]} ({merges[-1][1]} раз)')

for sample in ['Пингвины учатся плавать, а модели учатся на примерах.',
               'Токенизатор режет текст на кусочки.']:
    for limit in (0, 20, len(merges)):
        toks = encode(sample, merges, limit)
        print(f'{limit:3d} слияний: {len(toks):2d} токенов | ' + ' '.join(toks))
