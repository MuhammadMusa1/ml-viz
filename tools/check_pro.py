"""Сверка раздела «Для профи» (viz/pro-*): числа на страницах = эталон на Python (numpy, scipy, scikit-learn).

Запуск:  pip install palmerpenguins scikit-learn scipy playwright && playwright install chromium
         python tools/check_pro.py

Страницы открываются с file:// в Chromium (Playwright), их функции расчёта вызываются напрямую
(window.PRO_*), а результат сравнивается с независимым расчётом на Python по тем же данным.
Данные страниц берутся прямо из HTML — между метками /* data:start */ и /* data:end */.

Что сверяется (последний прогон: расхождений 0):
  П1  косинус и евклидово расстояние запроса до 39 фраз     ↔ sklearn.metrics.pairwise
  П2  recall@k, MRR@k, число чанков: 15 размеров × 11 перекрытий × 2 поиска × k=1,3,5 (990 настроек)
                                                            ↔ эталонная реализация BM25 / нарезки на Python
  П3  вероятности после температуры и top-p (1558 настроек) ↔ scipy.special.softmax
  П4  faithfulness во всех 24 сочетаниях сценария и защит   ↔ подсчёт опоры на Python
  П5  GaussianNB: вероятности, матрица ошибок, accuracy, P/R/F1, macro-F1 на 66 порогах, ROC-AUC
                                                            ↔ sklearn (GaussianNB, confusion_matrix, f1_score, roc_auc_score)
      согласие судьи-LLM и человека, каппа Коэна            ↔ sklearn.metrics.cohen_kappa_score
  П6  доля остановленных атак и ложных блокировок, 256 комбинаций защит ↔ recall_score и FPR из confusion_matrix
  П8  среднее, медиана, p95 задержки                        ↔ numpy.percentile
  П9  время цикла, часы человека, дефекты в проде: 4096 комбинаций агент/проверка × 4 уровня контекста
                                                            ↔ та же модель на numpy
  П10 оценка по критериям, экономия и 95% интервал Уэлча, кольцо радара: 8 инструментов × 17 размеров пилота × 5 наборов весов
                                                            ↔ scipy.stats.ttest_ind(equal_var=False).confidence_interval

Пример сверки (П5, порог 0.5):
  >>> model = GaussianNB().fit(X_train[['bill_length_mm', 'body_mass_g']], y_train)
  >>> f1_score(y_test, pred, labels=['Adelie', 'Chinstrap', 'Gentoo'], average='macro', zero_division=0)
  0.868   # на странице: Macro-F1 0.87, accuracy 88% (61 из 69), AUC «Gentoo / не Gentoo» 0.977
"""
import functools
import json
import math
import pathlib
import re
import sys

import numpy as np
from scipy.special import softmax
from sklearn.metrics import (accuracy_score, cohen_kappa_score, confusion_matrix, f1_score,
                             precision_recall_fscore_support, recall_score, roc_auc_score)
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances

ROOT = pathlib.Path(__file__).resolve().parent.parent
FAILS = []


def page(pid):
    return ROOT / 'viz' / pid / 'index.html'


def data(pid):
    s = page(pid).read_text(encoding='utf-8')
    return json.loads(re.search(r'/\* data:start \*/(.*?)/\* data:end \*/', s, re.S).group(1))


def report(name, n, bad):
    print(f'{name:4s} сверено {n:5d}, расхождений {bad}')
    if bad:
        FAILS.append(name)


# ---------------------------------------------------------------- П1
def check_p1(pg):
    D = data('pro-embeddings')
    lex = {k.replace('ё', 'е'): np.array(v) for k, v in D['lex'].items()}

    def stem(w):
        c = [s for s in lex if w == s or (len(s) >= 3 and w.startswith(s))]
        return max(c, key=len) if c else None

    def embed(t):
        ws = re.findall(r'[a-zа-я]+', t.lower().replace('ё', 'е'))
        v = [lex[stem(w)] for w in ws if stem(w)]
        return np.mean(v, axis=0) if v else np.zeros(8)

    E = np.array([embed(p) for p, _ in D['phrases']])
    bad = n = 0
    for q in D['presets'] + [r['q'] for r in D['rounds']]:
        for metric in ['cos', 'euc']:
            js = pg.evaluate(f"PRO_EMB.search(PRO_EMB.embed({json.dumps(q, ensure_ascii=False)}).v, 39, '{metric}')")
            qv = embed(q).reshape(1, -1)
            ref = cosine_similarity(qv, E)[0] if metric == 'cos' else euclidean_distances(qv, E)[0]
            n += 1
            # euclidean_distances считает через |a|² + |b|² − 2ab: у одинаковых векторов выходит ~1e-8 вместо 0
            tol = 1e-9 if metric == 'cos' else 1e-7
            if any(abs(h['s'] - ref[h['i']]) > tol for h in js):
                bad += 1
    report('П1', n, bad)


