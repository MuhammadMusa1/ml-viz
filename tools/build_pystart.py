"""Раздел «Python с нуля» (viz/py-*): примеры и задания -> data/pystart.js.

Как и в разминках (tools/build_warmup.py), ответы руками не пишем: каждую программу запускает настоящий Python.
  • Пошаговые примеры: sys.settrace записывает перед каждой строкой, что лежит в переменных и что уже напечатано.
    Страница показывает это кнопками «Шаг» / «Назад» — как отладчик, но без установки программ.
  • Задания (out / bug / parsons): вывод, строку ошибки и все верные порядки строк считает build() из build_warmup.py.
Руками пишутся только неверные варианты — скрипт проверяет, что они действительно неверные.

Запуск:  pip install pandas   (для страницы py-pandas)
         python tools/build_pystart.py
Тексты (ex_<id> подпись примера, exb_<id> кнопка примера, x_<id>, g_<id>, topic_<тема>) — в STR страницы viz/<page>/index.html.
"""
import ast
import contextlib
import io
import json
import os
import re
import sys
import types

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_warmup import build  # noqa: E402  (тот же проверенный сборщик заданий)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TABLE = '''import pandas as pd
df = pd.DataFrame({
    "species": ["Adelie", "Gentoo", "Adelie"],
    "mass": [3000, 5000, 4000],
})
'''

PAGES = {
    # ---------- Py 01: print и переменные ----------
    'py-print': dict(
        demos=[
            dict(id='p1x', code='''
print("Привет, пингвин!")
print(2 + 3)
print("2 + 3")
'''),
            dict(id='p1y', code='''
name = "Adelie"
mass = 3750
print(name, mass)
mass = mass + 250
print(mass)
'''),
            dict(id='p1z', code='''
a = 7
b = 2
print(a + b, a - b, a * b)
print(a / b)
c = a * 2 + 1
print(c)
'''),
        ],
        tasks=[
            dict(id='p1a', type='out', topic='print', code='''
print(10 + 5)
''', wrong=['10 + 5', '105', '!err']),
            dict(id='p1b', type='out', topic='str', code='''
print("10" + "5")
''', wrong=['15', '10 + 5', '!err']),
            dict(id='p1c', type='out', topic='var', code='''
x = 4
x = x * 2
print(x)
''', wrong=['4', 'x * 2', '16']),
            dict(id='p1d', type='out', topic='str', code='''
name = "Gentoo"
print("name")
''', wrong=['Gentoo', '"name"', '!err']),
            dict(id='p1e', type='out', topic='math', code='''
print(7 / 2)
''', wrong=['3', '3.0', '4']),
            dict(id='p1f', type='bug', topic='str', code='''
