"""Python-разминки к урокам: задания -> data/warmup.js.

Правильные ответы не пишем руками: скрипт запускает каждую программу настоящим Python
и сам находит вывод, строку ошибки и все порядки строк, которые дают нужный результат.
Руками пишутся только неверные варианты — скрипт проверяет, что они действительно неверные.

Запуск:  python tools/build_warmup.py
Тексты заданий (условие, объяснение, тема) — в STR страницы warmup/index.html по id задания.

Типы заданий:
  out     — «Что выведет программа?»: варианты = настоящий вывод + wrong ('!err' = «Ошибка»)
  bug     — «В какой строке ошибка?»: варианты = номера строк + «Ошибки нет»
  parsons — «Собери программу»: строки перемешаны, ученик ставит их по порядку
"""
import contextlib
import io
import itertools
import json
import os
import re
import traceback

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Урок -> задания. Только то, что понадобится на этом уроке курса (ноутбук chNN).
TASKS = {
    1: [
        dict(id='l1a', type='out', topic='if', code='''
flipper = 210
if flipper > 206:
    print("Gentoo")
else:
    print("not Gentoo")
''', wrong=['not Gentoo', 'Gentoo\nnot Gentoo', 'flipper']),
        dict(id='l1b', type='out', topic='var', code='''
border = 200
border = border + 6
print(border)
''', wrong=['200', '6', 'border + 6']),
        dict(id='l1c', type='bug', topic='if', code='''
flipper = 190
if flipper > 206
    print("Gentoo")
'''),
        dict(id='l1d', type='parsons', topic='if', code='''
mass = 5000
if mass > 4500:
    print("Gentoo")
else:
    print("not Gentoo")
'''),
    ],
    2: [
        dict(id='l2a', type='out', topic='list', code='''
masses = [3750, 3800, 3250, 4500]
print(masses[1])
''', wrong=['3750', '3250', '!err']),
        dict(id='l2b', type='out', topic='dict', code='''
penguin = {"species": "Adelie", "mass": 3750}
print(penguin["species"])
''', wrong=['species', '3750', '!err']),
        dict(id='l2c', type='bug', topic='list', code='''
masses = [3750, 3800, 3250]
print(len(masses))
print(masses[3])
'''),
        dict(id='l2d', type='parsons', topic='list', code='''
species = ["Adelie", "Gentoo", "Adelie"]
species.append("Chinstrap")
n = len(species)
print(n)
'''),
    ],
    3: [
        dict(id='l3a', type='out', topic='loop', code='''
total = 0
for m in [3000, 4000, 5000]:
    total = total + m
print(total)
''', wrong=['5000', '3000\n7000\n12000', '0']),
        dict(id='l3b', type='out', topic='loop', code='''
for m in [3, 4, 5]:
    print(m * 2)
''', wrong=['10', '6 8 10', '3\n4\n5']),
        dict(id='l3c', type='bug', topic='loop', code='''
total = 0
for m in [3000, 4000]:
total = total + m
print(total)
'''),
        dict(id='l3d', type='parsons', topic='loop', code='''
masses = [3000, 4000, 5000]
total = 0
for m in masses:
    total = total + m
print(total / len(masses))
'''),
    ],
    4: [
        dict(id='l4a', type='out', topic='sort', code='''
masses = [3800, 3400, 6300, 3600]
print(sorted(masses))
''', wrong=['[6300, 3800, 3600, 3400]', '[3800, 3400, 6300, 3600]', '3400']),
        dict(id='l4b', type='out', topic='sort', code='''
masses = sorted([3800, 3400, 6300])
print(masses[1])
''', wrong=['4500', '3400', '6300']),
        dict(id='l4c', type='bug', topic='none', code='''
masses = [3800, None, 3600]
total = 0
for m in masses:
    total = total + m
'''),
        dict(id='l4d', type='parsons', topic='none', code='''
masses = [3800, None, 3600]
total = 0
for m in masses:
    if m is not None:
        total = total + m
print(total)
'''),
    ],
    5: [
        dict(id='l5a', type='out', topic='func', code='''
def dist(a, b):
    return abs(a - b)

print(dist(40, 46))
''', wrong=['-6', '86', '!err']),
        dict(id='l5b', type='out', topic='func', code='''
def double(x):
    return x * 2

y = double(3) + double(4)
print(y)
''', wrong=['7', '6\n8', '!err']),
        dict(id='l5c', type='bug', topic='func', code='''
print(dist(40, 46))

def dist(a, b):
    return abs(a - b)
'''),
        dict(id='l5d', type='parsons', topic='loop', code='''
new = 45
bills = [39, 47, 50]
best = bills[0]
for b in bills:
    if abs(b - new) < abs(best - new):
        best = b
print(best)
'''),
    ],
    6: [
        dict(id='l6a', type='out', topic='slice', code='''
data = [1, 2, 3, 4, 5]
train = data[:4]
test = data[4:]
print(test)
''', wrong=['[4, 5]', '5', '[1, 2, 3, 4]']),
        dict(id='l6b', type='out', topic='loop', code='''
truth = ["A", "G", "A", "C"]
guess = ["A", "G", "C", "C"]
right = 0
for i in range(4):
    if truth[i] == guess[i]:
        right = right + 1
print(right / 4)
''', wrong=['3', '75', '0.25']),
        dict(id='l6c', type='bug', topic='if', code='''
truth = "Adelie"
guess = "Adelie"
if truth = guess:
    print("right")
'''),
        dict(id='l6d', type='parsons', topic='fstr', code='''
right = 3
total = 4
acc = right / total
print(f"accuracy = {acc}")
'''),
    ],
    # Урок 7 — дерево решений: вопросы по очереди (if / elif / else), max_depth=None
    7: [
        dict(id='l7a', type='out', topic='elif', code='''
bill = 46
mass = 3800
if bill < 42:
    print("Adelie")
elif mass > 4500:
    print("Gentoo")
else:
    print("Chinstrap")
''', wrong=['Adelie', 'Gentoo', 'Gentoo\nChinstrap']),
        dict(id='l7b', type='out', topic='none', code='''
for depth in [1, 3, None]:
    print(depth)
''', wrong=['1\n3', '1 3 None', '!err']),
        dict(id='l7c', type='bug', topic='elif', code='''
mass = 5000
if mass > 4500:
    print("Gentoo")
else if mass > 3500:
    print("Chinstrap")
'''),
        # Цикл по трём пингвинам: так проверяются все три ветки, и перепутать их тела не получится
        dict(id='l7d', type='parsons', topic='elif', code='''
for f in [190, 200, 220]:
    if f < 195:
        print("Adelie")
    elif f < 210:
        print("Chinstrap")
    else:
        print("Gentoo")
'''),
    ],
    # Урок 8 — линейная регрессия: прямая как функция, MAE и MSE
    8: [
        dict(id='l8a', type='out', topic='func', code='''
def predict(x):
    return 10 * x + 15

print(predict(4))
''', wrong=['40', '415', '10 * 4 + 15']),
        dict(id='l8b', type='out', topic='math', code='''
errors = [4, -2, 3]
total = 0
for e in errors:
    total = total + abs(e)
print(total / len(errors))
''', wrong=['1.6666666666666667', '3', '9']),
        dict(id='l8c', type='bug', topic='fmt', code='''
errors = [3, 4]
mse = (3 ** 2 + 4 ** 2) / 2
print("MSE: " + mse)
'''),
        dict(id='l8d', type='parsons', topic='math', code='''
errors = [2, -4]
total = 0
for e in errors:
    total = total + e ** 2
print(total / len(errors))
'''),
    ],
    # Урок 9 — случайный лес: голоса деревьев, словарь моделей
    9: [
        dict(id='l9a', type='out', topic='list', code='''
votes = ["Adelie", "Gentoo", "Adelie"]
print(votes.count("Adelie"))
''', wrong=['1', '3', '!err']),
        dict(id='l9b', type='out', topic='dict', code='''
scores = {"KNN": 0.97, "Forest": 0.96}
for name, acc in scores.items():
    print(name, acc)
''', wrong=['KNN\nForest', '0.97\n0.96', 'KNN: 0.97\nForest: 0.96']),
        dict(id='l9c', type='bug', topic='dict', code='''
votes = {"Adelie": 5, "Gentoo": 3}
print(votes["Adelie"])
print(votes["Chinstrap"])
'''),
        # Первый голос — не победитель: иначе программа «угадала» бы и без цикла
        dict(id='l9d', type='parsons', topic='loop', code='''
votes = ["Adelie", "Gentoo", "Gentoo"]
best = votes[0]
for v in votes:
    if votes.count(v) > votes.count(best):
        best = v
print(best)
'''),
    ],
    # Урок 10 — Pipeline: шаги-пары («имя», шаг), результат одного шага идёт в следующий
    10: [
        dict(id='l10a', type='out', topic='tuple', code='''
step = ("scale", 2)
name, k = step
print(name)
''', wrong=['2', "('scale', 2)", '!err']),
        dict(id='l10b', type='out', topic='func', code='''
def double(x):
    return x * 2

def add_one(x):
    return x + 1

print(add_one(double(5)))
''', wrong=['12', '10', '6']),
        dict(id='l10c', type='bug', topic='func', code='''
def scale(x, mean, std):
    return (x - mean) / std

print(scale(50))
'''),
        dict(id='l10d', type='parsons', topic='tuple', code='''
steps = [("double", 2), ("add", 3)]
x = 5
for name, k in steps:
    if name == "double":
        x = x * k
    else:
        x = x + k
print(x)
'''),
    ],
    # Урок 11 — матрица ошибок: идём по правде и ответам модели парами, считаем TP и precision
    11: [
        dict(id='l11a', type='out', topic='zip', code='''
truth = ["yes", "no", "yes"]
pred = ["yes", "yes", "no"]
for t, p in zip(truth, pred):
    print(t == p)
''', wrong=['True', '1', 'True\nTrue\nFalse']),
        dict(id='l11b', type='out', topic='math', code='''
tp = 6
fp = 2
print(tp / (tp + fp))
''', wrong=['3.0', '0.25', '8']),
        dict(id='l11c', type='bug', topic='math', code='''
tp = 0
fp = 0
precision = tp / (tp + fp)
print(precision)
'''),
        dict(id='l11d', type='parsons', topic='zip', code='''
truth = ["yes", "no", "yes"]
pred = ["yes", "yes", "yes"]
tp = 0
for t, p in zip(truth, pred):
    if t == "yes" and p == "yes":
        tp = tp + 1
print(tp)
'''),
    ],
    # Урок 12 — мини-проект: среднее по кросс-валидации, «ленивая» модель, сравнение с baseline
    12: [
        dict(id='l12a', type='out', topic='math', code='''
scores = [0.9, 1.0, 0.8]
print(round(sum(scores) / len(scores), 2))
''', wrong=['2.7', '0.8', '1.0']),
        dict(id='l12b', type='out', topic='list', code='''
species = ["Adelie", "Gentoo", "Adelie", "Chinstrap"]
best = max(species, key=species.count)
print(best)
''', wrong=['Gentoo', 'Chinstrap', '2']),
        dict(id='l12c', type='bug', topic='var', code='''
model = 0.95
baseline = 0.44
print(model - basline)
'''),
        dict(id='l12d', type='parsons', topic='if', code='''
model = 0.95
baseline = 0.44
if model > baseline:
    print("better")
else:
    print("no better")
'''),
    ],
    # Урок 13 — нейрон и градиентный спуск: взвешенная сумма, ReLU, шаг против градиента
    13: [
        dict(id='l13a', type='out', topic='math', code='''
w1 = 2
w2 = -1
b = 1
x1 = 3
x2 = 4
print(w1 * x1 + w2 * x2 + b)
''', wrong=['11', '2', '!err']),
        dict(id='l13b', type='out', topic='func', code='''
def relu(x):
    return max(0, x)

print(relu(-5), relu(3))
''', wrong=['-5 3', '0 0', '5 3']),
        dict(id='l13c', type='bug', topic='var', code='''
w = 5
for step in range(3):
    w = w - lr * 2 * w
lr = 0.1
'''),
        dict(id='l13d', type='parsons', topic='loop', code='''
w = 8
lr = 0.25
for step in range(2):
    w = w - lr * 2 * w
print(w)
'''),
    ],
    # Урок 14 — MNIST: яркость /255, номер самой большой вероятности, картинка в одну строку
    14: [
        dict(id='l14a', type='out', topic='math', code='''
pixel = 51
print(pixel / 255)
''', wrong=['51', '0', '255']),
        dict(id='l14b', type='out', topic='list', code='''
probs = [0.05, 0.1, 0.7, 0.15]
print(probs.index(max(probs)))
''', wrong=['0.7', '3', '1']),
        dict(id='l14c', type='bug', topic='list', code='''
image = [[0, 255],
         [255, 0]]
print(image[1][0])
print(image[2][0])
'''),
        dict(id='l14d', type='parsons', topic='loop', code='''
image = [[0, 255], [255, 0]]
flat = []
for row in image:
    for p in row:
        flat.append(p)
print(flat)
'''),
    ],
    # Урок 15 — свёртка: строки и столбцы картинки, фильтр, max pooling
    15: [
        dict(id='l15a', type='out', topic='list', code='''
img = [[1, 2, 3],
       [4, 5, 6]]
print(img[1][2])
''', wrong=['2', '5', '!err']),
        dict(id='l15b', type='out', topic='loop', code='''
patch = [1, 2, 3]
kernel = [1, 0, -1]
total = 0
for i in range(3):
    total = total + patch[i] * kernel[i]
print(total)
''', wrong=['6', '2', '0']),
        dict(id='l15c', type='bug', topic='loop', code='''
patch = [1, 2, 3]
total = 0
for i in range(4):
    total = total + patch[i]
'''),
        dict(id='l15d', type='parsons', topic='loop', code='''
row = [3, 8, 2, 5]
pooled = []
for i in range(0, 4, 2):
    pooled.append(max(row[i], row[i + 1]))
print(pooled)
'''),
    ],
    # Урок 16 — свои картинки: отражение (аугментация), словарь «класс → вероятность» для Gradio
    16: [
        dict(id='l16a', type='out', topic='slice', code='''
row = [1, 2, 3]
print(row[::-1])
''', wrong=['[1, 2, 3]', '3', '!err']),
        dict(id='l16b', type='out', topic='dict', code='''
labels = ["cat", "dog"]
pred = [0.8, 0.2]
result = {labels[i]: pred[i] for i in range(2)}
print(result["dog"])
''', wrong=['0.8', 'dog', '!err']),
        dict(id='l16c', type='bug', topic='if', code='''
pred = [0.8, 0.2]
best = max(pred)
if best > "0.5":
    print("sure")
'''),
        dict(id='l16d', type='parsons', topic='loop', code='''
labels = ["cat", "dog", "cat"]
guesses = ["cat", "cat", "cat"]
right = 0
for i in range(len(labels)):
    if labels[i] == guesses[i]:
        right = right + 1
print(right, "/", len(labels))
'''),
    ],
    # Урок 17 — токены, эмбеддинги, attention: слова → номера, похожесть векторов
    17: [
        dict(id='l17a', type='out', topic='str', code='''
text = "the cat sat"
words = text.split()
print(len(words))
''', wrong=['11', '1', 'the cat sat']),
        dict(id='l17b', type='out', topic='dict', code='''
vocab = {"the": 0, "cat": 1, "sat": 2}
ids = [vocab[w] for w in "cat sat the".split()]
print(ids)
''', wrong=['[0, 1, 2]', "['cat', 'sat', 'the']", '!err']),
        dict(id='l17c', type='bug', topic='str', code='''
vocab = {"the": 0, "cat": 1}
word = "Cat"
print(vocab[word])
'''),
        dict(id='l17d', type='parsons', topic='loop', code='''
a = [1, 0, 2]
b = [2, 1, 1]
dot = 0
for i in range(3):
    dot = dot + a[i] * b[i]
print(dot)
'''),
    ],
    # Урок 18 — температура и LLM: промпт f-строкой, самое вероятное слово, сообщения для API
    18: [
        dict(id='l18a', type='out', topic='fstr', code='''
question = "2 + 2?"
prompt = f"Question: {question}"
print(prompt)
''', wrong=['Question: {question}', 'Question: 4', '!err']),
        dict(id='l18b', type='out', topic='dict', code='''
probs = {"cat": 0.6, "dog": 0.3, "fish": 0.1}
word = max(probs, key=probs.get)
print(word)
''', wrong=['0.6', 'fish', 'dog']),
        dict(id='l18c', type='bug', topic='list', code='''
messages = [{"role": "user", "content": "Hi"}]
first = messages[0]
print(first["content"])
print(messages["content"])
'''),
        dict(id='l18d', type='parsons', topic='str', code='''
examples = ["good -> pos", "bad -> neg"]
prompt = "Examples:\\n"
for e in examples:
    prompt = prompt + e + "\\n"
print(prompt)
'''),
    ],
    # Урок 19 — AutoML: перебор моделей, лучшая по оценке, ровная печать результатов
    19: [
        dict(id='l19a', type='out', topic='fmt', code='''
score = 0.97345
print(f"{score:.3f}")
''', wrong=['0.97345', '0.97', '{score:.3f}']),
        dict(id='l19b', type='out', topic='dict', code='''
scores = {"KNN": 0.93, "Tree": 0.95, "Forest": 0.97}
best = max(scores, key=scores.get)
print(best, scores[best])
''', wrong=['0.97', 'KNN 0.93', 'Forest']),
        dict(id='l19c', type='bug', topic='dict', code='''
scores = {"KNN": 0.93, "Forest": 0.97}
for name in scores:
    print(name, scores[name])
print(scores["forest"])
'''),
        # Первая модель — не лучшая: иначе программа «угадала» бы и без сравнения
        dict(id='l19d', type='parsons', topic='loop', code='''
scores = {"KNN": 0.93, "Tree": 0.95, "Forest": 0.97}
best = "KNN"
for name in scores:
    if scores[name] > scores[best]:
        best = name
print(best)
'''),
    ],
    # Урок 20 — Gradio: функция прогноза, функцию передают (fn=predict), а вызывает её Gradio
    20: [
        dict(id='l20a', type='out', topic='func', code='''
def predict(h):
    return round(9.5 * h + 12.3, 1)

print(predict(4))
''', wrong=['50', '50.0', '9.5 * 4 + 12.3']),
        dict(id='l20b', type='out', topic='func', code='''
def hello(name):
    return "Hi, " + name

f = hello
print(f("Ali"))
''', wrong=['Hi, name', 'hello', '!err']),
        dict(id='l20c', type='bug', topic='func', code='''
def predict(h):
    return 9.5 * h + 12.3

print(predict("4"))
'''),
        dict(id='l20d', type='parsons', topic='func', code='''
def predict(h):
    score = 9.5 * h + 12.3
    return round(score, 1)
print(predict(2))
'''),
    ],
    # Урок 21 — финальный проект, питч: признаки без ответа, сравнение с baseline
    21: [
        dict(id='l21a', type='out', topic='math', code='''
baseline = 0.44
model = 0.97
print(round((model - baseline) * 100))
''', wrong=['0.53', '97', '44']),
        dict(id='l21b', type='out', topic='list', code='''
columns = ["species", "bill", "mass", "island"]
features = [c for c in columns if c != "species"]
print(features)
''', wrong=["['species']", "['species', 'bill', 'mass', 'island']", '3']),
        dict(id='l21c', type='bug', topic='tuple', code='''
X_tr, X_te, y_tr = ["a", "b", "c", "d"]
print(X_tr)
'''),
        dict(id='l21d', type='parsons', topic='fstr', code='''
baseline = 0.44
model = 0.97
gain = model - baseline
print(f"better by {gain:.2f}")
'''),
    ],
    # Урок 22 — финальный проект, сборка: из текстового поля приходит строка — её превращают в числа
    22: [
        dict(id='l22a', type='out', topic='str', code='''
text = "45,4000"
parts = text.split(",")
print(parts)
''', wrong=['[45, 4000]', '45 4000', "['45,4000']"]),
        dict(id='l22b', type='out', topic='str', code='''
parts = ["45", "4000"]
nums = [float(p) for p in parts]
print(nums[0] + 1)
''', wrong=['451', '46', '!err']),
        dict(id='l22c', type='bug', topic='str', code='''
text = "45 mm"
value = float(text)
print(value)
'''),
        dict(id='l22d', type='parsons', topic='func', code='''
def predict(text):
    parts = text.split(",")
    nums = [float(p) for p in parts]
    return str(sum(nums))
print(predict("1,2,3"))
'''),
    ],
    # Урок 23 — репетиция: ошибки, которые чаще всего ломают проект на защите
    23: [
        dict(id='l23a', type='out', topic='func', code='''
def predict(x):
    print(x * 2)

result = predict(5)
print(result)
''', wrong=['10\n10', '10', 'None']),
        dict(id='l23b', type='out', topic='try', code='''
try:
    value = float("abc")
except ValueError:
    value = 0
print(value)
''', wrong=['abc', '0.0', '!err']),
        dict(id='l23c', type='bug', topic='list', code='''
words = ["a", "b"]
print(words.length)
'''),
        # Две проверки сразу: нормальный ввод и неправильный — иначе ветки try и except можно было бы перепутать
        dict(id='l23d', type='parsons', topic='try', code='''
def safe(text):
    try:
        return float(text) * 2
    except ValueError:
        return "error"
print(safe("4"), safe("abc"))
'''),
    ],
    # Урок 24 — Demo Day: итоговое повторение главных конструкций курса
    24: [
        dict(id='l24a', type='out', topic='list', code='''
lessons = list(range(1, 25))
print(len(lessons), lessons[-1])
''', wrong=['24 23', '25 24', '23 24']),
        dict(id='l24b', type='out', topic='dict', code='''
votes = ["app", "pitch", "app", "app"]
count = {}
for v in votes:
    count[v] = count.get(v, 0) + 1
print(count)
''', wrong=["{'app': 1, 'pitch': 1}", '3', "['app', 'pitch']"]),
        dict(id='l24c', type='bug', topic='func', code='''
name = "Ali"
print "Thanks, " + name
'''),
        dict(id='l24d', type='parsons', topic='math', code='''
scores = [8, 9, 10]
avg = sum(scores) / len(scores)
print(f"Demo Day: {avg}")
'''),
    ],
}


