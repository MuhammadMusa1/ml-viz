/* Каталог визуализаций = карта курса (24 урока).
   Чтобы добавить страницу: создать viz/<id>/index.html и поменять status на 'ready'.
   Тексты — объекты {ru, tg}; пока заполнен только ru. */
window.CATALOG = [
  {
    phase: { ru: 'Фаза 1 · Данные' }, weeks: { ru: 'Недели 1–2' },
    items: [
      { id: 'dataset',     lesson: 2,  status: 'ready',   title: { ru: 'Из чего состоит датасет' },        analogy: { ru: 'Таблица = анкеты пингвинов: признаки и ответ' } },
      { id: 'correlation', lesson: 3,  status: 'ready',   title: { ru: 'Корреляция' },                     analogy: { ru: 'Двигаешь точки — смотришь, как меняется r' } },
      { id: 'outliers',    lesson: 4,  status: 'ready',   title: { ru: 'Выбросы и пропуски' },              analogy: { ru: 'Один «великан» портит среднее' } }
    ]
  },
  {
    phase: { ru: 'Фаза 2 · Классические алгоритмы' }, weeks: { ru: 'Недели 3–6' },
    items: [
      { id: 'knn',        lesson: 5,  status: 'ready',   title: { ru: 'KNN: метод ближайших соседей' },    analogy: { ru: 'Скажи мне, кто твой сосед, — и я скажу, кто ты' } },
      { id: 'train-test', lesson: 6,  status: 'ready',   title: { ru: 'Train / Test' },                    analogy: { ru: 'Нельзя проверять знания по билетам, которые ты видел' } },
      { id: 'tree',       lesson: 7,  status: 'ready',   title: { ru: 'Дерево решений' },                  analogy: { ru: 'Игра «20 вопросов»' } },
      { id: 'linreg',     lesson: 8,  status: 'ready',   title: { ru: 'Линейная регрессия' },              analogy: { ru: 'Положи линейку так, чтобы ошибок было меньше' } },
      { id: 'forest',     lesson: 9,  status: 'ready',   title: { ru: 'Случайный лес' },                   analogy: { ru: 'Голосование всего класса точнее одного мнения' } },
      { id: 'pipeline',   lesson: 10, status: 'ready',   title: { ru: 'Pipeline' },                        analogy: { ru: 'Конвейер: данные заходят — прогноз выходит' } },
      { id: 'confusion',  lesson: 11, status: 'ready',   title: { ru: 'Матрица ошибок, precision, recall' }, analogy: { ru: 'Когда accuracy обманывает' } }
    ]
  },
  {
    phase: { ru: 'Фаза 3 · Нейросети' }, weeks: { ru: 'Недели 7–8' },
    items: [
      { id: 'neuron',      lesson: 13, status: 'ready',   title: { ru: 'Нейрон и активации' },             analogy: { ru: 'Нейрон голосует: «да» или «нет»' } },
      { id: 'gd',          lesson: 13, status: 'ready',   title: { ru: 'Как учится сеть' },                analogy: { ru: 'Спуск с горы в тумане маленькими шагами' } },
      { id: 'convolution', lesson: 15, status: 'ready',   title: { ru: 'Свёртка' },                        analogy: { ru: 'Лупа ищет края и формы на картинке' } }
    ]
  },
  {
    phase: { ru: 'Фаза 4 · Как работают LLM' }, weeks: { ru: 'Недели 9–10' },
    items: [
      { id: 'tokens',      lesson: 17, status: 'ready',   title: { ru: 'Токенизатор' },                    analogy: { ru: 'Как текст режется на кусочки' } },
      { id: 'embeddings',  lesson: 17, status: 'ready',   title: { ru: 'Эмбеддинги' },                     analogy: { ru: 'Карта, где похожие слова живут рядом' } },
      { id: 'attention',   lesson: 17, status: 'ready',   title: { ru: 'Attention' },                      analogy: { ru: 'Кто на кого смотрит в предложении' } },
      { id: 'temperature', lesson: 18, status: 'ready',   title: { ru: 'Температура и галлюцинации' },     analogy: { ru: 'Очень умный автодополнитель, который иногда фантазирует' } }
    ]
  }
];
