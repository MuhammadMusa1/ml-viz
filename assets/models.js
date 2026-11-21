/* Лаборатория ML — модели, которые считаются так же, как в sklearn (для страниц с кросс-валидацией: уроки 12, 19).
   Подключается обычным <script src>, без модулей — работает и с file://.
   Модели работают с двумя признаками: точка = [a, b], ответ = номер вида 0..2 (по алфавиту, как классы в sklearn). */
(function () {
  'use strict';

  // Самый частый ответ; при ничьей — меньший номер (раньше по алфавиту), как np.argmax в sklearn
  function majority(c) { var b = 0; for (var k = 1; k < c.length; k++) if (c[k] > c[b]) b = k; return b; }
  function counts(ys) { var c = [0, 0, 0]; ys.forEach(function (y) { c[y]++; }); return c; }

  // StratifiedKFold(n) без перемешивания: номер части для каждой строки.
  // Виды нумеруются по первому появлению, доли видов в частях — как в отсортированном списке ответов.
  function folds(ys, n) {
    n = n || 5;
    var order = [], code = ys.map(function (y) {
      if (order.indexOf(y) === -1) order.push(y);
      return order.indexOf(y);
    });
    var sorted = code.slice().sort(function (a, b) { return a - b; });
    var alloc = [];
    for (var i = 0; i < n; i++) {
      var c = order.map(function () { return 0; });
      for (var j = i; j < sorted.length; j += n) c[sorted[j]]++;
      alloc.push(c);
    }
    var fold = new Array(ys.length);
    order.forEach(function (_, k) {
      var seq = [];
      alloc.forEach(function (c, i) { for (var r = 0; r < c[k]; r++) seq.push(i); });
      var m = 0;
      code.forEach(function (c, idx) { if (c === k) fold[idx] = seq[m++]; });
    });
    return fold;
  }

  // KNN в Pipeline со StandardScaler: масштаб учится только на этих точках (std как в sklearn, делим на n).
  // Возвращает predict(a, b, k). Ничьи расстояний — в порядке строк (стабильная сортировка).
  function knn(X, ys) {
    var sc = [0, 1].map(function (f) {
      var m = X.reduce(function (s, x) { return s + x[f]; }, 0) / X.length;
      var v = X.reduce(function (s, x) { return s + (x[f] - m) * (x[f] - m); }, 0) / X.length;
      return { m: m, s: Math.sqrt(v) || 1 };
    });
    var Z = X.map(function (x) { return [(x[0] - sc[0].m) / sc[0].s, (x[1] - sc[1].m) / sc[1].s]; });
    return function (a, b, k) {
      var qa = (a - sc[0].m) / sc[0].s, qb = (b - sc[1].m) / sc[1].s;
      var d = Z.map(function (z, i) { var da = z[0] - qa, db = z[1] - qb; return { i: i, d: da * da + db * db }; });
      d.sort(function (u, w) { return u.d - w.d; });
      var c = [0, 0, 0];
      for (var j = 0; j < k; j++) c[ys[d[j].i]]++;
      return majority(c);
    };
  }

  // Дерево решений (CART, Gini), как DecisionTreeClassifier: признаки во float32, порог — середина между значениями.
  function tree(X, ys, maxDepth) {
    var data = X.map(function (x, i) { return { y: ys[i], v: [Math.fround(x[0]), Math.fround(x[1])] }; });
    function gini(c, n) { return n ? 1 - (c[0] * c[0] + c[1] * c[1] + c[2] * c[2]) / (n * n) : 0; }
    function cnt(ps) { return counts(ps.map(function (p) { return p.y; })); }
    function split(ps) {
      var n = ps.length, best = null;
      for (var f = 0; f < 2; f++) {
        var s = ps.slice().sort(function (a, b) { return a.v[f] - b.v[f]; });
        var L = [0, 0, 0], R = cnt(s);
        for (var i = 1; i < n; i++) {
          L[s[i - 1].y]++; R[s[i - 1].y]--;
          var a = s[i - 1].v[f], b = s[i].v[f];
          if (b <= a + 1e-7) continue;
          var proxy = (L[0] * L[0] + L[1] * L[1] + L[2] * L[2]) / i + (R[0] * R[0] + R[1] * R[1] + R[2] * R[2]) / (n - i);
          if (!best || proxy > best.proxy) {
            var thr = a / 2 + b / 2;
            if (thr === b) thr = a;
            best = { f: f, thr: thr, proxy: proxy };
          }
        }
      }
      return best;
    }
    function grow(ps, depth) {
      var c = cnt(ps), node = { pred: majority(c), f: null };
      if (depth >= maxDepth || ps.length < 2 || gini(c, ps.length) <= 1e-7) return node;
      var b = split(ps);
      if (!b) return node;
      node.f = b.f; node.thr = b.thr;
      node.l = grow(ps.filter(function (p) { return p.v[b.f] <= b.thr; }), depth + 1);
      node.r = grow(ps.filter(function (p) { return p.v[b.f] > b.thr; }), depth + 1);
      return node;
    }
    var root = grow(data, 0);
    return function (a, b) {
      var v = [Math.fround(a), Math.fround(b)], n = root;
      while (n.f !== null) n = v[n.f] <= n.thr ? n.l : n.r;
      return n.pred;
    };
  }

  window.MLModels = { majority: majority, counts: counts, folds: folds, knn: knn, tree: tree };
})();
