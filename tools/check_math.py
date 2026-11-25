"""Сверка раздела «Математика для ML» (viz/math-*): числа на страницах = расчёт на Python (pandas, numpy, sklearn).

Запуск:  pip install palmerpenguins pandas scikit-learn playwright && playwright install chromium
         python tools/check_math.py

Страницы открываются с file:// в Chromium (Playwright), их функции вызываются напрямую (window.MATH_*).

Что сверяется (последний прогон: расхождений 0):
  М 01  «ленивая» модель на test (самый частый вид train) и доля Gentoo ↔ train_test_split + pandas;
        верный вариант в каждом из 10 вопросов игры ↔ round(100 · часть / целое), round(целое · p / 100), сравнение долей
  М 02  расстояния и ближайшая точка во всех 10 раундах ↔ numpy; ничьих и «почти ничьих» (< 0.1) нет
  М 03  среднее, медиана, стандартное отклонение (ddof=0, как StandardScaler) массы по видам, с опечаткой и без ↔ pandas;
        верный вариант в 10 вопросах игры ↔ numpy
"""
import json
import pathlib
import sys

import numpy as np
from palmerpenguins import load_penguins
from sklearn.model_selection import train_test_split

ROOT = pathlib.Path(__file__).resolve().parent.parent
FAILS = []
df = load_penguins().drop(columns=['sex']).dropna().reset_index(drop=True)


def report(name, n, bad):
    print(f'{name:5s} сверено {n:4d}, расхождений {bad}')
    if bad:
        FAILS.append(name)


def check_m1(pg):
    tr, te = train_test_split(df, test_size=0.2, random_state=42)
    lazy = tr['species'].value_counts().idxmax()
    facts = pg.evaluate('MATH_PCT.facts')
    bad = int(facts['lazy'] != {'k': int((te['species'] == lazy).sum()), 'n': len(te)})
    bad += int(facts['gentoo'] != {'k': int((df['species'] == 'Gentoo').sum()), 'n': len(df)})
    rounds = pg.evaluate('MATH_PCT.rounds'); n = 2
    for q in rounds:
        o = pg.evaluate(f'MATH_PCT.options({json.dumps(q)})'); n += 1
        if q['t'] == 'pct':
            ok = o['labels'][o['right']] == f"{round(100 * q['k'] / q['n'])}%"
        elif q['t'] == 'part':
            ok = o['labels'][o['right']] == str(round(q['n'] * q['p'] / 100))
        else:
            ok = o['right'] == (0 if q['a'] / q['an'] > q['b'] / q['bn'] else 1)
        bad += not ok
    print(f"      ленивая модель: {facts['lazy']['k']} из {facts['lazy']['n']}, Gentoo: {facts['gentoo']['k']} из {facts['gentoo']['n']}")
    report('М 01', n, bad)


def check_m2(pg):
    rounds = pg.evaluate('MATH_DIST.rounds'); bad = n = 0
    for q, ps in rounds:
        d = np.linalg.norm(np.array(ps) - np.array(q), axis=1)
        js = [pg.evaluate(f'MATH_DIST.dist({json.dumps(q)}, {json.dumps(p)})') for p in ps]
        s = np.sort(d); n += 1
        bad += np.abs(np.array(js) - d).max() > 1e-12 or s[1] - s[0] < 0.1
    report('М 02', n, bad)


def check_m3(pg):
    bad = n = 0
    typo = float(df['body_mass_g'].iloc[0] * 10)
    for sp in ['Adelie', 'Chinstrap', 'Gentoo', 'all']:
        s = df['body_mass_g'] if sp == 'all' else df.loc[df['species'] == sp, 'body_mass_g']
        for t in [False, True]:
            x = np.append(s.to_numpy(float), typo) if t else s.to_numpy(float)
            js = pg.evaluate(f"MATH_MEAN.stats('{sp}', {str(t).lower()})"); n += 1
            bad += (js['n'] != len(x) or abs(js['mean'] - x.mean()) > 1e-9 or abs(js['median'] - np.median(x)) > 1e-9
                    or abs(js['std'] - x.std(ddof=0)) > 1e-9)
    for q in pg.evaluate('MATH_MEAN.rounds'):
        o = pg.evaluate(f'MATH_MEAN.options({json.dumps(q)})'); n += 1
        if q['t'] == 'mean':
            bad += o['labels'][o['right']] != f"{round(np.mean(q['xs']))} г"
        else:
            bad += o['right'] != (0 if np.std(q['a']) > np.std(q['b']) else 1)
    report('М 03', n, bad)


if __name__ == '__main__':
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        for pid, fn in [('math-percent', check_m1), ('math-distance', check_m2), ('math-mean', check_m3)]:
            pg = b.new_page(); pg.goto((ROOT / 'viz' / pid / 'index.html').as_uri()); pg.wait_for_timeout(300)
            fn(pg); pg.close()
        b.close()
    print('ВСЁ СОВПАДАЕТ' if not FAILS else 'РАСХОЖДЕНИЯ: ' + ', '.join(FAILS))
    sys.exit(1 if FAILS else 0)