def run(src):
    """Запускает программу. Возвращает (вывод, None) или (вывод до ошибки, (номер строки, тип ошибки))."""
    out = io.StringIO()
    try:
        code = compile(src, '<warmup>', 'exec')
    except SyntaxError as e:          # сюда же попадает IndentationError
        return '', (e.lineno, type(e).__name__)
    try:
        with contextlib.redirect_stdout(out):
            exec(code, {'__name__': '__warmup__'})
    except Exception as e:
        line = [f.lineno for f in traceback.extract_tb(e.__traceback__) if f.filename == '<warmup>'][-1]
        return out.getvalue(), (line, type(e).__name__)
    return out.getvalue(), None


def build(t):
    code = t['code'].strip('\n')
    lines = code.split('\n')
    out, err = run(code)
    r = {'id': t['id'], 'type': t['type'], 'topic': t['topic']}
    if t['type'] == 'out':
        assert err is None, f"{t['id']}: программа должна работать, а падает: {err}"
        shown = out.rstrip('\n')
        for w in t['wrong']:
            assert w != shown, f"{t['id']}: неверный вариант {w!r} совпадает с настоящим выводом"
        assert len(set(t['wrong'])) == len(t['wrong']), f"{t['id']}: повтор в неверных вариантах"
        r.update(code=code, choices=[shown] + t['wrong'])
    elif t['type'] == 'bug':
        assert err is not None, f"{t['id']}: в программе нет ошибки"
        r.update(code=code, line=err[0], err=err[1])
    else:
        assert err is None, f"{t['id']}: собранная программа падает: {err}"
        # Все порядки строк, которые дают тот же вывод, тоже считаются верными
        orders = []
        for p in itertools.permutations(range(len(lines))):
            o, e = run('\n'.join(lines[i] for i in p))
            if e is None and o == out:
                orders.append(list(p))
        assert list(range(len(lines))) in orders
        r.update(lines=lines, out=out.rstrip('\n'), orders=orders)
    return r


