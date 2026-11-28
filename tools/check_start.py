"""Сверка теста «С чего начать» (start/index.html) с настоящим Python.

Вопросы лежат в странице между метками /* data:start */ … /* data:end */ (строгий JSON).
- Вопрос с кодом: программа запускается, её вывод должен совпасть с верным вариантом
  и не совпасть ни с одним неверным.
- Вопрос по математике: выражение check считается Python, результат = верный вариант.
- Тексты вопроса (q_<id>), объяснения (x_<id>) и варианты «@ключ» должны быть в STR.
- Страница-совет (page) должна быть в catalog.js.

Запуск: python tools/check_start.py
"""
import contextlib
import io
import json
import math  # noqa: F401 — нужен выражениям check
import re
import statistics  # noqa: F401
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
page = (ROOT / 'start' / 'index.html').read_text(encoding='utf-8')
catalog = (ROOT / 'assets' / 'catalog.js').read_text(encoding='utf-8')

data = json.loads(page.split('/* data:start */')[1].split('/* data:end */')[0])
keys = set(re.findall(r"^\s*(\w+):", page, re.M)) | set(re.findall(r",\s*(\w+):\s*'", page))
ids = set(re.findall(r"id:\s*'([\w-]+)'", catalog))

errors = []
for q in data:
    qid, opts, right = q['id'], q['opts'], q['right']
    for k in ['q_' + qid, 'x_' + qid] + [o[1:] for o in opts if o.startswith('@')]:
        if k not in keys:
            errors.append(f'{qid}: нет ключа STR {k}')
    if q['page'] not in ids:
        errors.append(f'{qid}: страницы {q["page"]} нет в catalog.js')
    if len(set(opts)) != len(opts):
        errors.append(f'{qid}: одинаковые варианты')

    if 'code' in q:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            exec(q['code'], {})
        got = buf.getvalue().strip()
    elif 'check' in q:
        v = eval(q['check'])
        got = f'{v:g}' + q.get('unit', '')
    else:
        print(f'{qid}: вопрос без проверки (про компьютер) — верный вариант «{opts[right]}»')
        continue

    if got != opts[right]:
        errors.append(f'{qid}: Python даёт «{got}», а верным отмечено «{opts[right]}»')
    others = [o for i, o in enumerate(opts) if i != right and o == got]
    if others:
        errors.append(f'{qid}: вывод совпадает с неверным вариантом')
    print(f'{qid}: {got!r} — ок' if got == opts[right] else f'{qid}: ОШИБКА')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
print(f'Все {len(data)} вопросов сходятся.')
