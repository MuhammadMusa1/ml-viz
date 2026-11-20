/* Лаборатория ML — общие функции для всех страниц.
   Подключается обычным <script src>, без модулей и сборки: так страницы открываются и с file:// (флешка в классе). */
(function () {
  'use strict';

  // ---------- Язык ----------
  // Сейчас только 'ru'. Таджикский ('tg') добавляется словарями в тех же объектах STR — разметку трогать не нужно.
  var LANGS = ['ru'];          // когда появится перевод: ['ru', 'tg']
  var LANG_NAMES = { ru: 'Рус', tg: 'Тоҷ' };

  function readLang() {
    var fromUrl = new URLSearchParams(location.search).get('lang');
    if (fromUrl && LANGS.indexOf(fromUrl) !== -1) return fromUrl;
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
  }

  function setLang(l) {
    try { localStorage.setItem('mlviz.lang', l); } catch (e) {}
    var u = new URL(location.href); u.searchParams.set('lang', l); location.href = u.toString();
  }

  // ---------- Шапка ----------
  var UI = {
    ru: { all: 'Все уроки', brand: 'Лаборатория <b>ML</b>', lesson: 'Урок {n}', prev: 'Предыдущий урок: {t}', next: 'Следующий урок: {t}' },
    tg: { all: 'Ҳамаи дарсҳо', brand: 'Лабораторияи <b>ML</b>', lesson: 'Дарси {n}', prev: 'Дарси пешина: {t}', next: 'Дарси оянда: {t}' }
  };

  // Соседние готовые уроки по каталогу (если catalog.js подключён) — учителю удобно листать на проекторе
  function lessonNav(root) {
    // Ищем именно папку /viz/<id>/: на GitHub Pages сайт лежит в /ml-viz/, и «viz/» встречается раньше
    var m = location.pathname.match(/\/viz\/([^\/]+)\//);
    if (!m || !window.CATALOG) return '';
    var ready = [];
    window.CATALOG.forEach(function (ph) { ph.items.forEach(function (it) { if (it.status === 'ready') ready.push(it); }); });
    var i = ready.map(function (it) { return it.id; }).indexOf(m[1]);
    if (i === -1) return '';
    function link(it, cls, label, tipKey) {
      var title = (it.title && (it.title[lang] || it.title.ru)) || it.id;
      return '<a class="lesson-step ' + cls + '" href="' + root + 'viz/' + it.id + '/index.html" title="' +
        t(UI, tipKey, { t: title }) + '" aria-label="' + t(UI, tipKey, { t: title }) + '">' + label + '</a>';
    }
    return (i > 0 ? link(ready[i - 1], 'prev', '‹ ' + t(UI, 'lesson', { n: ready[i - 1].lesson }), 'prev') : '') +
           (i < ready.length - 1 ? link(ready[i + 1], 'next', t(UI, 'lesson', { n: ready[i + 1].lesson }) + ' ›', 'next') : '');
  }

  // Логотип: три точки цветов пингвинов — маленькая «диаграмма рассеяния»
  var LOGO =
    '<svg class="logo" viewBox="0 0 32 32" aria-hidden="true">' +
      '<rect x="1" y="1" width="30" height="30" rx="9" fill="#261F4A" stroke="#3A3168"/>' +
      '<path d="M9 22 L16 12 L23 18" fill="none" stroke="#A9A2CC" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" opacity=".7"/>' +
      '<circle cx="9" cy="22" r="3.6" fill="#A78BFA"/>' +
      '<circle cx="16" cy="12" r="3.6" fill="#22D3EE"/>' +
      '<circle cx="23" cy="18" r="3.6" fill="#FBBF24"/>' +
    '</svg>';

  // root — относительный путь до корня сайта ('' для главной, '../../' для viz/xxx/)
  function renderHeader(root) {
    var h = document.getElementById('site-header');
    if (!h) return;
    var langBtns = LANGS.length > 1
      ? '<div class="lang-switch">' + LANGS.map(function (l) {
          return '<button type="button" data-lang="' + l + '" aria-pressed="' + (l === lang) + '">' + LANG_NAMES[l] + '</button>';
        }).join('') + '</div>'
      : '';
    h.className = 'site-header';
    h.innerHTML =
      '<div class="wrap">' +
        '<a class="brand" href="' + root + 'index.html">' + LOGO + '<span>' + t(UI, 'brand') + '</span></a>' +
        '<nav>' + (root ? '<a href="' + root + 'index.html">' + t(UI, 'all') + '</a>' + lessonNav(root) : '') + '</nav>' +
        langBtns +
      '</div>';
    h.querySelectorAll('[data-lang]').forEach(function (b) {
      b.addEventListener('click', function () { setLang(b.dataset.lang); });
    });
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
      step.textContent = o.text.finishTitle;
      result.innerHTML = o.text.final(q);
      next.textContent = o.text.again;
      if (o.onEnd) o.onEnd(q);
    });
    return q;
  }

  window.MLViz = {
    lang: lang, t: t, applyI18n: applyI18n, renderHeader: renderHeader,
    fitCanvas: fitCanvas, scale: scale, pointer: pointer, rng: rng, shuffle: shuffle, cssVar: cssVar,
    fontPx: fontPx, range: range, drawAxes: drawAxes, plotPad: plotPad, setPressed: setPressed, quiz: quiz
  };
})();
