/* Перевод сайта: выгрузка русских текстов и вставка перевода.
   Запуск (Node.js, без npm):
     node tools/i18n.js export          — i18n/ru/*.json: все тексты страниц (STR.ru), каталога и шапки
     node tools/i18n.js check           — русский текст в коде мимо STR (его перевод не увидит)
     node tools/i18n.js import tg       — i18n/tg/*.json → вставить в страницы, каталог и шапку (с проверками)
   Учебник (book/ml, book/ml2) сюда не входит: его переводят в Word и пересобирают tools/build_book.py. */
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const CYR = /[А-Яа-яЁё]/;

// ---------- Разбор JS: найти объект-литерал по началу, не сбиваясь на строках и комментариях ----------
function scanObject(src, openIdx) {        // openIdx — индекс «{»; вернёт индекс парной «}»
  let depth = 0, i = openIdx, q = null;
  for (; i < src.length; i++) {
    const ch = src[i], nx = src[i + 1];
    if (q) {
      if (ch === '\\') { i++; continue; }
      if (ch === q) q = null;
      continue;
    }
    if (ch === '/' && nx === '/') { i = src.indexOf('\n', i); continue; }
    if (ch === '/' && nx === '*') { i = src.indexOf('*/', i) + 1; continue; }
    if (ch === "'" || ch === '"' || ch === '`') { q = ch; continue; }
    if (ch === '{') depth++;
    else if (ch === '}') { depth--; if (depth === 0) return i; }
  }
  throw new Error('не нашёл конец объекта');
}
function evalObject(text) { return new Function('return (' + text + ');')(); }

// Все страницы со STR: главная, библиотека учебников, уроки
function pages() {
  const list = [['index', 'index.html'], ['book', 'book/index.html'], ['warmup', 'warmup/index.html']];
  fs.readdirSync(path.join(ROOT, 'viz')).sort().forEach(d => {
    const f = path.join('viz', d, 'index.html');
    if (fs.existsSync(path.join(ROOT, f))) list.push([d, f]);
  });
  return list;
}
function strBlock(src) {
  const at = src.indexOf('var STR = {');
  if (at < 0) return null;
  const open = src.indexOf('{', at), close = scanObject(src, open);
  return { open, close, obj: evalObject(src.slice(open, close + 1)) };
}

// ---------- Каталог: тексты уроков, фаз и словаря терминов ----------
function loadCatalog() {
  const w = {};
  new Function('window', fs.readFileSync(path.join(ROOT, 'assets/catalog.js'), 'utf8'))(w);
  return w;
}
function catalogRu(w) {
  const out = {};
  w.CATALOG.forEach((ph, pi) => {
    out[`phase.${pi}.phase`] = ph.phase.ru;
    out[`phase.${pi}.weeks`] = ph.weeks.ru;
    ph.items.forEach(it => {
      out[`item.${it.id}.title`] = it.title.ru;
      out[`item.${it.id}.analogy`] = it.analogy.ru;
      if (it.bridge) out[`item.${it.id}.bridge`] = it.bridge.ru;
      if (it.myths) it.myths.ru.forEach((m, k) => {
        out[`item.${it.id}.myth.${k}.seems`] = m[0];
        out[`item.${it.id}.myth.${k}.truth`] = m[1];
      });
    });
  });
  w.GLOSSARY.forEach((g, k) => {
    out[`glossary.${k}.term`] = g.term.ru;
    out[`glossary.${k}.def`] = g.def.ru;
    out[`glossary.${k}.re_ru`] = g.re;   // основа слова для поиска в тексте — на таджикском нужна своя
  });
  return out;
}

// ---------- Шапка и общие блоки (core.js, объект UI) ----------
function uiBlock(src) {
  const at = src.indexOf('var UI = {');
  const open = src.indexOf('{', at), close = scanObject(src, open);
  return { open, close, obj: evalObject(src.slice(open, close + 1)) };
}

function write(file, obj) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, JSON.stringify(obj, null, 2) + '\n', 'utf8');
}

// ---------- export ----------
function doExport() {
  let n = 0, chars = 0;
  const add = (name, obj) => {
    write(path.join(ROOT, 'i18n/ru', name + '.json'), obj);
    n++; chars += Object.values(obj).join('').length;
  };
  pages().forEach(([name, f]) => {
    const b = strBlock(fs.readFileSync(path.join(ROOT, f), 'utf8'));
    if (b) add('page.' + name, b.obj.ru);
  });
  add('catalog', catalogRu(loadCatalog()));
  add('ui', uiBlock(fs.readFileSync(path.join(ROOT, 'assets/core.js'), 'utf8')).obj.ru);
  console.log(`i18n/ru: ${n} файлов, ${chars} символов текста`);
}

