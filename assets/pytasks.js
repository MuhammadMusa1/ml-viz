/* Задания с кодом Python: «Что выведет?», «В какой строке ошибка?», «Собери программу».
   Общий движок для Python-разминок (warmup/) и раздела «Python с нуля» (viz/py-*).
   Сами задания и ответы считает настоящий Python (tools/build_warmup.py, tools/build_pystart.py),
   страница даёт только список заданий и тексты x_<id> (объяснение), g_<id> (условие «собери»), topic_<тема>.

   Разметка на странице (внутри одного блока с классом pytask):
     <div class="pytask" id="game">
       <div class="task-head"><h3 id="gameStep"></h3><h2 id="ask"></h2></div>
       <p class="task-hint" id="hint"></p>
       <div class="task-grid" id="taskGrid"><pre class="code" id="code"></pre>
         <div><p class="sub" id="answerLabel"></p><div id="answer"></div></div></div>
       <div id="gameResult"></div><button type="button" id="nextBtn" hidden></button>
     </div>
*/
(function () {
  'use strict';
  // Подписи движка (одни на всех страницах с заданиями)
  var UI = {
    ru: {
      codeAria: 'Код программы с номерами строк',
      step: 'Задание {i} из {n}', next: 'Дальше', finish: 'Итог', finishTitle: 'Итог', again: 'Сыграть ещё ↺',
      askOut: 'Что выведет программа?', askBug: 'В какой строке ошибка?', askParsons: 'Собери программу',
      hintOut: 'Сначала подумай, потом нажимай.', keysHint: 'Можно клавишами 1–{n}.',
      hintBug: 'Python остановится на одной из строк. Нажми на неё прямо в коде — или «Ошибки нет».',
      hintParsons: '{g} Нажимай строки по порядку.',
      answerLabel: 'Выбери ответ', bugLabel: 'Или', errChoice: 'Ошибка — программа не запустится',
      lineN: 'Строка {n}', noBug: 'Ошибки нет', bugIs: 'Ошибка в строке {n}. Python напишет <code>{err}</code>.',
      poolLabel: 'Строки (нажми, чтобы добавить)', slot: '— нажми строку —', undo: '← Убрать последнюю', check: 'Проверить',
      rightOrder: 'Правильная программа:', right: 'Верно', wrong: 'Не так',
      finalScore: '<b>{s}</b> из {n}',
      repeatTitle: 'Повтори', repeatItem: 'Задание {i}', okTopics: 'Верно: {t}.', retry: 'Пройти ошибки ещё раз',
      // Пошаговый показ («Python с нуля»)
      stepStart: 'Python ещё ничего не выполнил. Стрелка ▶ — строка, которую он выполнит следующей.',
      stepNext: 'Шаг {k} из {n}. Следующей Python выполнит строку {line}.',
      stepRet: 'Шаг {k} из {n}. Функция <code>{fn}</code> закончила работу и возвращает <b>{ret}</b>.',
      stepEnd: 'Программа закончилась. Шагов: {n}.',
      varsTitle: 'Переменные', varsEmpty: 'Пока ни одной переменной.', localTitle: 'Внутри функции {fn}()',
      outTitle: 'Вывод (что напечатал print)', outEmpty: 'Пока ничего не напечатано.',
      changed: 'изменилась',
      panelNote: 'Перед каждым «Шагом» угадай: какая коробка изменится и что напечатается?',
      demoTitle: 'Пример', back: '← Назад', stepBtn: 'Шаг →', reset: 'Сначала', end: 'До конца',
      gameTitle: 'Игра: прочитай код раньше Python',
      gameRules: '8 заданий: «что выведет?», «где ошибка?», «собери программу». За верный ответ — 1 очко, попытка одна. После ответа — объяснение, в конце — итог и темы, которые стоит повторить.',
      pyFinish: 'Итог игры',
      pyAll: 'Все 8 — отлично! Эта тема у тебя в кармане.',
      pySome: 'Неплохо. Пройди ошибки ещё раз или вернись к примерам выше и пошагай их.',
      pyFew: 'Ничего страшного: вернись к примерам выше, пошагай каждый и угадывай следующую строку, прежде чем нажать «Шаг».',
      type_int: 'целое число', type_float: 'дробное число', type_str: 'текст (строка)', type_list: 'список', type_bool: 'да / нет',
      type_NoneType: 'пусто (None)', type_dict: 'словарь', type_function: 'функция', type_DataFrame: 'таблица: строк × столбцов',
      type_Series: 'столбец: сколько значений', type_tuple: 'кортеж'
    }
  };
  function U(k, v) { return MLViz.t(UI, k, v); }
  function el(id) { return document.getElementById(id); }
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

  // Подсветка Python: ключевые слова, строки, числа, встроенные функции, комментарии.
  // Цвета пастельные и только внутри кода — интерфейс и данные ими не красим
  var HL = /(f?"[^"]*"|'[^']*')|(#.*$)|\b(def|return|if|elif|else|for|in|while|not|is|and|or|None|True|False|import|from|as|try|except)\b|\b(print|len|abs|sorted|sum|range|min|max|round|float|int|str|list|zip|type)\b(?=\()|\b(\d+(?:\.\d+)?)\b/g;
  function hl(line) {
    var out = '', last = 0, m;
    HL.lastIndex = 0;
    while ((m = HL.exec(line))) {
      out += esc(line.slice(last, m.index));
      var cls = m[1] ? 's' : m[2] ? 'c' : m[3] ? 'k' : m[4] ? 'f' : 'n';
      out += '<span class="tok-' + cls + '">' + esc(m[0]) + '</span>';
      last = m.index + m[0].length;
    }
    return out + esc(line.slice(last));
  }
  function lineHtml(text, i) { return '<span class="no">' + (i + 1) + '</span><span>' + hl(text) + '</span>'; }
  // Код с номерами строк: в заданиях «найди ошибку» номер строки — это ответ
  function codeHtml(code) {
    return code.split('\n').map(function (l, i) { return '<span class="ln">' + lineHtml(l, i) + '</span>'; }).join('');
  }
  function verdict(ok, body) {
    return '<div class="verdict ' + (ok ? 'ok' : 'no') + '"><span class="mark" aria-hidden="true">' + (ok ? '✓' : '✕') + '</span>' +
      '<div><b class="v">' + U(ok ? 'right' : 'wrong') + '</b>' + body + '</div></div>';
  }

  // o.T(k, v)        — тексты страницы (x_<id>, g_<id>, topic_<тема>)
  // o.list()         — все задания текущего набора (урока или страницы)
  // o.rand           — генератор случайных чисел (MLViz.rng)
  // o.finalMsg(q)    — фраза под счётом в итоге
  // o.finalLinks(q)  — html кнопок в итоге (например, «К уроку 5»), по желанию
  // o.finishTitle    — заголовок итога, по желанию
  function game(o) {
    var T = o.T, rand = o.rand, retryIdx = null, pendingRetry = false;
    el('code').setAttribute('aria-label', U('codeAria'));
    function tasks() {
      var all = o.list();
      return retryIdx ? retryIdx.map(function (i) { return all[i]; }) : all;
    }
    function topicsOf(list) {
      var seen = [];
      list.forEach(function (t) { if (seen.indexOf(t.topic) === -1) seen.push(t.topic); });
      return seen.map(function (k) { return T('topic_' + k); }).join(', ');
    }
    function layout() { el('taskGrid').classList.remove('wide'); el('code').hidden = false; }

    // «Что выведет?»: код слева, варианты справа (клавиши 1–4 добавляет MLViz.quiz)
    function roundOut(q, t) {
      layout();
      el('ask').textContent = U('askOut');
      // Про клавиши говорим только там, где есть клавиатура
      el('hint').textContent = U('hintOut') + (window.matchMedia('(pointer: coarse)').matches ? '' : ' ' + U('keysHint', { n: t.choices.length }));
      el('answerLabel').textContent = U('answerLabel');
      el('code').innerHTML = codeHtml(t.code);
      var opts = MLViz.shuffle(t.choices.map(function (c, k) { return { v: c, ok: k === 0 }; }), rand);
      var box = el('answer');
      box.className = 'choices mono';
      q.choices(box, opts.map(function (x) {
        return x.v === '!err' ? esc(U('errChoice')) : esc(x.v).replace(/\n/g, '<br>');
      }), function (k) { return opts[k].ok; }, function (k, ok) {
        q.data.res[q.i] = ok;
        q.answer(ok ? 1 : 0, verdict(ok, T('x_' + t.id)));
      });
    }
    // «В какой строке ошибка?»: строки кода — сами кнопки
    function roundBug(q, t) {
      layout();
      el('ask').textContent = U('askBug');
      el('hint').textContent = U('hintBug');
      el('answerLabel').textContent = U('bugLabel');
      var code = el('code'), lines = t.code.split('\n'), done = false, noBtn;
      code.innerHTML = '';
      function finish(pickedLine) {
        if (done) return;
        done = true;
        var ok = pickedLine === t.line;
        code.querySelectorAll('button.ln').forEach(function (b) {
          b.disabled = true;
          if (+b.dataset.n === t.line) b.classList.add('is-right');
          else if (+b.dataset.n === pickedLine) b.classList.add('is-wrong');
        });
        noBtn.disabled = true;
        if (pickedLine === 0) noBtn.classList.add('wrong');
        q.data.res[q.i] = ok;
        q.answer(ok ? 1 : 0, verdict(ok, U('bugIs', { n: t.line, err: t.err }) + ' ' + T('x_' + t.id)));
      }
      lines.forEach(function (l, i) {
        if (!l.trim()) { code.insertAdjacentHTML('beforeend', '<span class="ln">' + lineHtml('', i) + '</span>'); return; }
        var b = document.createElement('button');
        b.type = 'button'; b.className = 'ln'; b.dataset.n = i + 1;
        b.setAttribute('aria-label', U('lineN', { n: i + 1 }) + ': ' + l.trim());
        b.innerHTML = lineHtml(l, i);
        b.addEventListener('click', function () { finish(i + 1); });
        code.appendChild(b);
      });
      var box = el('answer');
      box.className = '';
      box.innerHTML = '';
      noBtn = document.createElement('button');
      noBtn.type = 'button'; noBtn.textContent = U('noBug');
      noBtn.addEventListener('click', function () { finish(0); });
      box.appendChild(noBtn);
    }
    // «Собери программу»: слева — нумерованные строки программы, справа — строки, которые нажимают по порядку
    function roundParsons(q, t) {
      layout();
      el('ask').textContent = U('askParsons');
      el('hint').innerHTML = U('hintParsons', { g: T('g_' + t.id) });
      el('answerLabel').textContent = U('poolLabel');
      var n = t.lines.length, built = [], pool, done = false;
      function isValid(order) { return t.orders.some(function (x) { return x.join() === order.join(); }); }
      // Перемешиваем так, чтобы строки не стояли сразу в верном порядке
      do { pool = MLViz.shuffle(MLViz.range(0, n - 1, 1), rand); } while (isValid(pool));
      var box = el('answer');
      box.className = 'parsons';
      box.innerHTML = '<div class="lines" id="pool"></div>' +
        '<div class="row"><button type="button" id="undoBtn">' + U('undo') + '</button>' +
        '<button type="button" class="primary" id="checkBtn" disabled>' + U('check') + '</button></div>';
      function draw() {
        var code = el('code'), pEl = el('pool');
        code.innerHTML = ''; pEl.innerHTML = '';
        for (var i = 0; i < n; i++) {
          if (i < built.length) {
            var b = document.createElement('button');
            b.type = 'button'; b.className = 'ln'; b.disabled = done;
            b.innerHTML = lineHtml(t.lines[built[i]], i);
            b.addEventListener('click', (function (pos) { return function () { built.splice(pos, 1); draw(); }; })(i));
            code.appendChild(b);
          } else {
            code.insertAdjacentHTML('beforeend', '<span class="ln slot"><span class="no">' + (i + 1) + '</span><span>' + U('slot') + '</span></span>');
          }
        }
        pool.forEach(function (k) {
          if (built.indexOf(k) !== -1) return;
          var b = document.createElement('button');
          b.type = 'button'; b.textContent = t.lines[k]; b.disabled = done;
          b.addEventListener('click', function () { built.push(k); draw(); });
          pEl.appendChild(b);
        });
        el('checkBtn').disabled = done || built.length < n;
        el('undoBtn').disabled = done || !built.length;
      }
      el('undoBtn').addEventListener('click', function () { built.pop(); draw(); });
      el('checkBtn').addEventListener('click', function () {
        if (built.length < n) return;
        var ok = isValid(built);
        done = true; draw();
        q.data.res[q.i] = ok;
        q.answer(ok ? 1 : 0, verdict(ok, (ok ? '' : U('rightOrder') + '<pre class="code">' + codeHtml(t.lines.join('\n')) + '</pre>') + T('x_' + t.id)));
      });
      draw();
    }

    // Итог: счёт, «Повтори» с заданиями, где ошибся, и «Пройти ошибки ещё раз»
    function finalHtml(q) {
      var list = tasks(), all = o.list(), missed = [], good = [];
      var items = list.map(function (t, i) {
        if (q.data.res[i]) { good.push(t); return ''; }
        missed.push(i);
        return '<li><span class="n">' + MLViz.pad2(missed.length) + '</span><div><b>' + T('topic_' + t.topic) + '</b>' +
          '<small>' + U('repeatItem', { i: i + 1 }) + ' · ' + U(t.type === 'out' ? 'askOut' : t.type === 'bug' ? 'askBug' : 'askParsons') + '</small></div></li>';
      }).join('');
      q.data.missed = missed.map(function (i) { return all.indexOf(list[i]); });
      // «Верно» — только темы, где не было ни одной ошибки (иначе тема окажется и в «Повтори», и в «Верно»)
      var missedTopics = missed.map(function (i) { return list[i].topic; });
      var goodOnly = good.filter(function (t) { return missedTopics.indexOf(t.topic) === -1; });
      return '<div class="final"><div>' +
          '<div class="score">' + U('finalScore', { s: q.score, n: q.n }) + '</div><p>' + o.finalMsg(q) + '</p>' +
          '<div class="row">' + (missed.length ? '<button type="button" class="btn" id="retryBtn">' + U('retry') + '</button>' : '') +
          (o.finalLinks ? o.finalLinks(q) : '') + '</div>' +
        '</div><div>' +
          (missed.length ? '<p class="sub">' + U('repeatTitle') + '</p><ul class="repeat-list">' + items + '</ul>' : '') +
          (goodOnly.length ? '<p class="note">' + U('okTopics', { t: topicsOf(goodOnly) }) + '</p>' : '') +
        '</div></div>';
    }

    var g = MLViz.quiz({
      box: el('game'),
      rounds: function () { return tasks().length; },
      text: {
        step: function (q) { return U('step', { i: q.i + 1, n: q.n }); },
        next: U('next'), finish: U('finish'), again: U('again'), finishTitle: o.finishTitle || U('finishTitle'),
        final: finalHtml
      },
      start: function (q) {
        if (!pendingRetry) retryIdx = null;
        pendingRetry = false;
        q.data.res = [];
      },
      round: function (q) {
        var t = tasks()[q.i];
        if (t.type === 'out') roundOut(q, t);
        else if (t.type === 'bug') roundBug(q, t);
        else roundParsons(q, t);
      },
      onEnd: function (q) {
        el('ask').textContent = ''; el('hint').textContent = '';
        el('taskGrid').hidden = true;
        var rb = el('retryBtn');
        if (rb) rb.addEventListener('click', function () {
          retryIdx = q.data.missed; pendingRetry = true;
          g.start();
        });
      }
    });
    // Новый раунд или новая игра — сетка задания снова видна
    el('nextBtn').addEventListener('click', function () { el('taskGrid').hidden = false; }, true);
    var start0 = g.start;
    g.start = function () { el('taskGrid').hidden = false; start0(); };
    g.topicsOf = topicsOf;
    return g;
  }

  // ---------- Пошаговый показ программы: как отладчик, но шаги заранее записал настоящий Python ----------
  // Шаг = состояние ПЕРЕД строкой steps[i].line: переменные, напечатанное; последний шаг (line 0) — итог.
  // Шаг с ret — функция закончила работу и возвращает значение.
  function stepper(o) {
    var demo = null, i = 0, T = o.T;
    function varsHtml(list, prev) {
      if (!list.length) return '<p class="note">' + U('varsEmpty') + '</p>';
      return '<ul class="py-vars">' + list.map(function (v) {
        var old = null;
        (prev || []).forEach(function (p) { if (p[0] === v[0]) old = p; });
        var ch = prev && (!old || old[1] !== v[1]);
        return '<li' + (ch ? ' class="changed"' : '') + '><span class="name">' + esc(v[0]) + '</span>' +
          '<span class="val">' + (v[2] === 'function' ? '' : esc(v[1])) + '</span>' +
          '<span class="type">' + U('type_' + v[2]) + (ch ? ' · ' + U('changed') : '') + '</span></li>';
      }).join('') + '</ul>';
    }
    function draw() {
      var st = demo.steps[i], prev = i > 0 ? demo.steps[i - 1] : null, n = demo.steps.length - 1;
      var cur = st.line, was = prev && !prev.ret ? prev.line : 0;
      el('demoCode').innerHTML = demo.code.split('\n').map(function (l, k) {
        var ln = k + 1, cls = ln === cur ? ' cur' : ln === was ? ' was' : '';
        return '<span class="ln' + cls + '"><span class="no">' + (ln === cur ? '▶ ' : '') + ln + '</span><span>' + hl(l) + '</span></span>';
      }).join('');
      el('stepInfo').innerHTML = i === 0 ? U('stepStart')
        : st.line === 0 ? U('stepEnd', { n: n })
        : st.ret != null ? U('stepRet', { k: i, n: n, fn: esc(st.local.fn), ret: esc(st.ret) })
        : U('stepNext', { k: i, n: n, line: st.line });
      // Подсветка «изменилась» — только для одной и той же области (снаружи / внутри функции)
      var pl = prev && prev.local && st.local && prev.local.fn === st.local.fn ? prev.local.vars : null;
      el('vars').innerHTML = varsHtml(st.vars, prev ? prev.vars : null) +
        (st.local ? '<p class="sub py-local">' + U('localTitle', { fn: esc(st.local.fn) }) + '</p>' + varsHtml(st.local.vars, pl) : '');
      var out = el('out');
      out.textContent = st.out ? st.out.replace(/\n$/, '') : U('outEmpty');
      out.classList.toggle('empty', !st.out);
      el('backBtn').disabled = i === 0;
      el('stepBtn').disabled = el('endBtn').disabled = i === n;
      el('resetBtn').disabled = i === 0;
    }
    function pick(k) {
      demo = o.demos[k]; i = 0;
      MLViz.setPressed(el('demoSeg'), function (b) { return +b.dataset.k === k; });
      el('demoCap').innerHTML = T('ex_' + demo.id);
      draw();
    }
    o.demos.forEach(function (d, k) {
      var b = document.createElement('button');
      b.type = 'button'; b.dataset.k = k; b.textContent = T('exb_' + d.id);
      b.addEventListener('click', function () { pick(k); });
      el('demoSeg').appendChild(b);
    });
    el('stepBtn').addEventListener('click', function () { if (i < demo.steps.length - 1) { i++; draw(); } });
    el('backBtn').addEventListener('click', function () { if (i > 0) { i--; draw(); } });
    el('resetBtn').addEventListener('click', function () { i = 0; draw(); });
    el('endBtn').addEventListener('click', function () { i = demo.steps.length - 1; draw(); });
    el('varsTitle').textContent = U('varsTitle');
    el('outTitle').textContent = U('outTitle');
    pick(0);
    return { pick: pick, state: function () { return { demo: demo.id, i: i }; } };
  }

  // Страница раздела «Python с нуля»: пошаговые примеры + игра из 8 заданий. Данные — window.PYSTART[id страницы]
  function pystart(STR) {
    MLViz.renderHeader('../../');
    MLViz.applyI18n(STR);
    var T = function (k, v) { return MLViz.t(STR, k, v); };
    var id = (location.pathname.match(/\/viz\/([^\/]+)\//) || [])[1];
    var data = window.PYSTART[id];
    // Подписи кнопок и игры — общие для всех страниц раздела
    [['demoTitle', 'demoTitle'], ['backBtn', 'back'], ['stepBtn', 'stepBtn'], ['resetBtn', 'reset'], ['endBtn', 'end'],
      ['gameTitle', 'gameTitle'], ['gameRules', 'gameRules'], ['panelNote', 'panelNote']].forEach(function (x) { el(x[0]).textContent = U(x[1]); });
    var st = stepper({ T: T, demos: data.demos });
    var g = game({
      T: T, rand: MLViz.rng(Date.now()), finishTitle: U('pyFinish'),
      list: function () { return data.tasks; },
      finalMsg: function (q) { return U(q.score === q.n ? 'pyAll' : q.score >= q.n / 2 ? 'pySome' : 'pyFew'); }
    });
    g.start();
    window.PY_PAGE = { data: data, stepper: st, game: g };   // для проверки в браузере
  }

  window.MLPyTasks = { esc: esc, hl: hl, lineHtml: lineHtml, codeHtml: codeHtml, game: game, stepper: stepper, pystart: pystart, UI: UI };
})();
