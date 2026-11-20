"""Сверка: страница viz/what-is-ml (урок 1) должна совпадать с sklearn.

Запуск:  pip install palmerpenguins scikit-learn
         python tools/check_what_is_ml.py
Задача: «Gentoo или нет?» по одному признаку. Компьютер ищет правило «если признак > порога → Gentoo»
так же, как DecisionTreeClassifier(max_depth=1), по первым n обучающим пингвинам (порядок как в X_train).
Для каждого признака и n печатает порог, сторону Gentoo и сколько из 69 новых пингвинов угадано.
Те же числа показывает панель «Правило компьютера» на странице.
"""
from palmerpenguins import load_penguins
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

df = load_penguins().drop(columns=['sex']).dropna().reset_index(drop=True)
FEATURES = ['flipper_length_mm', 'body_mass_g', 'bill_length_mm', 'bill_depth_mm']
X = df[FEATURES]
y = df['species'] == 'Gentoo'   # ответ: Gentoo или нет
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f'Ленивая модель (всегда «не Gentoo»): {int((~y_test).sum())}/{len(y_test)}')


def flipper_threshold(n):
    m = DecisionTreeClassifier(max_depth=1).fit(X_train[['flipper_length_mm']][:n], y_train[:n])
    return m.tree_.threshold[0]


# На этих числах держатся тексты страницы («Попробуй сам»: граница прыгает на 13 и 14 примерах;
# до 8 примеров правила нет). Если данные или порядок X_train изменятся — тексты надо переписать.
assert all(DecisionTreeClassifier(max_depth=1).fit(X_train[['flipper_length_mm']][:n], y_train[:n]).tree_.node_count == 1
           for n in range(1, 9)), 'до 8 примеров должно не быть правила'
assert (flipper_threshold(12), flipper_threshold(13), flipper_threshold(14)) == (213, 210, 213), 'граница на 12/13/14 примерах изменилась'
print('Тексты страницы (нет правила до 8 примеров, прыжок 213 → 210 → 213): OK')
for f in FEATURES:
    print(f)
    for n in list(range(1, 31)) + [40, 50, 60, 80, 100, 150, 200, 273]:
        model = DecisionTreeClassifier(max_depth=1)
        model.fit(X_train[[f]][:n], y_train[:n])
        correct = int((model.predict(X_test[[f]]) == y_test).sum())
        t = model.tree_
        if t.node_count == 1:
            rule = 'всегда «Gentoo»' if model.classes_[t.value[0][0].argmax()] else 'всегда «не Gentoo»'
        else:
            left_gentoo = model.classes_[t.value[t.children_left[0]][0].argmax()]
            right_gentoo = model.classes_[t.value[t.children_right[0]][0].argmax()]
            if left_gentoo == right_gentoo:   # граница есть, но ответ с обеих сторон один
                rule = f'граница {t.threshold[0]:g}, всегда «{"Gentoo" if left_gentoo else "не Gentoo"}»'
            else:
                rule = f'{"больше" if right_gentoo else "меньше"} {t.threshold[0]:g}'
        print(f'  n={n:3d}: {rule:22s} {correct}/{len(y_test)}')
