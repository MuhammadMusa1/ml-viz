/* Лаборатория ML — общие функции для всех страниц.
   Подключается обычным <script src>, без модулей и сборки: так страницы открываются и с file:// (флешка в классе). */
(function () {
  'use strict';

  // ---------- Язык ----------
  // Сейчас только 'ru'. Таджикский ('tg') добавляется словарями в тех же объектах STR — разметку трогать не нужно.
  var LANGS = ['ru', 'tg'];    // таджикский — перевод из i18n/tg (tools/i18n.js)
  var LANG_NAMES = { ru: 'Рус', tg: 'Тоҷ' };

  function readLang() {
    var fromUrl = new URLSearchParams(location.search).get('lang');
    if (fromUrl && LANGS.indexOf(fromUrl) !== -1) {
      // Язык из ссылки запоминаем: иначе на следующем уроке (ссылки в шапке без ?lang) он сбросился бы
      try { localStorage.setItem('mlviz.lang', fromUrl); } catch (e) {}
      return fromUrl;
    }
    try {
      var saved = localStorage.getItem('mlviz.lang');
      if (saved && LANGS.indexOf(saved) !== -1) return saved;
    } catch (e) { /* file:// или приватный режим — просто русский */ }
    return 'ru';
  }
  var lang = readLang();

  // t(STR, 'key', {n: 5}) -> строка на текущем языке, с запасным русским вариантом и подстановкой {n}
  function t(dict, key, vars) {
    var s = (dict[lang] && dict[lang][key]) || (dict.ru && dict.ru[key]) || key;
    if (vars) s = s.replace(/\{(\w+)\}/g, function (_, k) { return vars[k] != null ? vars[k] : ''; });
    return s;
  }

  // Заполняет все элементы с data-i18n="key" (текст) и data-i18n-html="key" (разметка)
  function applyI18n(dict, root) {
    root = root || document;
    root.querySelectorAll('[data-i18n]').forEach(function (el) { el.textContent = t(dict, el.dataset.i18n); });
    root.querySelectorAll('[data-i18n-html]').forEach(function (el) { el.innerHTML = t(dict, el.dataset.i18nHtml); });
    document.documentElement.lang = lang;
    // Название вкладки браузера: в HTML оно русское, на другом языке берём заголовок страницы из перевода
    if (root === document && lang !== 'ru' && dict[lang] && dict[lang].title) {
      document.title = (dict[lang].title + ' · ' + t(UI, 'brand')).replace(/<[^>]+>/g, '');
    }
    if (root === document) decorateTerms();
  }

  function setLang(l) {
    try { localStorage.setItem('mlviz.lang', l); } catch (e) {}
    var u = new URL(location.href); u.searchParams.set('lang', l); location.href = u.toString();
  }

  // ---------- Шапка ----------
  var UI = {
    ru: { all: 'Все уроки', brand: 'Лаборатория <b>ML</b>', lesson: 'Урок {n}', lessonShort: 'Урок {n} ({k}/{m})',
          lessonPart: 'Урок {n} · часть {k} из {m}', prev: 'Предыдущий урок: {t}', next: 'Следующий урок: {t}', home: 'Лаборатория ML — на главную',
          mythsTitle: 'Типичные ошибки новичка', mythSeems: 'Кажется:', mythTruth: 'На самом деле:',
          nextTitle: 'Что дальше', nextGo: 'Дальше: {l} · {t} ›', toHome: 'На главную ›',
          doneYes: '✓ Урок пройден: ты доиграл игру до конца. Отметка видна на главной.',
          doneNo: 'Доиграй игру на этой странице до конца — и урок отметится как пройденный на главной.',
          book: 'Учебник', readChapter: '📖 Глава {n} учебника', colab: 'Открыть ноутбук в Colab',
          bookLinksTitle: 'К этой главе', vizLink: '🧪 Интерактив: {l} · {t}', copy: 'Скопировать', copied: 'Скопировано ✓' },
    tg: {"all":"Ҳамаи дарсҳо","brand":"Лабораторияи <b>ML</b>","lesson":"Дарси {n}","lessonShort":"Дарси {n} ({k}/{m})","lessonPart":"Дарси {n} · қисми {k} аз {m}","prev":"Дарси гузашта: {t}","next":"Дарси оянда: {t}","home":"Лабораторияи ML — ба саҳифаи асосӣ","mythsTitle":"Хатоҳои маъмули навкор","mythSeems":"Ба назар мерасад:","mythTruth":"Дар асл:","nextTitle":"Баъд чӣ?","nextGo":"Баъд: {l} · {t} ›","toHome":"Ба саҳифаи асосӣ ›","doneYes":"✓ Дарс гузашта шуд: ту бозиро то охир бозидӣ. Нишона дар саҳифаи асосӣ намоён аст.","doneNo":"Бозии ин саҳифаро то охир бозӣ кун — он гоҳ дарс дар саҳифаи асосӣ ҳамчун гузашташуда қайд мешавад.","book":"Китоби дарсӣ","readChapter":"📖 Боби {n}-и китоби дарсӣ","colab":"Кушодани дафтар дар Colab","bookLinksTitle":"Ба ин боб","vizLink":"🧪 Интерактив: {l} · {t}","copy":"Нусхабардорӣ","copied":"Нусхабардорӣ шуд ✓"}
  };

  // Номер страницы в уроке: на один урок курса бывает несколько страниц (урок 17 — три).
  // Возвращает {n, k, m}: урок n, страница k из m. Считается по каталогу, руками номера не пишем.
  function lessonPart(it) {
    var same = [];
    (window.CATALOG || []).forEach(function (ph) { ph.items.forEach(function (x) { if (x.lesson === it.lesson) same.push(x.id); }); });
    return { n: it.lesson, k: same.indexOf(it.id) + 1, m: same.length };
  }
  // «Урок 5» или «Урок 17 · часть 1 из 3» (short — коротко для кнопок шапки: «Урок 17 (1/3)»)
  function lessonLabel(it, short) {
    var p = lessonPart(it);
    return p.m > 1 ? t(UI, short ? 'lessonShort' : 'lessonPart', p) : t(UI, 'lesson', p);
  }

  // Соседние готовые уроки по каталогу (если catalog.js подключён) — учителю удобно листать на проекторе
  // id страницы урока из адреса. Ищем именно папку /viz/<id>/: на GitHub Pages сайт лежит в /ml-viz/,
  // и «viz/» встречается раньше нужного места (то же на флешке, если папка называется ml-viz)
  function pageId() {
    var m = location.pathname.match(/\/viz\/([^\/]+)\//);
    return m ? m[1] : null;
  }
  function readyItems() {
    var ready = [];
    (window.CATALOG || []).forEach(function (ph) { ph.items.forEach(function (it) { if (it.status === 'ready') ready.push(it); }); });
    return ready;
  }
  function tx(o) { return (o && (o[lang] || o.ru)) || ''; }
  // Фаза урока без номера: «Фаза 2 · Классические алгоритмы» → «Классические алгоритмы»
  function phaseName(it) {
    var name = '';
    (window.CATALOG || []).forEach(function (ph) { if (ph.items.indexOf(it) !== -1) name = tx(ph.phase); });
    return name.split(' · ').slice(1).join(' · ');
  }
  // Данные в атрибут title="…": кавычка в названии урока иначе обрежет атрибут
  function attr(s) { return String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;'); }

  // ---------- Прогресс ученика ----------
  // Урок «пройден», когда ученик доиграл игру страницы до конца. Хранится только в этом браузере (localStorage);
  // в приватном режиме или с запретом хранения просто ничего не отмечается — страница работает как обычно.
  var DONE_KEY = 'mlviz.done';
  function doneList() {
    try { var v = JSON.parse(localStorage.getItem(DONE_KEY) || '[]'); return Array.isArray(v) ? v : []; }
    catch (e) { return []; }
  }
  function markDone(id) {
    if (!id) return;
    var d = doneList();
    if (d.indexOf(id) === -1) { d.push(id); try { localStorage.setItem(DONE_KEY, JSON.stringify(d)); } catch (e) {} }
    updateDoneNote();
  }
  function resetDone() { try { localStorage.removeItem(DONE_KEY); } catch (e) {} }
  function updateDoneNote() {
    var n = document.getElementById('doneNote'), id = pageId();
    if (n && id) n.textContent = t(UI, doneList().indexOf(id) !== -1 ? 'doneYes' : 'doneNo');
  }

  // ---------- Учебник и Colab ----------
  // Глава N книги «Машинное обучение для начинающих» = урок N курса; ноутбук главы — notebooks/chNN.ipynb.
  function pad2(n) { return (n < 10 ? '0' : '') + n; }
  function chapterUrl(root, n) { return root + 'book/ml/ch' + pad2(n) + '.html'; }
  function colabUrl(n) { return window.COURSE && window.COURSE.colab ? window.COURSE.colab + 'ch' + pad2(n) + '.ipynb' : ''; }

  // На странице главы: какие интерактивы к ней есть и кнопка Colab
  function renderBook() {
    var main = document.querySelector('main[data-chapter]'), box = document.getElementById('bookLinks');
    if (main && box && main.dataset.book === 'ml') {
      var n = +main.dataset.chapter, links = [];
      readyItems().forEach(function (it) {
        if (it.lesson === n) links.push('<a class="btn" href="../../viz/' + it.id + '/index.html">' + t(UI, 'vizLink', { l: lessonLabel(it), t: tx(it.title) }) + '</a>');
      });
      var c = colabUrl(n);
      if (c) links.push('<a class="btn" href="' + c + '" target="_blank" rel="noopener">' + t(UI, 'colab') + ' ↗</a>');
      if (links.length) box.innerHTML = '<div class="book-links"><span class="sub">' + t(UI, 'bookLinksTitle') + '</span><div class="row">' + links.join('') + '</div></div>';
    }
    // Кнопка «Скопировать» у каждого блока кода: код из книги вставляют в Colab
    document.querySelectorAll('.book-text pre').forEach(function (pre) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'copy-code'; b.textContent = t(UI, 'copy');
      b.addEventListener('click', function () {
        var code = pre.querySelector('code').textContent;
        var done = function () { b.textContent = t(UI, 'copied'); setTimeout(function () { b.textContent = t(UI, 'copy'); }, 1500); };
        if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(code).then(done, function () {});
        else {   // file:// — буфер обмена через выделение текста
          var r = document.createRange(); r.selectNodeContents(pre.querySelector('code'));
          var sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(r);
          try { document.execCommand('copy'); done(); } catch (e) {}
          sel.removeAllRanges();
        }
      });
      pre.appendChild(b);
    });
  }

  // ---------- «Типичные ошибки новичка» и «Что дальше» ----------
  // Тексты лежат в catalog.js (myths, bridge), а не в каждой странице: так их удобно писать и переводить одним списком.
  // Ошибки встают перед «Для любопытных», «Что дальше» — в самый конец страницы.
  function renderLessonExtras(root) {
    var id = pageId(), main = document.querySelector('main');
    if (!id || !main) return;
    var ready = readyItems(), i = ready.map(function (it) { return it.id; }).indexOf(id);
    if (i === -1) return;
    var it = ready[i], next = ready[i + 1];
    // «Урок 5 · Классические алгоритмы» — из каталога, чтобы номер и фаза не расходились со страницами
    var eb = main.querySelector('.eyebrow');
    if (eb) eb.textContent = lessonLabel(it) + ' · ' + phaseName(it);
    var myths = it.myths && (it.myths[lang] || it.myths.ru);
    if (myths && myths.length) {
      var sec = document.createElement('section');
      sec.className = 'section myths';
      sec.innerHTML = '<h2>' + t(UI, 'mythsTitle') + '</h2><ul>' + myths.map(function (m) {
        return '<li><b>' + t(UI, 'mythSeems') + '</b> ' + m[0] + '<br><b>' + t(UI, 'mythTruth') + '</b> ' + m[1] + '</li>';
      }).join('') + '</ul>';
      var firstDetails = main.querySelector(':scope > details');
      main.insertBefore(sec, firstDetails || null);
    }
    var br = document.createElement('section');
    br.className = 'section bridge';
    br.innerHTML = '<h2>' + t(UI, 'nextTitle') + '</h2>' +
      (it.bridge ? '<p>' + tx(it.bridge) + '</p>' : '') +
      '<p class="row" style="margin:10px 0 0"><a class="btn" href="' + chapterUrl(root, it.lesson) + '">' + t(UI, 'readChapter', { n: it.lesson }) + '</a>' +
        (colabUrl(it.lesson) ? '<a class="btn" href="' + colabUrl(it.lesson) + '" target="_blank" rel="noopener">' + t(UI, 'colab') + ' ↗</a>' : '') + '</p>' +
      '<p class="note" id="doneNote"></p>' +
      '<p style="margin:12px 0 0">' + (next
        ? '<a class="btn" href="' + root + 'viz/' + next.id + '/index.html">' + t(UI, 'nextGo', { l: lessonLabel(next), t: tx(next.title) }) + '</a>'
        : '<a class="btn" href="' + root + 'index.html">' + t(UI, 'toHome') + '</a>') + '</p>';
    main.appendChild(br);
    updateDoneNote();
    var cl = document.getElementById('colabLink');
    if (cl && colabUrl(it.lesson)) { cl.href = colabUrl(it.lesson); cl.hidden = false; }
  }

  // ---------- Словарь терминов ----------
  // Первое упоминание термина на странице (в аналогии и текстовых разделах) становится кнопкой с подсказкой.
  // Кнопка, а не наведение мышью: на телефоне и проекторе наведения нет.
  var termPop = null, termBtn = null;
  function closeTerm(focusBack) {
    if (!termPop || termPop.hidden) return;
    termPop.hidden = true;
    if (termBtn) { termBtn.setAttribute('aria-expanded', 'false'); termBtn.removeAttribute('aria-describedby'); if (focusBack) termBtn.focus(); }
    termBtn = null;
  }
  function openTerm(btn) {
    var g = window.GLOSSARY[+btn.dataset.g];
    if (!termPop) {
      termPop = document.createElement('div');
      termPop.className = 'term-pop'; termPop.id = 'termPop'; termPop.setAttribute('role', 'tooltip'); termPop.hidden = true;
      document.body.appendChild(termPop);
    }
    closeTerm(false);
    termPop.innerHTML = '<b>' + tx(g.term) + '</b><br>' + tx(g.def);
    termPop.hidden = false;
    var r = btn.getBoundingClientRect(), w = termPop.offsetWidth;
    termPop.style.left = Math.max(8, Math.min(window.innerWidth - w - 8, r.left)) + window.scrollX + 'px';
    termPop.style.top = r.bottom + window.scrollY + 6 + 'px';
    termBtn = btn; btn.setAttribute('aria-expanded', 'true'); btn.setAttribute('aria-describedby', 'termPop');
  }
  function decorateTerms() {
    var G = window.GLOSSARY;
    if (!G || document.body.hasAttribute('data-terms')) return;
    document.body.setAttribute('data-terms', '');
    var roots = document.querySelectorAll('main .analogy-box, main .section, main details.box');
    var SKIP = /^(CODE|A|BUTTON|H1|H2|H3|SUMMARY|SCRIPT|STYLE)$/;
    function skipped(node, root) {
      for (var e = node.parentElement; e && e !== root; e = e.parentElement) if (SKIP.test(e.tagName)) return true;
      return false;
    }
    G.forEach(function (g, gi) {
      // Границы слова для кириллицы: \b в JS понимает только латиницу
      // На другом языке — своя основа слова (re_tg из перевода каталога); нет её — термин на этом языке не ищем
      var stem = lang === 'ru' ? g.re : g['re_' + lang];
      if (!stem) return;
      var re = new RegExp('(^|[^\\p{L}\\p{N}_])(' + stem + ')(?![\\p{L}\\p{N}_])', 'iu');
      for (var k = 0; k < roots.length; k++) {
        var w = document.createTreeWalker(roots[k], NodeFilter.SHOW_TEXT), node, m;
        while ((node = w.nextNode())) {
          if (skipped(node, roots[k]) || !(m = re.exec(node.data))) continue;
          var word = node.splitText(m.index + m[1].length);
          word.splitText(m[2].length);
          var b = document.createElement('button');
          b.type = 'button'; b.className = 'term'; b.dataset.g = gi; b.setAttribute('aria-expanded', 'false');
          b.textContent = word.data;
          word.parentNode.replaceChild(b, word);
          return;
        }
      }
    });
    document.addEventListener('click', function (e) {
      var b = e.target.closest && e.target.closest('button.term');
      if (b) { if (b === termBtn) closeTerm(false); else openTerm(b); return; }
      if (termPop && !termPop.contains(e.target)) closeTerm(false);
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeTerm(true); });
    window.addEventListener('resize', function () { closeTerm(false); });
  }

  function lessonNav(root) {
    var id = pageId();
    if (!id || !window.CATALOG) return '';
    var ready = readyItems();
    var i = ready.map(function (it) { return it.id; }).indexOf(id);
    if (i === -1) return '';
    function link(it, cls, label, tipKey) {
      var tip = attr(t(UI, tipKey, { t: tx(it.title) || it.id }));
      return '<a class="lesson-step ' + cls + '" href="' + root + 'viz/' + it.id + '/index.html" title="' +
        tip + '" aria-label="' + tip + '">' + label + '</a>';
    }
    return (i > 0 ? link(ready[i - 1], 'prev', '‹ ' + lessonLabel(ready[i - 1], true), 'prev') : '') +
           (i < ready.length - 1 ? link(ready[i + 1], 'next', lessonLabel(ready[i + 1], true) + ' ›', 'next') : '');
  }

  // Логотип: пингвин — герой всего курса (датасет Palmer Penguins). Рисунок в SVG, чтобы работал офлайн
  var LOGO_SVG =
    '<svg class="logo" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" aria-hidden="true">' +
      '<rect x="1" y="1" width="30" height="30" rx="9" fill="#261F4A" stroke="#3A3168"/>' +
      '<ellipse cx="16" cy="17.2" rx="8.6" ry="10.2" fill="#0F0C22" stroke="#A78BFA" stroke-width="1.3"/>' +
      '<path d="M8.2 17 Q5.6 20.5 7.4 24.2" fill="none" stroke="#A78BFA" stroke-width="1.3" stroke-linecap="round"/>' +
      '<path d="M23.8 17 Q26.4 20.5 24.6 24.2" fill="none" stroke="#A78BFA" stroke-width="1.3" stroke-linecap="round"/>' +
      '<ellipse cx="16" cy="20.3" rx="5.6" ry="6.6" fill="#EEEAFB"/>' +
      '<circle cx="13.2" cy="12.4" r="1.55" fill="#EEEAFB"/><circle cx="13.5" cy="12.6" r=".75" fill="#0F0C22"/>' +
      '<circle cx="18.8" cy="12.4" r="1.55" fill="#EEEAFB"/><circle cx="18.5" cy="12.6" r=".75" fill="#0F0C22"/>' +
      '<path d="M14.3 14.9 L17.7 14.9 L16 17.3 Z" fill="#FBBF24"/>' +
      '<ellipse cx="13" cy="27.4" rx="2.3" ry="1.05" fill="#FBBF24"/><ellipse cx="19" cy="27.4" rx="2.3" ry="1.05" fill="#FBBF24"/>' +
    '</svg>';
  var LOGO = LOGO_SVG;

  // Тот же пингвин — значком вкладки браузера (data-URL: без отдельного файла и без сети)
  function setFavicon() {
    if (document.querySelector('link[rel="icon"]')) return;
    var l = document.createElement('link');
    l.rel = 'icon'; l.type = 'image/svg+xml';
    l.href = 'data:image/svg+xml,' + encodeURIComponent(LOGO_SVG.replace(' class="logo"', '').replace(' aria-hidden="true"', ''));
    document.head.appendChild(l);
  }

  // root — относительный путь до корня сайта ('' для главной, '../../' для viz/xxx/)
  function renderHeader(root) {
    var h = document.getElementById('site-header');
    if (!h) return;
    var langBtns = LANGS.length > 1
      ? '<div class="lang-switch">' + LANGS.map(function (l) {
          return '<button type="button" data-lang="' + l + '" aria-pressed="' + (l === lang) + '">' + LANG_NAMES[l] + '</button>';
        }).join('') + '</div>'
      : '';
    setFavicon();
    // На странице урока в шапке ещё кнопки «‹ Урок N · Урок N ›»: на телефоне там остаётся только пингвин
    h.className = 'site-header' + (root ? ' sub-page' : '') + (pageId() ? ' in-lesson' : '');
    h.innerHTML =
      '<div class="wrap">' +
        '<a class="brand" href="' + root + 'index.html" aria-label="' + t(UI, 'home') + '">' + LOGO + '<span>' + t(UI, 'brand') + '</span></a>' +
        '<nav><a class="book-link" href="' + root + 'book/index.html">' + t(UI, 'book') + '</a>' +
          (root ? '<a class="all-link" href="' + root + 'index.html">' + t(UI, 'all') + '</a>' + lessonNav(root) : '') + '</nav>' +
        langBtns +
      '</div>';
    h.querySelectorAll('[data-lang]').forEach(function (b) {
      b.addEventListener('click', function () { setLang(b.dataset.lang); });
    });
    if (root) renderLessonExtras(root);
  }

  // ---------- Canvas ----------
  // Подгоняет canvas под ширину контейнера и плотность пикселей экрана (чётко на проекторе и телефоне).
  function fitCanvas(canvas, aspect) {
    var dpr = window.devicePixelRatio || 1;
    var w = canvas.parentElement.clientWidth - 20; // минус padding .stage
    var h = Math.round(w * aspect);
    canvas.style.height = h + 'px';
    canvas.width = Math.round(w * dpr);
    canvas.height = Math.round(h * dpr);
    // Картинка для программ экранного доступа: без роли многие из них не читают aria-label у canvas
    if (!canvas.hasAttribute('role')) canvas.setAttribute('role', 'img');
    var ctx = canvas.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    return { ctx: ctx, w: w, h: h };
  }

  // Линейная шкала: данные -> пиксели и обратно
  function scale(d0, d1, r0, r1) {
    var f = function (v) { return r0 + (v - d0) / (d1 - d0) * (r1 - r0); };
    f.invert = function (p) { return d0 + (p - r0) / (r1 - r0) * (d1 - d0); };
    return f;
  }

  // Координаты указателя внутри canvas в CSS-пикселях (мышь и тач)
  function pointer(canvas, ev) {
    var r = canvas.getBoundingClientRect();
    return { x: ev.clientX - r.left, y: ev.clientY - r.top };
  }

  // Детерминированный генератор случайных чисел (аналог random_state=42)
  function rng(seed) {
    var a = seed >>> 0;
    return function () {
      a = (a + 0x6D2B79F5) >>> 0;
      var x = Math.imul(a ^ (a >>> 15), 1 | a);
      x = (x + Math.imul(x ^ (x >>> 7), 61 | x)) ^ x;
      return ((x ^ (x >>> 14)) >>> 0) / 4294967296;
    };
  }

  function shuffle(arr, rand) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(rand() * (i + 1)); var tmp = a[i]; a[i] = a[j]; a[j] = tmp;
    }
    return a;
  }

  function cssVar(name) { return getComputedStyle(document.documentElement).getPropertyValue(name).trim(); }

  // ---------- Оси графиков (общие для всех страниц) ----------
  // Размер шрифта растёт с шириной графика: на проекторе 15–16 px, на телефоне не меньше 13 px.
  function fontPx(w) { return Math.round(Math.max(13, Math.min(16, w / 50))); }
  function range(a, b, step) {
    var r = [];
    for (var v = a; v <= b + 1e-9; v += step) r.push(Math.round(v * 1e6) / 1e6);
    return r;
  }
  // o: {w, h, pad, sx, sy, xTicks, yTicks, xLabel, yLabel, xGrid (по умолчанию true), xFmt, yFmt}
  function drawAxes(ctx, o) {
    var fs = fontPx(o.w), pad = o.pad;
    var fx = o.xFmt || String, fy = o.yFmt || String;
    ctx.save();
    ctx.strokeStyle = 'rgba(169,162,204,.16)'; ctx.fillStyle = '#C9C3E6'; ctx.lineWidth = 1;
    ctx.font = fs + 'px Calibri, system-ui, sans-serif';
    ctx.textAlign = 'center'; ctx.textBaseline = 'top';
    o.xTicks.forEach(function (x) {
      if (o.xGrid !== false) { ctx.beginPath(); ctx.moveTo(o.sx(x), pad.t); ctx.lineTo(o.sx(x), o.h - pad.b); ctx.stroke(); }
      ctx.fillText(fx(x), o.sx(x), o.h - pad.b + 6);
    });
    ctx.textAlign = 'right'; ctx.textBaseline = 'middle';
    o.yTicks.forEach(function (y) {
      ctx.beginPath(); ctx.moveTo(pad.l, o.sy(y)); ctx.lineTo(o.w - pad.r, o.sy(y)); ctx.stroke();
      ctx.fillText(fy(y), pad.l - 8, o.sy(y));
    });
    // Названия осей — ярче и жирнее делений, чтобы их было видно с задней парты
    ctx.fillStyle = '#EEEAFB'; ctx.font = 'bold ' + fs + 'px Calibri, system-ui, sans-serif';
    ctx.textAlign = 'center'; ctx.textBaseline = 'bottom';
    ctx.fillText(o.xLabel, (pad.l + o.w - pad.r) / 2, o.h - 2);
    ctx.translate(fs * 0.75, (pad.t + o.h - pad.b) / 2); ctx.rotate(-Math.PI / 2);
    ctx.textBaseline = 'middle'; ctx.fillText(o.yLabel, 0, 0);
    ctx.restore();
  }
  // Отступы графика под крупный шрифт: слева место для делений (yChars — сколько символов в самом длинном)
  function plotPad(w, yChars) {
    var fs = fontPx(w);
    return { l: Math.round(fs * (1.6 + 0.6 * (yChars || 2))) + 8, r: 14, t: 14, b: Math.round(fs * 2.6) + 8 };
  }

  // ---------- Переключатели (режимы, виды) ----------
  // Выбранный пункт отмечается aria-pressed: так его видно и глазами, и программе экранного доступа
  function setPressed(container, isOn) {
    container.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', isOn(b) ? 'true' : 'false'); });
  }

  // ---------- Игра (общая для всех страниц) ----------
  // Игра — это N раундов. Экзамен «подбери и сдай один раз» — игра из одного раунда.
  // В каждом раунде страница задаёт вопрос (round), ученик отвечает, страница вызывает q.answer(очки, html).
  // Компонент сам ведёт счёт, заголовок «Раунд i из n», кнопку «Дальше» / «Итог» / «Сыграть ещё» и итог.
  //
  // o.box     — блок игры в панели; внутри ищутся (или создаются) #gameStep, #gameResult (role=status), #nextBtn
  // o.rounds  — число раундов (или функция, которая его возвращает)
  // o.text    — { step(q) → заголовок раунда, next, finish (текст кнопки перед итогом), finishTitle, again, final(q) → html итога }
  //             Без final итог не показывается отдельно: после ответа на последний раунд сразу «Сыграть ещё» (для экзаменов).
  // o.start(q) — сброс перед новой игрой (по желанию)
  // o.round(q) — подготовить раунд q.i (0, 1, …): показать вопрос, кнопки ответа
  // o.onEnd(q) — после показа итога (по желанию)
  function quiz(o) {
    var box = o.box;
    function part(id, tag, first) {
      var e = document.getElementById(id);
      if (!e) {
        e = document.createElement(tag); e.id = id;
        if (first) box.insertBefore(e, box.firstChild); else box.appendChild(e);
      }
      return e;
    }
    var step = part('gameStep', 'h3', true), result = part('gameResult', 'p'), next = part('nextBtn', 'button');
    result.setAttribute('role', 'status');
    next.type = 'button'; next.classList.add('primary');
    var q = { i: 0, n: 0, score: 0, over: false, answered: false, data: {} };

    function total() { return typeof o.rounds === 'function' ? o.rounds(q) : o.rounds; }
    function showStep() { step.textContent = o.text.step(q); }
    function begin() {
      q.answered = false;
      result.innerHTML = '';
      next.hidden = true;
      showStep();
      o.round(q);
    }
    q.start = function () {
      q.i = 0; q.score = 0; q.over = false; q.data = {};
      q.n = total();
      if (o.start) o.start(q);
      begin();
    };
    // Ответ на раунд: очки и текст результата. Повторный ответ в том же раунде не считается.
    q.answer = function (points, html) {
      if (q.answered || q.over) return;
      q.answered = true;
      q.score += points || 0;
      result.innerHTML = html || '';
      showStep();
      next.hidden = false;
      // Без отдельного итога (игра-экзамен из одного раунда) — сразу «Сыграть ещё»
      if (q.i === q.n - 1 && !o.text.final) {
        q.over = true;
        markDone(pageId());   // доиграл до конца — урок пройден
        if (o.text.finishTitle) step.textContent = o.text.finishTitle;
        next.textContent = o.text.again;
        if (o.onEnd) o.onEnd(q);
        return;
      }
      next.textContent = q.i === q.n - 1 ? o.text.finish : o.text.next;
    };
    // Кнопки-варианты ответа: верные отмечаются ✓, выбранный неверный — ✕ (классы right / wrong из style.css)
    q.choices = function (container, labels, isRight, onPick) {
      container.innerHTML = '';
      labels.forEach(function (label, k) {
        var b = document.createElement('button');
        b.type = 'button'; b.innerHTML = label;
        b.addEventListener('click', function () {
          if (q.answered || q.over) return;
          var ok = isRight(k);
          container.querySelectorAll('button').forEach(function (x, j) {
            x.disabled = true;
            if (isRight(j)) x.classList.add('right');
          });
          if (!ok) b.classList.add('wrong');
          onPick(k, ok);
        });
        container.appendChild(b);
      });
    };
    next.addEventListener('click', function () {
      if (q.over) { q.start(); return; }
      if (q.i < q.n - 1) { q.i++; begin(); return; }
      q.over = true;
      markDone(pageId());   // доиграл до конца — урок пройден
      step.textContent = o.text.finishTitle;
      result.innerHTML = o.text.final(q);
      next.textContent = o.text.again;
      if (o.onEnd) o.onEnd(q);
    });
    return q;
  }

  window.MLViz = {
    lang: lang, t: t, applyI18n: applyI18n, renderHeader: renderHeader, lessonLabel: lessonLabel, doneList: doneList, resetDone: resetDone, renderBook: renderBook,
    fitCanvas: fitCanvas, scale: scale, pointer: pointer, rng: rng, shuffle: shuffle, cssVar: cssVar,
    fontPx: fontPx, range: range, drawAxes: drawAxes, plotPad: plotPad, setPressed: setPressed, quiz: quiz
  };
})();
