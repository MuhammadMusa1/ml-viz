/* Лаборатория ML — сеть MNIST из урока 14 и подготовка рисунка «как в MNIST» (уроки 14 и 16).
   Нужен data/mnist.js (веса сети). Обычный <script src>, без модулей — работает с file://. */
(function () {
  'use strict';

  function bytes(b64) { var s = atob(b64), a = new Uint8Array(s.length); for (var i = 0; i < s.length; i++) a[i] = s.charCodeAt(i); return a; }
  var W1 = null, W2 = null;
  function weights() {
    if (!W1) { W1 = new Int8Array(bytes(MNIST.w1).buffer); W2 = new Int8Array(bytes(MNIST.w2).buffer); }
  }

  // Сеть 784 → 128 (ReLU) → 10 (softmax). Веса int8 × множитель слоя — как в tools/check_mnist.py.
  // h — 128 нейронов скрытого слоя: в уроке 16 это «готовый эксперт по штрихам» (transfer learning).
  function forward(px) {                 // px — 784 числа 0..255
    weights();
    var h = new Float64Array(128), z = new Float64Array(10), i, j, k;
    for (j = 0; j < 128; j++) h[j] = MNIST.b1[j];
    for (i = 0; i < 784; i++) {
      if (!px[i]) continue;              // пустые клетки ничего не добавляют
      var x = px[i] / 255 * MNIST.s1, row = i * 128;
      for (j = 0; j < 128; j++) h[j] += x * W1[row + j];
    }
    for (j = 0; j < 128; j++) if (h[j] < 0) h[j] = 0;   // ReLU
    for (k = 0; k < 10; k++) {
      var s = MNIST.b2[k];
      for (j = 0; j < 128; j++) s += h[j] * W2[j * 10 + k] * MNIST.s2;
      z[k] = s;
    }
    var m = Math.max.apply(null, z), sum = 0, p = [];
    for (k = 0; k < 10; k++) { p.push(Math.exp(z[k] - m)); sum += p[k]; }
    p = p.map(function (v) { return v / sum; });
    var best = 0; for (k = 1; k < 10; k++) if (p[k] > p[best]) best = k;
    return { p: p, pred: best, h: h };
  }

  // Как в MNIST: рисунок вписывают в 20 × 20 и ставят центром масс в центр поля 28 × 28.
  // Без этого маленький рисунок в углу для сети — совсем другой узор.
  function toMnist(raw) {
    var x0 = 28, x1 = -1, y0 = 28, y1 = -1, r, c;
    for (r = 0; r < 28; r++) for (c = 0; c < 28; c++) if (raw[r * 28 + c] > 0) {
      if (c < x0) x0 = c; if (c > x1) x1 = c; if (r < y0) y0 = r; if (r > y1) y1 = r;
    }
    var out = new Uint8Array(784);
    if (x1 < 0) return out;
    var w = x1 - x0 + 1, h = y1 - y0 + 1, k = 20 / Math.max(w, h);
    var nw = Math.max(1, Math.round(w * k)), nh = Math.max(1, Math.round(h * k));
    var small = new Float64Array(nw * nh);
    for (r = 0; r < nh; r++) for (c = 0; c < nw; c++) {
      var sy = y0 + (r + 0.5) / k - 0.5, sx = x0 + (c + 0.5) / k - 0.5;
      var ry = Math.max(y0, Math.min(y1, Math.round(sy))), rx = Math.max(x0, Math.min(x1, Math.round(sx)));
      small[r * nw + c] = raw[ry * 28 + rx];
    }
    var mx = 0, my = 0, tot = 0;
    for (r = 0; r < nh; r++) for (c = 0; c < nw; c++) { var v = small[r * nw + c]; mx += v * c; my += v * r; tot += v; }
    var ox = Math.round(14 - (tot ? mx / tot : nw / 2) - 0.5), oy = Math.round(14 - (tot ? my / tot : nh / 2) - 0.5);
    for (r = 0; r < nh; r++) for (c = 0; c < nw; c++) {
      var R = r + oy, C = c + ox;
      if (R >= 0 && R < 28 && C >= 0 && C < 28) out[R * 28 + C] = small[r * nw + c];
    }
    return out;
  }

  // Кисть: мягкое пятно радиусом ~1.5 клетки, как штрих пером; между точками — отрезок без пропусков
  function brush(raw, cx, cy) {
    for (var r = Math.floor(cy - 2); r <= Math.ceil(cy + 2); r++) for (var c = Math.floor(cx - 2); c <= Math.ceil(cx + 2); c++) {
      if (r < 0 || r > 27 || c < 0 || c > 27) continue;
      var d = Math.hypot(c + 0.5 - cx, r + 0.5 - cy), v = Math.round(255 * Math.max(0, Math.min(1, 1.9 - d)));
      if (v > raw[r * 28 + c]) raw[r * 28 + c] = v;
    }
  }
  function line(raw, a, b) {
    var steps = Math.ceil(Math.hypot(b[0] - a[0], b[1] - a[1]) * 3);
    for (var s = 0; s <= steps; s++) brush(raw, a[0] + (b[0] - a[0]) * s / (steps || 1), a[1] + (b[1] - a[1]) * s / (steps || 1));
  }

  // Клетка 0..255 → цвет от фона курса к светлому штриху
  function gray(v) {
    return 'rgb(' + Math.round(23 + 215 * v / 255) + ',' + Math.round(19 + 215 * v / 255) + ',' + Math.round(46 + 205 * v / 255) + ')';
  }

  window.MLDigits = { bytes: bytes, forward: forward, toMnist: toMnist, brush: brush, line: line, gray: gray };
})();