// ---------- check: русский текст в коде мимо STR ----------
function doCheck() {
  let bad = 0;
  const scanFile = (f, skip) => {
    const src = fs.readFileSync(path.join(ROOT, f), 'utf8');
    const scriptAt = src.lastIndexOf('<script>');
    if (scriptAt < 0) return;
    const lines = src.slice(scriptAt).split('\n');
    let line0 = src.slice(0, scriptAt).split('\n').length;
    let inSkip = false, pos = scriptAt;
    lines.forEach((l, k) => {
      const lineStart = pos; pos += l.length + 1;
      if (skip && lineStart >= skip[0] && lineStart <= skip[1]) return;
      const code = l.replace(/\/\/.*$/, '').replace(/\/\*.*?\*\//g, '');
      const lit = code.match(/'[^']*'|"[^"]*"/g) || [];
      lit.filter(s => CYR.test(s)).forEach(s => { bad++; console.log(`${f}:${line0 + k}: ${s.slice(0, 70)}`); });
    });
  };
  pages().forEach(([name, f]) => {
    const src = fs.readFileSync(path.join(ROOT, f), 'utf8');
    const b = strBlock(src);
    scanFile(f, b ? [b.open, b.close] : null);
  });
  console.log(bad ? `Найдено строк: ${bad}` : 'Русского текста мимо STR нет');
}

// ---------- import ----------
const TAGS = s => (s.match(/<\/?[a-z][^>]*>/gi) || []).map(t => t.replace(/\s.*?>/, '>').toLowerCase()).sort().join('');
const VARS = s => (s.match(/\{\w+\}/g) || []).sort().join('');
// Сравнение одного значения: строки — переведены и с теми же тегами/подстановками;
// вложенные списки и объекты (например, задания игры на уроке 2) — той же формы; числа и флажки — без изменений
function compare(ru, tg, k, errs) {
  if (typeof ru === 'string') {
    if (typeof tg !== 'string' || !tg.trim()) { errs.push(`пусто: ${k}`); return; }
    if (VARS(ru) !== VARS(tg)) errs.push(`подстановки {…} не совпадают: ${k}`);
    if (TAGS(ru) !== TAGS(tg)) errs.push(`HTML-теги не совпадают: ${k}`);
    if (ru.includes('|') && ru.split('|').length !== tg.split('|').length) errs.push(`число частей через | не совпадает: ${k}`);
  } else if (Array.isArray(ru)) {
    if (!Array.isArray(tg) || tg.length !== ru.length) { errs.push(`другая длина списка: ${k}`); return; }
    ru.forEach((v, i) => compare(v, tg[i], `${k}[${i}]`, errs));
  } else if (ru && typeof ru === 'object') {
    if (!tg || typeof tg !== 'object') { errs.push(`нет вложенного объекта: ${k}`); return; }
    Object.keys(ru).forEach(c => compare(ru[c], tg[c], `${k}.${c}`, errs));
  } else if (ru !== tg) errs.push(`число или флажок изменён: ${k}`);
}
function validate(name, ru, tg) {
  const errs = [];
  Object.keys(ru).forEach(k => {
    if (k.endsWith('.re_ru')) return;
    if (!(k in tg)) { errs.push(`нет ключа ${k}`); return; }
    compare(ru[k], tg[k], k, errs);
  });
  Object.keys(tg).forEach(k => { if (!(k in ru) && !k.endsWith('.re')) errs.push(`лишний ключ ${k}`); });
  if (errs.length) { console.log(`✗ ${name}:\n  ` + errs.slice(0, 12).join('\n  ') + (errs.length > 12 ? `\n  … ещё ${errs.length - 12}` : '')); return false; }
  return true;
}
const MARK_A = '/* tg:start — перевод вставлен tools/i18n.js, не правьте руками */', MARK_B = '/* tg:end */';
function replaceMarked(src, insertAt, block) {
  const a = src.indexOf(MARK_A);
  if (a >= 0) { const b = src.indexOf(MARK_B, a) + MARK_B.length; return src.slice(0, a) + block + src.slice(b); }
  return src.slice(0, insertAt) + block + src.slice(insertAt);
}
function doImport(lang) {
  const dir = path.join(ROOT, 'i18n', lang);
  let ok = true, done = 0;
  const read = name => {
    const f = path.join(dir, name + '.json');
    if (!fs.existsSync(f)) { console.log(`– нет перевода ${name}.json`); ok = false; return null; }
    // Переводчик иногда добавляет первую строку «// имя файла» или обёртку ```json — их отбрасываем
    const text = fs.readFileSync(f, 'utf8').replace(/^﻿/, '').replace(/^\s*```[a-z]*\s*\n/i, '').replace(/\n```\s*$/, '')
      .replace(/^(\s*\/\/[^\n]*\n)+/, '');
    try { return JSON.parse(text); }
    catch (e) { console.log(`✗ ${name}.json — не JSON: ${e.message}`); ok = false; return null; }
  };
  // Страницы: tg-объект в STR рядом с ru
  pages().forEach(([name, f]) => {
    const file = path.join(ROOT, f), src = fs.readFileSync(file, 'utf8'), b = strBlock(src);
    if (!b) return;
    const tg = read('page.' + name);
    if (!tg || !validate('page.' + name, b.obj.ru, tg)) { ok = false; return; }
    const ordered = {}; Object.keys(b.obj.ru).forEach(k => { ordered[k] = tg[k]; });
    const block = `${MARK_A}\n      ${lang}: ${JSON.stringify(ordered, null, 2).replace(/\n/g, '\n      ')}\n      ${MARK_B}`;
    const at = src.indexOf(MARK_A) >= 0 ? 0 : src.lastIndexOf('}', b.close - 1) + 1;
    let out = src.indexOf(MARK_A) >= 0 ? replaceMarked(src, 0, block) : src.slice(0, at) + `,\n      ${block}` + src.slice(at);
    fs.writeFileSync(file, out, 'utf8'); done++;
  });
  // Каталог: блок в конце catalog.js дописывает tg в объекты уроков и словаря
  const cat = read('catalog'), w = loadCatalog();
  if (cat && validate('catalog', catalogRu(w), cat)) {
    const block = `${MARK_A}\n(function () {\n  var T = ${JSON.stringify(cat, null, 2).replace(/\n/g, '\n  ')};\n  var L = '${lang}';\n` +
      `  window.CATALOG.forEach(function (ph, pi) {\n    ph.phase[L] = T['phase.' + pi + '.phase']; ph.weeks[L] = T['phase.' + pi + '.weeks'];\n` +
      `    ph.items.forEach(function (it) {\n      var p = 'item.' + it.id + '.';\n      it.title[L] = T[p + 'title']; it.analogy[L] = T[p + 'analogy'];\n` +
      `      if (it.bridge) it.bridge[L] = T[p + 'bridge'];\n      if (it.myths) it.myths[L] = it.myths.ru.map(function (_, k) { return [T[p + 'myth.' + k + '.seems'], T[p + 'myth.' + k + '.truth']]; });\n    });\n  });\n` +
      `  window.GLOSSARY.forEach(function (g, k) {\n    g.term[L] = T['glossary.' + k + '.term']; g.def[L] = T['glossary.' + k + '.def'];\n    if (T['glossary.' + k + '.re']) g['re_' + L] = T['glossary.' + k + '.re'];\n  });\n})();\n${MARK_B}`;
    const file = path.join(ROOT, 'assets/catalog.js'), src = fs.readFileSync(file, 'utf8');
    fs.writeFileSync(file, src.indexOf(MARK_A) >= 0 ? replaceMarked(src, 0, block) : src.replace(/\s*$/, '\n\n' + block + '\n'), 'utf8'); done++;
  } else ok = false;
  // Шапка: объект UI.tg в core.js целиком
  const ui = read('ui'), cfile = path.join(ROOT, 'assets/core.js'), csrc = fs.readFileSync(cfile, 'utf8'), u = uiBlock(csrc);
  if (ui && validate('ui', u.obj.ru, ui)) {
    const oldAt = csrc.indexOf('    ' + lang + ': {', u.open);
    let out;
    if (oldAt > 0 && oldAt < u.close) {      // заменить существующий tg-объект
      const open = csrc.indexOf('{', oldAt), close = scanObject(csrc, open);
      out = csrc.slice(0, oldAt) + `    ${lang}: ${JSON.stringify(ui)}` + csrc.slice(close + 1);
    } else out = csrc.slice(0, u.close) + `,\n    ${lang}: ${JSON.stringify(ui)}\n  ` + csrc.slice(u.close);
    fs.writeFileSync(cfile, out, 'utf8'); done++;
  } else ok = false;
  console.log(ok ? `Готово: вставлено ${done} файлов перевода` : `Вставлено ${done}; остальные исправьте и запустите снова`);
}

const [cmd, arg] = process.argv.slice(2);
if (cmd === 'export') doExport();
else if (cmd === 'check') doCheck();
else if (cmd === 'import') doImport(arg || 'tg');
else console.log('node tools/i18n.js export | check | import tg');
