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
  М 04  лучшая прямая и средняя ошибка на train ↔ LinearRegression; ответы игры (подставить x, уравнение по графику)
  М 05  наклон ↔ численная производная, 20 шагов спуска при 5 размерах шага, ответы игры
  М 06  косинусы и самая похожая стрелка (запас ≥ 0.05), сумма векторов ↔ numpy
  М 07  вероятности в 10 вопросах игры ↔ доли на numpy
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


def check_m4(pg):
    from sklearn.linear_model import LinearRegression
    tr, _ = train_test_split(df, test_size=0.2, random_state=42)
    m = LinearRegression().fit(tr[['flipper_length_mm']], tr['body_mass_g'])
    best = pg.evaluate('MATH_LINE.best'); n = 2
    bad = int(abs(best['a'] - m.coef_[0]) > 1e-9) + int(abs(best['b'] - m.intercept_) > 1e-6)
    pred = m.predict(tr[['flipper_length_mm']])
    n += 1; bad += abs(pg.evaluate(f"MATH_LINE.mae({best['a']}, {best['b']})") - np.abs(tr['body_mass_g'] - pred).mean()) > 1e-6
    for q in pg.evaluate('MATH_LINE.rounds'):
        o = pg.evaluate(f'MATH_LINE.options({json.dumps(q)})'); n += 1
        if q['t'] == 'val':
            y = q['a'] * q['x'] + q['b']
            bad += float(o['labels'][o['right']]) != y
        else:
            bad += o['labels'][o['right']] != 'y = ' + pg.evaluate(f"MATH_LINE.eq({q['a']}, {q['b']})")
    print(f"      лучшая прямая на train: масса = {m.coef_[0]:.2f} × крыло {m.intercept_:+.2f}")
    report('М 04', n, bad)


def check_m5(pg):
    bad = n = 0
    for x in np.arange(-1, 7.01, 0.5):
        h = 1e-6; num_slope = ((x + h - 3) ** 2 - (x - h - 3) ** 2) / (2 * h)
        n += 1; bad += abs(pg.evaluate(f'MATH_SLOPE.slope({x})') - num_slope) > 1e-5
    # спуск: 20 шагов с разными размерами шага
    for lr in [0.1, 0.3, 0.5, 1.0, 1.1]:
        x = 0.0; js = 0.0
        for _ in range(20):
            x = x - lr * 2 * (x - 3); js = pg.evaluate(f'(() => {{ let x = 0; for (let i = 0; i < 20; i++) x = MATH_SLOPE.step(x, {lr}); return x; }})()')
        n += 1; bad += abs(js - x) > 1e-9 * max(1, abs(x))
    for q in pg.evaluate('MATH_SLOPE.rounds'):
        o = pg.evaluate(f'MATH_SLOPE.options({json.dumps(q)})'); n += 1
        s = 2 * (q['x'] - 3)
        if q['t'] == 'dir':
            bad += o['right'] != (0 if s > 0 else 1 if s < 0 else 2)
        else:
            bad += abs(float(o['labels'][o['right']]) - (q['x'] - q['lr'] * s)) > 1e-9
    report('М 05', n, bad)


def check_m6(pg):
    bad = n = 0
    for q in pg.evaluate('MATH_VEC.rounds'):
        o = pg.evaluate(f'MATH_VEC.options({json.dumps(q)})'); n += 1
        if q['t'] == 'sum':
            sx, sy = q['a'][0] + q['b'][0], q['a'][1] + q['b'][1]
            bad += o['labels'][o['right']] != f'({sx}; {sy})'
        else:
            a = np.array(q['a'], float); c = np.array(q['c'], float)
            cs = c @ a / np.linalg.norm(c, axis=1) / np.linalg.norm(a); srt = np.sort(cs)
            js = [pg.evaluate(f"MATH_VEC.cos({json.dumps(q['a'])}, {json.dumps(v)})") for v in q['c']]
            bad += o['right'] != int(np.argmax(cs)) or srt[-1] - srt[-2] < 0.05 or np.abs(np.array(js) - cs).max() > 1e-12
    report('М 06', n, bad)


def check_m7(pg):
    bad = n = 0
    for q in pg.evaluate('MATH_PROB.rounds'):
        o = pg.evaluate(f'MATH_PROB.options({json.dumps(q)})'); n += 1
        if q['t'] == 'coin':
            ref = 50
        elif q['t'] == 'miss':
            ref = 100 - q['pa'] - q['pc']
        else:
            c = np.array(q['c'], float); p = c / c.sum()
            ref = round(100 * (p[q['sp']] if q['t'] == 'one' else 1 - p[0]), 1)
        lab = o['labels'][o['right']].rstrip('%')
        bad += abs(float(lab) - ref) > 1e-9
    report('М 07', n, bad)


if __name__ == '__main__':
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        for pid, fn in [('math-percent', check_m1), ('math-distance', check_m2), ('math-mean', check_m3), ('math-line', check_m4),
                        ('math-slope', check_m5), ('math-vector', check_m6), ('math-prob', check_m7)]:
            pg = b.new_page(); pg.goto((ROOT / 'viz' / pid / 'index.html').as_uri()); pg.wait_for_timeout(300)
            fn(pg); pg.close()
        b.close()
    print('ВСЁ СОВПАДАЕТ' if not FAILS else 'РАСХОЖДЕНИЯ: ' + ', '.join(FAILS))
    sys.exit(1 if FAILS else 0)
