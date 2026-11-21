"""Собирает раздел «Учебник» сайта из книг в формате Word (.docx).

Запуск (из папки ml-viz):
    python tools/build_book.py
    python tools/build_book.py --ml "путь/к/книге1.docx" --ml2 "путь/к/книге2.docx"

Книгу правят в Word, потом запускают скрипт — страницы book/ml/*.html и book/ml2/*.html пересобираются.
Руками сгенерированные страницы не правим: следующая сборка их перезапишет.

Как читается docx (так свёрстаны книги):
  - Заголовки 1/2/3 уровня → страница / h2 / h3. Каждый заголовок 1 уровня = отдельная страница.
  - Абзацы с заливкой подряд → блок: строки шрифтом Consolas = код (<pre>), остальное = врезка
    («Аналогия 💡», «Внимание ⚠️»…). Полностью жирный абзац в заливке начинает новую врезку.
  - Абзац «ФАЗА N» / «ЧАСТЬ N» между главами → название фазы для следующих глав.
  - Списки, таблицы, жирный, курсив и `код` внутри текста сохраняются.
Только стандартная библиотека Python: без pip, работает и без интернета.
"""
import argparse
import html
import os
import re
import shutil
import zipfile
from xml.etree import ElementTree as ET

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = r'D:\ML begin\lesson-01-ml-magic'
DEFAULT_ML = os.path.join(SRC, 'books', 'новая часть книги', 'МАШИННОЕ_ОБУЧЕНИЕ_(главы1-33).docx')
DEFAULT_ML2 = os.path.join(SRC, 'books', 'новая часть книги', 'МАШИННОЕ_ОБУЧЕНИЕ_уровень2_коды-проверены.docx')
DEFAULT_NB = os.path.join(SRC, 'books', 'новая часть книги', 'Colab_ноутбуки_ML_главы_1-33.zip')
DEFAULT_PY = os.path.join(SRC, 'python', 'Uchebnik_Python_full.html')

PHASE_RE = re.compile(r'^(ФАЗА|ЧАСТЬ)\s+\d+$')
CALLOUT_KIND = [('💡', 'analogy'), ('⚠', 'warn'), ('🎯', 'goal'), ('ℹ', 'info'), ('⭐', 'star'), ('💬', 'talk')]


def esc(s):
    return html.escape(s, quote=False)


# ---------------------------------------------------------------- чтение docx
class Docx:
    def __init__(self, path):
        z = zipfile.ZipFile(path)
        self.body = ET.fromstring(z.read('word/document.xml')).find(W + 'body')
        # Стиль → уровень заголовка (по имени стиля «heading N»: id стиля в разных книгах разный)
        self.heading = {}
        styles = ET.fromstring(z.read('word/styles.xml'))
        for st in styles.iter(W + 'style'):
            name = st.find(W + 'name')
            m = re.match(r'heading (\d)', (name.get(W + 'val') if name is not None else '').lower())
            if m:
                self.heading[st.get(W + 'styleId')] = int(m.group(1))
        # Нумерация списков: numId → «decimal» / «bullet»
        self.numfmt = {}
        if 'word/numbering.xml' in z.namelist():
            num = ET.fromstring(z.read('word/numbering.xml'))
            absfmt = {}
            for a in num.iter(W + 'abstractNum'):
                lvl = a.find(W + 'lvl')
                f = lvl.find(W + 'numFmt') if lvl is not None else None
                absfmt[a.get(W + 'abstractNumId')] = f.get(W + 'val') if f is not None else 'bullet'
            for n in num.iter(W + 'num'):
                a = n.find(W + 'abstractNumId')
                self.numfmt[n.get(W + 'numId')] = absfmt.get(a.get(W + 'val') if a is not None else '', 'bullet')


def on(el):
    """<w:b/> включён, если нет w:val="0"/"false"."""
    return el is not None and el.get(W + 'val') not in ('0', 'false')


def runs(p):
    """Кусочки текста абзаца: [(текст, жирный, курсив, код)]."""
    out = []
    for r in p.iter(W + 'r'):
        rpr = r.find(W + 'rPr')
        b = i = code = False
        if rpr is not None:
            b, i = on(rpr.find(W + 'b')), on(rpr.find(W + 'i'))
            f = rpr.find(W + 'rFonts')
            code = f is not None and 'consolas' in (f.get(W + 'ascii') or '').lower()
        for c in r:
            if c.tag == W + 't':
                out.append([c.text or '', b, i, code])
            elif c.tag == W + 'tab':
                out.append(['    ', b, i, code])
            elif c.tag == W + 'br' and c.get(W + 'type') != 'page':
                out.append(['\n', b, i, code])
    return out


def ptext(p):
    return ''.join(r[0] for r in runs(p))