# ---------------------------------------------------------------- П2 (эталон поиска на Python)
def check_p2(pg):
    D = data('pro-rag')
    DOC, QS, CON, STOP = D['doc'], D['questions'], D['concepts'], set(D['stop'])
    CN = list(CON)

    def words(t):
        return re.findall(r'[a-zа-я0-9]+(?:-[a-z0-9]+)*', t.lower().replace('ё', 'е'))

    def cvec(t):
        v = np.zeros(len(CN))
        for w in words(t):
            best = None
            for ci, c in enumerate(CN):
                for st in CON[c]:
                    if w.startswith(st) and (best is None or len(st) > best[1]):
                        best = (ci, len(st))
            if best:
                v[best[0]] += 1
        return v

    def bstem(w):
        if re.search(r'[0-9a-z]', w):
            return w
        return w if len(w) <= 4 else (w[:4] if len(w) <= 6 else w[:5])

    def btoks(t):
        return [bstem(w) for w in words(t) if w not in STOP]

    def chunk(S, o):
        L = len(DOC); out = []; pos = 0; ov = int(math.floor(S * o + 0.5))
        while True:
            end = min(L, pos + S)
            if end < L:
                cut = max(DOC.rfind(' ', pos + S // 2, end), DOC.rfind('\n', pos + S // 2, end))
                if cut > pos:
                    end = cut
            out.append((pos, end))
            if end >= L:
                break
            nxt = max(pos + 1, end - ov)
            while 0 < nxt < L and not DOC[nxt - 1].isspace():
                nxt += 1
            nxt = min(nxt, end)
            while nxt < L and DOC[nxt].isspace():
                nxt += 1
            pos = nxt
        return out

    def cos(a, b):
        n = np.linalg.norm(a) * np.linalg.norm(b)
        return float(a @ b / n) if n else 0.0

    def bm25(chs, q, k1=1.5, b=0.75):
        N = len(chs); avg = sum(map(len, chs)) / N; df = {}
        for c in chs:
            for w in set(c):
                df[w] = df.get(w, 0) + 1
        return [sum(math.log((N - df[w] + .5) / (df[w] + .5) + 1) * c.count(w) * (k1 + 1) /
                    (c.count(w) + k1 * (1 - b + b * len(c) / avg)) for w in sorted(set(q)) if w in df) for c in chs]

    def rank(sc):
        def cmp(i, j):
            d = sc[j] - sc[i]
            return (1 if d > 0 else -1) if abs(d) > 1e-12 else i - j
        return sorted(range(len(sc)), key=functools.cmp_to_key(cmp))

    def mm(x):
        lo, hi = min(x), max(x)
        return [(v - lo) / (hi - lo) if hi > lo else 0.0 for v in x]

    def evaluate(S, o, mode, k):
        ch = chunk(S, o); texts = [DOC[a:b] for a, b in ch]; rec = mrr = 0
        for q, key, _ in QS:
            cs = [cos(cvec(q), cvec(t)) for t in texts]
            sc = cs if mode == 'vec' else [0.5 * a + 0.5 * b for a, b in zip(mm(cs), mm(bm25([btoks(t) for t in texts], btoks(q))))]
            r = rank(sc); at = DOC.index(key)
            rel = [i for i, (s, e) in enumerate(ch) if s <= at and at + len(key) <= e]
            pos = [j for j, c in enumerate(r[:k]) if c in rel]
            if pos:
                rec += 1; mrr += 1 / (pos[0] + 1)
        return rec / len(QS), mrr / len(QS), len(ch)

    bad = n = 0
    for S in range(100, 801, 50):
        for ov in range(0, 51, 5):
            for mode in ['vec', 'hyb']:
                for k in [1, 3, 5]:
                    js = pg.evaluate(f"PRO_RAG.metrics({S},{ov}/100,'{mode}',{k})")
                    py = evaluate(S, ov / 100, mode, k); n += 1
                    if abs(js['recall'] - py[0]) > 1e-9 or abs(js['mrr'] - py[1]) > 1e-9 or js['n'] != py[2]:
                        bad += 1
    report('П2', n, bad)


# ---------------------------------------------------------------- П3
def check_p3(pg):
    D = data('pro-sampling')

    def ref(ci, T, top):
        z = np.array([c[1] for c in D['contexts'][ci]])
        p = np.eye(len(z))[np.argmax(z)] if T == 0 else softmax(z / T)
        o = np.argsort(-p, kind='stable'); keep = np.cumsum(p[o]) - p[o] < top - 1e-9
        m = np.zeros(len(p), bool); m[o[keep]] = True
        q = np.where(m, p, 0)
        return q / q.sum()

    bad = n = 0
    for ci in [0, 1]:
        for T in np.round(np.arange(0, 2.0001, 0.05), 2):
            for top in np.round(np.arange(0.1, 1.0001, 0.05), 2):
                js = np.array(pg.evaluate(f'PRO_SAMPLING.probs({ci},{T},{top}).p')); n += 1
                if np.abs(js - ref(ci, T, top)).max() > 1e-9:
                    bad += 1
    report('П3', n, bad)


# ---------------------------------------------------------------- П4
def check_p4(pg):
    D = data('pro-hallucinations')
    low = lambda s: s.lower().replace('ё', 'е')
    bad = n = 0
    for si, sc in enumerate(D['scenarios']):
        for ctx in [0, 1]:
            for cite in [0, 1]:
                for chk in [0, 1]:
                    sents = []
                    if ctx and sc.get('refuse'):
                        sents = [True]
                    else:
                        for s in sc['raw']:
                            x = s
                            if ctx:
                                if s['ctx'] == 'drop':
                                    continue
                                if isinstance(s['ctx'], dict):
                                    x = s['ctx']
                            docs = [sc['docs'][x['cite'] - 1]] if cite else sc['docs']
                            sents.append(any(low(x['f']) in low(d) for d in docs))
                    if chk:
                        sents = [s for s in sents if s]
                    ref = np.mean(sents) if sents else 1.0
                    js = pg.evaluate(f'PRO_HALLU.metrics({si},{{ctx:{ctx},cite:{cite},check:{chk}}}).faith'); n += 1
                    if abs(js - ref) > 1e-12:
                        bad += 1
    report('П4', n, bad)


# ---------------------------------------------------------------- П5
def check_p5(pg):
    from palmerpenguins import load_penguins
    from sklearn.model_selection import train_test_split
    from sklearn.naive_bayes import GaussianNB
    df = load_penguins().drop(columns=['sex']).dropna().reset_index(drop=True)
    X = df[['bill_length_mm', 'body_mass_g']]; y = df['species']
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
    m = GaussianNB().fit(Xtr, ytr); P = m.predict_proba(Xte); L = list(m.classes_)
    bad = int(np.abs(np.array(pg.evaluate('PRO_METRICS.proba()')) - P).max() > 1e-9); n = 1
    for th in np.round(np.arange(0.34, 1.0, 0.01), 2):
        pred = np.where(P.max(1) >= th - 1e-12, np.array(L)[P.argmax(1)], 'не уверена')
        cm = confusion_matrix(yte, pred, labels=L + ['не уверена'])[:3]
        pr, rc, f, _ = precision_recall_fscore_support(yte, pred, labels=L, zero_division=0)
        js = pg.evaluate(f'PRO_METRICS.metricsAt({th})'); n += 1
        ok = ((np.array(js['cm']) == cm).all() and abs(js['acc'] - accuracy_score(yte, pred)) < 1e-12
              and abs(js['macro'] - f1_score(yte, pred, labels=L, average='macro', zero_division=0)) < 1e-12
              and np.allclose([[x['P'], x['R'], x['F']] for x in js['per']], np.c_[pr, rc, f], atol=1e-12))
        bad += not ok
    n += 1; bad += abs(pg.evaluate('PRO_METRICS.auc') - roc_auc_score(yte == 'Gentoo', P[:, L.index('Gentoo')])) > 1e-12
    G = data('pro-metrics')['golden']
    for jt in range(2, 6):   # при пороге 1 судья всегда «да» — каппа не определена, страница пишет 0
        j = [int(r[6] >= jt) for r in G]; h = [r[7] for r in G]
        js = pg.evaluate(f'PRO_METRICS.llm({jt})'); n += 1
        bad += abs(js['kappa'] - cohen_kappa_score(j, h)) > 1e-12 or abs(js['agree'] - np.mean(np.array(j) == np.array(h))) > 1e-12
    report('П5', n, bad)


# ---------------------------------------------------------------- П6
def check_p6(pg):
    res = pg.evaluate('PRO_GUARD.configs().map(c => PRO_GUARD.metrics(c))')
    y = np.array(pg.evaluate('PRO_GUARD.unwanted')); bad = 0
    for m in res:
        pred = np.array(m['blocked']); tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
        bad += abs(recall_score(y, pred) - m['stop']) > 1e-12 or abs(fp / (fp + tn) - m['fb']) > 1e-12
    report('П6', len(res), bad)


# ---------------------------------------------------------------- П8
def check_p8(pg):
    lat = np.array(data('pro-architecture')['lat']); js = pg.evaluate('PRO_ARCH.lat')
    bad = (abs(js['mean'] - lat.mean()) > 1e-9) + (abs(js['med'] - np.percentile(lat, 50)) > 1e-9) + (abs(js['p95'] - np.percentile(lat, 95)) > 1e-9)
    report('П8', 3, int(bad))


# ---------------------------------------------------------------- П9
def check_p9(pg):
    import itertools
    D = data('pro-ai-sdlc'); S = np.array([[s['H'], s['h'], s['s'], s['a'], s['R']] for s in D['stages']])
    tc = D['testCatch']

    def run(agent, review, ctx):
        H, h, s, a, R = S.T
        agent = np.array(agent, bool); review = np.array(review, bool) & agent
        t = np.where(agent, H * s + R * review, H)
        d = np.where(agent, a * (1 - D['ctxEffect'] * ctx) * np.where(review, 1 - D['review'], 1), h)
        c = tc['human'] if not agent[3] else (tc['agentReviewed'] if review[3] else tc['agent'])
        prod = (d[:3].sum() * (1 - c) + d[3:].sum()) * D['perFeatures']
        return t.sum(), np.where(agent, R * review, H).sum(), prod

    combos = [(list(a), list(r)) for a in itertools.product([0, 1], repeat=6) for r in itertools.product([0, 1], repeat=6)]
    bad = n = 0
    for ctx in [0, 0.3, 0.6, 1]:
        js = pg.evaluate(f'(() => {{ const out = []; const C = {json.dumps(combos)};'
                         f' for (const [a, r] of C) {{ const x = PRO_SDLC.run({{agent: a, review: r, ctx: {ctx}}}); out.push([x.cycle, x.human, x.prod]); }} return out; }})()')
        for (a, r), j in zip(combos, js):
            n += 1
            if np.abs(np.array(j) - np.array(run(a, r, ctx))).max() > 1e-9:
                bad += 1
    report('П9', n, bad)


# ---------------------------------------------------------------- П10
def check_p10(pg):
    from scipy import stats
    D = data('pro-tech-radar')

    def ref(t, n, w):
        sw = sum(w) or 4
        w = w if sum(w) else [1, 1, 1, 1]
        sc = sum(s * x for s, x in zip(t['s'], w)) / sw
        gate = next((g for g in D['gates'] if not t['gates'][g]), None)
        st = None
        if t['pilot']:
            c, a = np.array(t['pilot']['ctrl'][:n]), np.array(t['pilot']['ai'][:n])
            ci = stats.ttest_ind(c, a, equal_var=False).confidence_interval(0.95)
            st = (c.mean() - a.mean(), ci.low, ci.high)
            dc, da = sum(t['pilot']['dc'][:n]), sum(t['pilot']['da'][:n])
        if gate:
            ring = 'hold'
        elif not st:
            ring = 'assess'
        elif st[2] < 0:
            ring = 'hold'
        elif st[1] <= 0 or da > dc or sc < D['adoptScore']:
            ring = 'trial'
        else:
            ring = 'adopt'
        return sc, st, ring

    bad = n_ = 0
    for wi, w in enumerate([D['weights'], [0, 0, 5, 0], [5, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]]):
        for ti, t in enumerate(D['tools']):
            for n in range(4, 21):
                js = pg.evaluate(f'PRO_RADAR.evaluate({ti},{n},{json.dumps(w)})')
                sc, st, ring = ref(t, n, w); n_ += 1
                ok = abs(js['score'] - sc) < 1e-12 and js['ring'] == ring
                if st:
                    ok = ok and max(abs(js['st']['d'] - st[0]), abs(js['st']['lo'] - st[1]), abs(js['st']['hi'] - st[2])) < 1e-9
                bad += not ok
    report('П10', n_, bad)


if __name__ == '__main__':
    from playwright.sync_api import sync_playwright
    checks = [('pro-embeddings', check_p1), ('pro-rag', check_p2), ('pro-sampling', check_p3), ('pro-hallucinations', check_p4),
              ('pro-metrics', check_p5), ('pro-guardrails', check_p6), ('pro-architecture', check_p8), ('pro-ai-sdlc', check_p9),
              ('pro-tech-radar', check_p10)]
    with sync_playwright() as p:
        b = p.chromium.launch()
        for pid, fn in checks:
            pg = b.new_page(); pg.goto(page(pid).as_uri()); pg.wait_for_timeout(300)
            fn(pg); pg.close()
        b.close()
    print('ВСЁ СОВПАДАЕТ' if not FAILS else 'РАСХОЖДЕНИЯ: ' + ', '.join(FAILS))
    sys.exit(1 if FAILS else 0)