a = 5
print(a)
print("Привет)
'''),
            dict(id='p1g', type='bug', topic='str', code='''
age = 13
print("Мне лет: " + age)
'''),
            dict(id='p1h', type='parsons', topic='var', code='''
a = 3
b = 4
s = a + b
print(s)
'''),
        ]),
    # ---------- Py 02: условия ----------
    'py-if': dict(
        demos=[
            dict(id='i2x', code='''
mass = 5000
if mass > 4500:
    print("большой пингвин")
print("конец")
'''),
            dict(id='i2y', code='''
flipper = 190
if flipper > 206:
    print("Gentoo")
else:
    print("не Gentoo")
'''),
            dict(id='i2z', code='''
bill = 45
if bill < 40:
    print("Adelie")
elif bill < 48:
    print("Chinstrap")
else:
    print("Gentoo")
'''),
        ],
        tasks=[
            dict(id='i2a', type='out', topic='if', code='''
x = 7
if x > 5:
    print("да")
else:
    print("нет")
''', wrong=['нет', 'да\nнет', '!err']),
            dict(id='i2b', type='out', topic='cmp', code='''
x = 5
if x > 5:
    print("больше")
else:
    print("не больше")
''', wrong=['больше', 'больше\nне больше', '!err']),
            dict(id='i2c', type='out', topic='indent', code='''
x = 3
if x == 3:
    print("три")
print("готово")
''', wrong=['три', 'готово', '!err']),
            dict(id='i2d', type='out', topic='indent', code='''
x = 2
if x > 5:
    print("A")
print("B")
''', wrong=['A\nB', 'A', '!err']),
            dict(id='i2e', type='out', topic='elif', code='''
m = 4000
if m > 4500:
    print("Gentoo")
elif m > 3500:
    print("Chinstrap")
else:
    print("Adelie")
''', wrong=['Gentoo', 'Adelie', 'Chinstrap\nAdelie']),
            dict(id='i2f', type='bug', topic='cmp', code='''
x = 10
if x = 10:
    print("десять")
'''),
            dict(id='i2g', type='bug', topic='indent', code='''
x = 1
if x > 0:
print("плюс")
'''),
            dict(id='i2h', type='parsons', topic='if', code='''
age = 15
if age >= 13:
    print("можно")
else:
    print("рано")
'''),
        ]),
    # ---------- Py 03: списки ----------
    'py-list': dict(
        demos=[
            dict(id='s3x', code='''
masses = [3750, 3800, 3250]
print(masses[0])
print(masses[2])
print(len(masses))
'''),
            dict(id='s3y', code='''
species = ["Adelie", "Gentoo"]
species.append("Chinstrap")
print(species)
print(species[-1])
'''),
            dict(id='s3z', code='''
masses = [3750, 3800, 3250]
print(sum(masses))
print(min(masses), max(masses))
masses[1] = 4000
print(masses)
'''),
        ],
        tasks=[
            dict(id='s3a', type='out', topic='index', code='''
a = [10, 20, 30]
print(a[1])
''', wrong=['10', '30', '!err']),
            dict(id='s3b', type='out', topic='list', code='''
a = [10, 20, 30]
print(len(a))
''', wrong=['2', '30', '60']),
            dict(id='s3c', type='out', topic='index', code='''
a = [10, 20, 30]
print(a[-1])
''', wrong=['10', '20', '!err']),
            dict(id='s3d', type='out', topic='list', code='''
a = [1, 2]
a.append(5)
print(a)
''', wrong=['[5, 1, 2]', '[1, 2]', '3']),
            dict(id='s3e', type='out', topic='list', code='''
a = [4, 1, 3]
print(sum(a), max(a))
''', wrong=['8', '4 8', '3 4']),
            dict(id='s3f', type='bug', topic='index', code='''
a = [5, 6]
print(a[0])
print(a[2])
'''),
            dict(id='s3g', type='bug', topic='list', code='''
a = [1, 2, 3
print(a)
'''),
            dict(id='s3h', type='parsons', topic='list', code='''
birds = ["Adelie"]
birds.append("Gentoo")
print(len(birds))
'''),
        ]),
    # ---------- Py 04: цикл for ----------
    'py-for': dict(
        demos=[
            dict(id='f4x', code='''
for name in ["Adelie", "Chinstrap", "Gentoo"]:
    print(name)
print("конец")
'''),
            dict(id='f4y', code='''
total = 0
for m in [3000, 4000, 5000]:
    total = total + m
print(total)
print(total / 3)
'''),
            dict(id='f4z', code='''
count = 0
for m in [3750, 5000, 4800, 3200]:
    if m > 4500:
        count = count + 1
print(count)
'''),
        ],
        tasks=[
            dict(id='f4a', type='out', topic='loop', code='''
for x in [1, 2, 3]:
    print(x * 2)
''', wrong=['6', '1\n2\n3', '2 4 6']),
            dict(id='f4b', type='out', topic='range', code='''
for i in range(3):
    print(i)
''', wrong=['1\n2\n3', '0\n1\n2\n3', '3']),
            dict(id='f4c', type='out', topic='sum', code='''
s = 0
for x in [5, 5, 5]:
    s = s + x
print(s)
''', wrong=['5\n10\n15', '5', '0']),
            dict(id='f4d', type='out', topic='sum', code='''
s = 0
for x in [5, 5, 5]:
    s = s + x
    print(s)
''', wrong=['15', '5\n5\n5', '!err']),
            dict(id='f4e', type='out', topic='count', code='''
n = 0
for m in [3000, 5000, 4800]:
    if m > 4500:
        n = n + 1
print(n)
''', wrong=['3', '1', '0']),
            dict(id='f4f', type='bug', topic='loop', code='''
for x in [1, 2]
    print(x)
'''),
            dict(id='f4g', type='bug', topic='sum', code='''
total = 0
for x in [1, 2]:
    total = total + y
print(total)
'''),
            dict(id='f4h', type='parsons', topic='sum', code='''
s = 0
for x in [2, 4, 6]:
    s = s + x
print(s / 3)
'''),
        ]),
    # ---------- Py 05: функции ----------
    'py-func': dict(
        demos=[
            dict(id='u5x', code='''
def hello(name):
    print("Привет,", name)

hello("Аня")
hello("Тимур")
'''),
            dict(id='u5y', code='''
def double(x):
    return x * 2

a = double(5)
print(a)
print(double(a))
'''),
            dict(id='u5z', code='''
def kind(mass):
    if mass > 4500:
        return "Gentoo"
    return "не Gentoo"

print(kind(5000))
print(kind(3500))
'''),
        ],
        tasks=[
            dict(id='u5a', type='out', topic='func', code='''
def add(a, b):
    return a + b
print(add(2, 3))
''', wrong=['23', 'add(2, 3)', '!err']),
            dict(id='u5b', type='out', topic='return', code='''
def f(x):
    return x + 1
print(f(f(1)))
''', wrong=['2', '1', '!err']),
            dict(id='u5c', type='out', topic='func', code='''
def show(x):
    print(x * 10)
show(2)
show(3)
''', wrong=['50', '20', '2\n3']),
            dict(id='u5d', type='out', topic='return', code='''
def g(x):
    print(x)
r = g(5)
print(r)
''', wrong=['5\n5', '5', 'None']),
            dict(id='u5e', type='out', topic='return', code='''
def area(w, h):
    return w * h
print(area(3, 4) + 1)
''', wrong=['12', '8', '!err']),
            dict(id='u5f', type='bug', topic='func', code='''
print(square(3))
def square(x):
    return x * x
'''),
            dict(id='u5g', type='bug', topic='func', code='''
def half(x):
    return x / 2
print(half())
'''),
            dict(id='u5h', type='parsons', topic='return', code='''
def triple(x):
    return x * 3
print(triple(4))
'''),
        ]),
    # ---------- Py 06: таблица pandas ----------
    'py-pandas': dict(
        demos=[
            dict(id='d6x', code=TABLE + '''print(df)
print(len(df))
'''),
            dict(id='d6y', code=TABLE + '''print(df["mass"])
print(df["mass"].mean())
print(df["mass"].max())
'''),
            dict(id='d6z', code=TABLE + '''big = df[df["mass"] > 3500]
print(big)
print(df["species"].value_counts())
'''),
        ],
        tasks=[
            dict(id='d6a', type='out', topic='df', code=TABLE + '''print(len(df))
''', wrong=['2', '6', '!err']),
            dict(id='d6b', type='out', topic='col', code=TABLE + '''print(df["mass"].mean())
''', wrong=['4000', '12000', '3000.0']),
            dict(id='d6c', type='out', topic='col', code=TABLE + '''print(df["species"][1])
''', wrong=['Adelie', 'species', '!err']),
            dict(id='d6d', type='out', topic='filter', code=TABLE + '''big = df[df["mass"] > 3500]
print(len(big))
''', wrong=['1', '3', '0']),
            dict(id='d6e', type='out', topic='col', code=TABLE + '''print(df["mass"].max() - df["mass"].min())
''', wrong=['5000', '3000', '8000']),
            dict(id='d6f', type='bug', topic='col', code=TABLE + '''print(df["Mass"].mean())
'''),
            dict(id='d6g', type='bug', topic='df', code='''df = pd.DataFrame({
    "mass": [3000, 5000],
})
print(df)
'''),
            dict(id='d6h', type='parsons', topic='col', code='''
import pandas as pd
df = pd.DataFrame({"mass": [3000, 5000]})
m = df["mass"].mean()
print(m)
'''),
        ]),
}


def value(v):
    """(показ, тип) для переменной; None — не показывать (модули)."""
    if isinstance(v, types.ModuleType):
        return None
    if isinstance(v, types.FunctionType):
        return ['', 'function']
    t = type(v).__name__
    if t == 'DataFrame':
        return [f'{v.shape[0]} × {v.shape[1]}', 'DataFrame']
    if t == 'Series':
        return [str(len(v)), 'Series']
    r = repr(v)
    return [r if len(r) <= 40 else r[:37] + '…', t]


def snapshot(names):
    out = []
    for k, v in names.items():
        if k.startswith('__'):
            continue
        s = value(v)
        if s is not None:
            out.append([k] + s)
    return out


def trace(src):
    """Шаги программы: перед каждой строкой — номер строки, переменные, напечатанное; в конце — итог."""
    code = compile(src, '<demo>', 'exec')
    # Python 3.12 останавливается и на строках внутри многострочного выражения (словарь для DataFrame);
    # показываем шаги только на строках, где начинается команда
    starts = {n.lineno for n in ast.walk(ast.parse(src)) if isinstance(n, ast.stmt)}
    g = {'__name__': '__demo__'}
    out, steps = io.StringIO(), []

    def step(frame, **extra):
        local = None
        if frame.f_code.co_name != '<module>':
            local = {'fn': frame.f_code.co_name, 'vars': snapshot(frame.f_locals)}
        st = dict(line=frame.f_lineno, vars=snapshot(g), local=local, out=out.getvalue(), **extra)
        if steps and steps[-1] == st:
            return                           # та же строка ещё раз (после многострочного выражения) — шаг не нужен
        steps.append(st)

    def tr(frame, event, arg):
        if frame.f_code.co_filename != '<demo>':
            return None                      # внутрь pandas и встроенных функций не заходим
        if event == 'line' and frame.f_lineno in starts:
            step(frame)
        elif event == 'return' and frame.f_code.co_name != '<module>':
            r = value(arg)
            step(frame, ret=r[0] if r and r[1] != 'function' else repr(arg))
        return tr

    sys.settrace(tr)
    try:
        with contextlib.redirect_stdout(out):
            exec(code, g)
    finally:
        sys.settrace(None)
    steps.append(dict(line=0, vars=snapshot(g), local=None, out=out.getvalue()))
    return steps


def main():
    data = {}
    for page, spec in PAGES.items():
        demos = []
        for d in spec['demos']:
            code = d['code'].strip('\n')
            demos.append(dict(id=d['id'], code=code, steps=trace(code)))
        data[page] = dict(demos=demos, tasks=[build(t) for t in spec['tasks']])

    ids = [d['id'] for s in PAGES.values() for d in s['demos'] + s['tasks']]
    assert len(ids) == len(set(ids)), 'повтор id'

    # Страницы раздела в каталоге (поле py) = страницы с заданиями
    cat = open(os.path.join(ROOT, 'assets', 'catalog.js'), encoding='utf-8').read()
    listed = re.findall(r"id:\s*'(py-[a-z]+)'", cat)
    assert sorted(listed) == sorted(PAGES), f'в catalog.js страницы {listed}, а заданий — к {sorted(PAGES)}'

    # Все тексты есть в STR.ru страниц
    for page, spec in PAGES.items():
        src = open(os.path.join(ROOT, 'viz', page, 'index.html'), encoding='utf-8').read()
        ru = src[src.index('ru: {'):]
        need = []
        for d in spec['demos']:
            need += ['ex_' + d['id'], 'exb_' + d['id']]
        for t in spec['tasks']:
            need += ['x_' + t['id'], 'topic_' + t['topic']] + (['g_' + t['id']] if t['type'] == 'parsons' else [])
        for k in need:
            assert re.search(r'\b' + k + r':', ru), f'в STR.ru страницы {page} нет ключа {k}'

    js = ('/* Раздел «Python с нуля»: пошаговые примеры и задания. Сгенерировано tools/build_pystart.py — руками не править.\n'
          '   Шаги примеров записаны настоящим Python (sys.settrace), ответы заданий — тоже. */\n'
          'window.PYSTART = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n')
    with open(os.path.join(ROOT, 'data', 'pystart.js'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(js)
    for page, d in data.items():
        info = [f"{x['id']} шагов {len(x['steps'])}" for x in d['demos']]
        for t in d['tasks']:
            info.append(f"{t['id']} строка {t['line']} {t['err']}" if t['type'] == 'bug'
                        else f"{t['id']} порядков {len(t['orders'])}" if t['type'] == 'parsons'
                        else f"{t['id']} = {t['choices'][0]!r}")
        print(page + ': ' + '; '.join(info))
    print(f'data/pystart.js записан ({len(js) // 1024} КБ)')


if __name__ == '__main__':
    main()