def pprops(doc, p):
    ppr = p.find(W + 'pPr')
    st = shd = num = None
    if ppr is not None:
        s = ppr.find(W + 'pStyle')
        st = s.get(W + 'val') if s is not None else None
        shd = ppr.find(W + 'shd') is not None
        n = ppr.find(W + 'numPr')
        if n is not None:
            nid = n.find(W + 'numId')
            num = doc.numfmt.get(nid.get(W + 'val') if nid is not None else '', 'bullet')
    return doc.heading.get(st), bool(shd), num


def all_code(rs):
    txt = [r for r in rs if r[0].strip()]
    return bool(txt) and all(r[3] for r in txt)


def all_bold(rs):
    txt = [r for r in rs if r[0].strip()]
    return bool(txt) and all(r[1] for r in txt)


def inline(rs):
    """Кусочки → HTML: соседние кусочки с одинаковым оформлением склеиваем."""
    merged = []
    for t, b, i, c in rs:
        if merged and merged[-1][1:] == [b, i, c]:
            merged[-1][0] += t
        else:
            merged.append([t, b, i, c])
    out = []
    for t, b, i, c in merged:
        s = esc(t).replace('\n', '<br>')
        if not t.strip():
            out.append(s)
            continue
        if c:
            s = '<code>' + s + '</code>'
        if i:
            s = '<i>' + s + '</i>'
        if b:
            s = '<b>' + s + '</b>'
        out.append(s)
    return ''.join(out).strip()


# ---------------------------------------------------------------- разбор на страницы
def slugify_title(title, n):
    m = re.match(r'Глава (\d+)\.', title)
    if m:
        return 'ch%02d' % int(m.group(1)), int(m.group(1))
    m = re.match(r'Приложение ([A-ZА-Я])\.', title)
    if m:
        return 'app-' + m.group(1).lower(), None
    return 'page%02d' % n, None


def parse(path):
    doc = Docx(path)
    blocks = list(doc.body)
    cover, pages, phase = [], [], None
    cur = None
    phase_mode = None          # собираем текст страницы-разделителя «ФАЗА N»
    other_n = 0
    i = 0
    while i < len(blocks):
        el = blocks[i]
        if el.tag == W + 'tbl':
            if cur is not None and phase_mode is None:
                cur['body'].append(table_html(doc, el))
            i += 1
            continue
        if el.tag != W + 'p':
            i += 1
            continue
        level, shd, num = pprops(doc, el)
        rs = runs(el)
        text = ''.join(r[0] for r in rs).strip()
        if level == 1:
            phase_mode = None
            if text == 'Содержание':
                cur = None              # оглавление книги строим сами
                i += 1
                continue
            other_n += 1
            slug, chap = slugify_title(text, other_n)
            cur = {'title': text, 'slug': slug, 'chapter': chap, 'phase': phase if chap else None, 'body': []}
            pages.append(cur)
            i += 1
            continue
        if not pages and cur is None and level is None and not shd:
            # Обложка: абзацы до оглавления
            if text and not pages:
                cover.append(text)
            i += 1
            continue
        if PHASE_RE.match(text) and not shd and level is None:
            phase_mode = {'label': text.title(), 'name': '', 'about': []}
            phase = phase_mode
            i += 1
            continue
        if phase_mode is not None:
            if text:
                if not phase_mode['name']:
                    phase_mode['name'] = text
                else:
                    phase_mode['about'].append(text)
            i += 1
            continue
        if cur is None:
            i += 1
            continue
        if level in (2, 3):
            cur['body'].append('<h%d>%s</h%d>' % (level, inline(rs), level))
            i += 1
            continue
        if shd:
            group = []
            while i < len(blocks) and blocks[i].tag == W + 'p' and pprops(doc, blocks[i])[1] and pprops(doc, blocks[i])[0] is None:
                group.append(blocks[i])
                i += 1
            cur['body'].extend(shaded_html(group))
            continue
        if num:
            kind = num
            items = []
            while i < len(blocks) and blocks[i].tag == W + 'p':
                lv, sh, nm = pprops(doc, blocks[i])
                if not nm or sh or lv:
                    break
                items.append('<li>%s</li>' % inline(runs(blocks[i])))
                i += 1
            tag = 'ol' if kind == 'decimal' else 'ul'
            cur['body'].append('<%s>%s</%s>' % (tag, ''.join(items), tag))
            continue
        if text:
            if all_code(rs) and '\n' not in text and len(text) < 200 and text.count(' ') < 25 and not re.search('[а-яё]{4,} [а-яё]{4,}', text.split('#')[0], re.I):
                cur['body'].append('<pre><code>%s</code></pre>' % esc(ptext(el)))
            else:
                cur['body'].append('<p>%s</p>' % inline(rs))
        i += 1
    return cover, pages