def main():
    data = {str(n): [build(t) for t in ts] for n, ts in TASKS.items()}
    ids = [t['id'] for ts in TASKS.values() for t in ts]
    assert len(ids) == len(set(ids)), 'повтор id задания'

    # Ссылка «Python-разминка» на странице урока появляется по списку COURSE.warmup в catalog.js
    cat = open(os.path.join(ROOT, 'assets', 'catalog.js'), encoding='utf-8').read()
    m = re.search(r'warmup:\s*\[([^\]]*)\]', cat)
    listed = sorted(int(x) for x in re.findall(r'\d+', m.group(1))) if m else []
    assert listed == sorted(TASKS), f'COURSE.warmup в catalog.js = {listed}, а разминки есть к урокам {sorted(TASKS)}'

    # Тексты заданий лежат в STR страницы — проверяем, что ни одно не забыто
    page = open(os.path.join(ROOT, 'warmup', 'index.html'), encoding='utf-8').read()
    ru = page[page.index('ru: {'):page.index('/* tg:start')]
    for ts in TASKS.values():
        for t in ts:
            need = ['x_' + t['id']] + (['g_' + t['id']] if t['type'] == 'parsons' else [])
            need.append('topic_' + t['topic'])
            for k in need:
                assert re.search(r'\b' + k + r':', ru), f'в STR.ru страницы warmup нет ключа {k}'

    js = ('/* Python-разминки к урокам. Сгенерировано tools/build_warmup.py — руками не править.\n'
          '   Ответы посчитаны настоящим Python: вывод, строка ошибки, все верные порядки строк. */\n'
          'window.WARMUP = ' + json.dumps(data, ensure_ascii=False, indent=1) + ';\n')
    with open(os.path.join(ROOT, 'data', 'warmup.js'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(js)
    for n, ts in data.items():
        info = []
        for t in ts:
            if t['type'] == 'bug':
                info.append(f"{t['id']} строка {t['line']} {t['err']}")
            elif t['type'] == 'parsons':
                info.append(f"{t['id']} порядков {len(t['orders'])}")
            else:
                info.append(f"{t['id']} = {t['choices'][0]!r}")
        print(f'урок {n}: ' + '; '.join(info))
    print('data/warmup.js записан')


if __name__ == '__main__':
    main()
