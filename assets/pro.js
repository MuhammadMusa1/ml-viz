/* Лаборатория ML — общие функции раздела «Для профи» (страницы viz/pro-*).
   Подключается после core.js и catalog.js. Без модулей и сборки: работает с file://.
   Здесь только то, что нужно больше чем одной странице раздела: бумажные этикетки на canvas,
   векторная математика (косинус, softmax), разбор строк и мелкие помощники для разметки. */
(function () {
  'use strict';

  // Шапка, тексты из STR и функция T(key, vars) — одинаковое начало у всех страниц раздела
  function init(STR) {
    MLViz.renderHeader('../../');
    MLViz.applyI18n(STR);
    return function (k, v) { return MLViz.t(STR, k, v); };
  }
  function el(id) { return document.getElementById(id); }
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }

  // ---------- Canvas ----------
  function font(px, bold) { return (bold ? 'bold ' : '') + px + 'px ' + (MLViz.cssVar('--font') || 'Calibri, system-ui, sans-serif'); }
  // Размер подписи на графике: не мельче 13 px (правило курса), на проекторе растёт вместе с графиком
  function fs(g) { return MLViz.fontPx(g.w); }
  function rr(ctx, x, y, w, h, r) {   // скруглённый прямоугольник без ctx.roundRect (его нет в старых браузерах)
    ctx.beginPath();
    ctx.moveTo(x + r, y); ctx.lineTo(x + w - r, y); ctx.quadraticCurveTo(x + w, y, x + w, y + r);
    ctx.lineTo(x + w, y + h - r); ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    ctx.lineTo(x + r, y + h); ctx.quadraticCurveTo(x, y + h, x, y + h - r);
    ctx.lineTo(x, y + r); ctx.quadraticCurveTo(x, y, x + r, y);
    ctx.closePath();
  }
  // Этикетка на графике: тёмный текст на бумаге (--paper / --ink), как подсказки и бирки курса.
  // o: { size, bold, align: 'left'|'center'|'right', base: 'middle'|'top'|'bottom', dashed, maxW } → {x, y, w, h}
  function label(ctx, text, x, y, o) {
    o = o || {};
    var size = Math.max(13, o.size || 13), padX = Math.round(size * 0.4), h = Math.round(size * 1.5);
    ctx.save();
    ctx.font = font(size, o.bold);
    var tw = ctx.measureText(text).width;
    if (o.maxW && tw > o.maxW - 2 * padX) {   // длинная фраза — обрезаем с многоточием, полный текст есть в панели
      while (text.length > 1 && ctx.measureText(text + '…').width > o.maxW - 2 * padX) text = text.slice(0, -1);
      text += '…'; tw = ctx.measureText(text).width;
    }
    var w = tw + 2 * padX;
    var bx = o.align === 'center' ? x - w / 2 : o.align === 'right' ? x - w : x;
    var by = o.base === 'top' ? y : o.base === 'bottom' ? y - h : y - h / 2;
    rr(ctx, bx, by, w, h, 4);
    ctx.fillStyle = MLViz.cssVar('--paper');
    ctx.fill();
    if (o.dashed) { ctx.setLineDash([4, 3]); ctx.strokeStyle = MLViz.cssVar('--ink'); ctx.lineWidth = 1.5; ctx.stroke(); ctx.setLineDash([]); }
    ctx.fillStyle = MLViz.cssVar('--ink');
    ctx.textAlign = 'left'; ctx.textBaseline = 'middle';
    ctx.fillText(text, bx + padX, by + h / 2 + 1);
    ctx.restore();
    return { x: bx, y: by, w: w, h: h };
  }
  function overlaps(a, list) {
    for (var i = 0; i < list.length; i++) {
      var b = list[i];
      if (a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y) return true;
    }
    return false;
  }
  // Ширина этикетки заранее — чтобы подобрать место без наложений
  function labelSize(ctx, text, size, bold) {
    size = Math.max(13, size || 13);
    ctx.save(); ctx.font = font(size, bold);
    var w = ctx.measureText(text).width + 2 * Math.round(size * 0.4);
    ctx.restore();
    return { w: w, h: Math.round(size * 1.5) };
  }

  // ---------- Векторы ----------
  function dot(a, b) { var s = 0; for (var i = 0; i < a.length; i++) s += a[i] * b[i]; return s; }
  function norm(a) { return Math.sqrt(dot(a, a)); }
  function cosine(a, b) { var n = norm(a) * norm(b); return n ? dot(a, b) / n : 0; }
  function euclid(a, b) { var s = 0; for (var i = 0; i < a.length; i++) s += (a[i] - b[i]) * (a[i] - b[i]); return Math.sqrt(s); }
  // softmax(z / T): логиты → вероятности. Вычитаем максимум, чтобы exp не переполнялся при маленьком T
  function softmax(z, T) {
    T = T == null ? 1 : T;
    var m = Math.max.apply(null, z), e = z.map(function (v) { return Math.exp((v - m) / T); });
    var s = e.reduce(function (a, b) { return a + b; }, 0);
    return e.map(function (v) { return v / s; });
  }

  // ---------- Числа ----------
  function pct(x, d) { return (x * 100).toFixed(d || 0) + '%'; }
  function fix(x, d) { return (+x).toFixed(d == null ? 2 : d); }

  // Перерисовка по resize с задержкой (как на всех страницах курса)
  function onResize(fn) { var rt; window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(fn, 120); }); }

  window.MLPro = {
    init: init, el: el, esc: esc, font: font, fs: fs, rr: rr, label: label, labelSize: labelSize, overlaps: overlaps,
    dot: dot, norm: norm, cosine: cosine, euclid: euclid, softmax: softmax, pct: pct, fix: fix, onResize: onResize
  };
})();