def shaded_html(group):
    """Подряд идущие абзацы с заливкой → код и врезки."""
    out, code, box = [], [], None

    def flush_code():
        if code:
            while code and not code[-1].strip():
                code.pop()
            if code:
                out.append('<pre><code>%s</code></pre>' % esc('\n'.join(code)))
            del code[:]

    def flush_box():
        nonlocal box
        if box and (box['title'] or box['body']):
            kind = 'note'
            for mark, k in CALLOUT_KIND:
                if mark in box['title']:
                    kind = k
                    break
            out.append('<aside class="callout %s">%s%s</aside>' % (
                kind, ('<p class="callout-title">%s</p>' % box['title']) if box['title'] else '', ''.join(box['body'])))
        box = None

    for p in group:
        rs = runs(p)
        text = ''.join(r[0] for r in rs)
        is_code = all_code(rs) or (code and not text.strip())
        if is_code:
            flush_box()
            code.append(text.replace('\u00a0', ' ').rstrip())
            continue
        if not text.strip():
            continue
        flush_code()
        if all_bold(rs):
            flush_box()
            box = {'title': esc(text.strip()), 'body': []}
        else:
            if box is None:
                box = {'title': '', 'body': []}
            box['body'].append('<p>%s</p>' % inline(rs))
    flush_code()
    flush_box()
    return out


def table_html(doc, tbl):
    rows = []
    for k, tr in enumerate(tbl.findall(W + 'tr')):
        cells = []
        for tc in tr.findall(W + 'tc'):
            parts = [inline(runs(p)) for p in tc.findall(W + 'p')]
            cells.append('<br>'.join(x for x in parts if x))
        tag = 'th' if k == 0 else 'td'
        rows.append('<tr>%s</tr>' % ''.join('<%s>%s</%s>' % (tag, c, tag) for c in cells))
    return '<div class="tbl-wrap"><table class="book-table">%s</table></div>' % ''.join(rows)


# ---------------------------------------------------------------- вывод HTML
PAGE = '''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} · {book} · Лаборатория ML</title>
  <link rel="stylesheet" href="../../assets/style.css">
</head>
<body>
  <!-- Страница сгенерирована tools/build_book.py из книги Word. Не правьте руками: пересоберите. -->
  <header id="site-header"></header>
  <main class="wrap book-page" data-book="{key}"{chapter_attr}>
    <p class="eyebrow">{eyebrow}</p>
    <h1>{title}</h1>
    <div id="bookLinks"></div>
    <article class="book-text">
{body}
    </article>
    <nav class="book-nav" aria-label="Главы">
      {prev}<a class="btn" href="index.html">Оглавление</a>{next}
    </nav>
  </main>
  <footer class="site-footer"><div class="wrap">{book} · раздел «Учебник» Лаборатории ML.</div></footer>
  <script src="../../assets/core.js"></script>
  <script src="../../assets/catalog.js"></script>
  <script>MLViz.renderHeader('../../'); MLViz.renderBook();</script>
</body>
</html>
'''

TOC = '''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{book} · Учебник · Лаборатория ML</title>
  <link rel="stylesheet" href="../../assets/style.css">
</head>
<body>
  <!-- Страница сгенерирована tools/build_book.py из книги Word. Не правьте руками: пересоберите. -->
  <header id="site-header"></header>
  <main class="wrap book-page">
    <p class="eyebrow">Учебник</p>
    <h1>{book}</h1>
    <p class="lead">{sub}</p>
    <p style="margin-top:14px"><a class="btn" href="../index.html">‹ Все учебники</a></p>
{toc}
  </main>
  <footer class="site-footer"><div class="wrap">{book} · раздел «Учебник» Лаборатории ML.</div></footer>
  <script src="../../assets/core.js"></script>
  <script src="../../assets/catalog.js"></script>
  <script>MLViz.renderHeader('../../');</script>
</body>
</html>
'''


def build_book(key, path, book_title):
    cover, pages = parse(path)
    out_dir = os.path.join(ROOT, 'book', key)
    if os.path.isdir(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)
    sub = ' · '.join(esc(c) for c in cover[1:4])
    for k, pg in enumerate(pages):
        prev = '<a class="btn" href="%s.html">‹ %s</a>' % (pages[k - 1]['slug'], esc(short(pages[k - 1]['title']))) if k else ''
        nxt = '<a class="btn" href="%s.html">%s ›</a>' % (pages[k + 1]['slug'], esc(short(pages[k + 1]['title']))) if k + 1 < len(pages) else ''
        ph = pg['phase']
        eyebrow = 'Учебник' + (' · %s · %s' % (ph['label'], esc(ph['name'])) if ph else '')
        with open(os.path.join(out_dir, pg['slug'] + '.html'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(PAGE.format(title=esc(pg['title']), book=esc(book_title), key=key, eyebrow=eyebrow,
                                chapter_attr=(' data-chapter="%d"' % pg['chapter']) if pg['chapter'] else '',
                                body='\n'.join('      ' + b for b in pg['body']), prev=prev, next=nxt))
    # Оглавление: вступление → фазы с главами → приложения
    toc, last_phase, opened = [], None, False

    def open_list(title, about=''):
        nonlocal opened
        if opened:
            toc.append('</ol></section>')
        toc.append('<section class="section book-toc"><h2>%s</h2>%s<ol>' % (title, ('<p class="note">%s</p>' % about) if about else ''))
        opened = True

    for pg in pages:
        if pg['chapter']:
            ph = pg['phase']
            if ph is not last_phase:
                open_list('%s · %s' % (ph['label'], esc(ph['name'])) if ph else 'Главы', esc(' '.join(ph['about'][:1])) if ph else '')
                last_phase = ph
        elif pg['slug'].startswith('app-'):
            if last_phase != 'app':
                open_list('Приложения')
                last_phase = 'app'
        elif last_phase is None:
            open_list('Перед началом')
            last_phase = 'front'
        elif last_phase not in ('front', 'app', 'tail'):
            open_list('После глав')
            last_phase = 'tail'
        toc.append('<li><a href="%s.html">%s</a></li>' % (pg['slug'], esc(pg['title'])))
    if opened:
        toc.append('</ol></section>')
    with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(TOC.format(book=esc(book_title), sub=sub, toc='\n'.join('    ' + t for t in toc)))
    print('%s: %d страниц' % (key, len(pages)))
    return pages


def short(title):
    m = re.match(r'(Глава \d+|Приложение [A-ZА-Я])\.', title)
    return m.group(1) if m else (title if len(title) < 28 else title[:26] + '…')


def copy_notebooks(zip_path):
    """Ноутбуки к главам 1–33 → notebooks/chNN.ipynb (латинские имена: их проще открыть в Colab по ссылке)."""
    out = os.path.join(ROOT, 'notebooks')
    os.makedirs(out, exist_ok=True)
    z = zipfile.ZipFile(zip_path)
    n = 0
    for zi in z.infolist():
        name = zi.filename
        if not zi.flag_bits & 0x800:      # имя в старой кодировке zip (cp437)
            try:
                name = name.encode('cp437').decode('utf-8')
            except UnicodeError:
                pass
        m = re.search(r'Глава_(\d+)_.*\.ipynb$', name)
        if m:
            with open(os.path.join(out, 'ch%02d.ipynb' % int(m.group(1))), 'wb') as f:
                f.write(z.read(zi))
            n += 1
    print('notebooks: %d' % n)


def copy_python(src):
    """Учебник Python — как есть, только без внешних шрифтов (офлайн) и со ссылкой обратно на сайт."""
    h = open(src, encoding='utf-8').read()
    h = re.sub(r"@import url\('https://fonts\.googleapis\.com[^)]*\);", '', h)
    # Без названия организации: на сайте учебник не привязан к школе.
    # Подпись стоит в двух местах — жирным в конце строки «9 класс · …» на обложках частей и в колонтитуле (span.brand).
    h = re.sub(r'(<div class="who"[^>]*>[^<]*?)\s*·\s*<b>[^<]*</b>', r'\1', h)
    h = re.sub(r'<span class="brand">[^<]*</span>', '', h)
    assert '<span class="brand">' not in h and not re.search(r'<div class="who"[^>]*>[^<]*<b>', h), 'подпись организации осталась'
    back = ('<a href="../index.html" style="position:fixed;left:12px;top:12px;z-index:50;background:#17132E;color:#EEEAFB;'
            'padding:10px 14px;border-radius:10px;font:600 15px Calibri,system-ui,sans-serif;text-decoration:none">‹ Учебники</a>')
    h = h.replace('<body>', '<body>\n' + back, 1)
    os.makedirs(os.path.join(ROOT, 'book', 'python'), exist_ok=True)
    with open(os.path.join(ROOT, 'book', 'python', 'index.html'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(h)
    print('python: ok')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--ml', default=DEFAULT_ML)
    ap.add_argument('--ml2', default=DEFAULT_ML2)
    ap.add_argument('--notebooks', default=DEFAULT_NB)
    ap.add_argument('--python', default=DEFAULT_PY)
    a = ap.parse_args()
    build_book('ml', a.ml, 'Машинное обучение для начинающих')
    build_book('ml2', a.ml2, 'Машинное обучение. Уровень 2')
    copy_notebooks(a.notebooks)
    copy_python(a.python)
