/* Python-разминки к урокам. Сгенерировано tools/build_warmup.py — руками не править.
   Ответы посчитаны настоящим Python: вывод, строка ошибки, все верные порядки строк. */
window.WARMUP = {
 "1": [
  {
   "id": "l1a",
   "type": "out",
   "topic": "if",
   "code": "flipper = 210\nif flipper > 206:\n    print(\"Gentoo\")\nelse:\n    print(\"not Gentoo\")",
   "choices": [
    "Gentoo",
    "not Gentoo",
    "Gentoo\nnot Gentoo",
    "flipper"
   ]
  },
  {
   "id": "l1b",
   "type": "out",
   "topic": "var",
   "code": "border = 200\nborder = border + 6\nprint(border)",
   "choices": [
    "206",
    "200",
    "6",
    "border + 6"
   ]
  },
  {
   "id": "l1c",
   "type": "bug",
   "topic": "if",
   "code": "flipper = 190\nif flipper > 206\n    print(\"Gentoo\")",
   "line": 2,
   "err": "SyntaxError"
  },
  {
   "id": "l1d",
   "type": "parsons",
   "topic": "if",
   "lines": [
    "mass = 5000",
    "if mass > 4500:",
    "    print(\"Gentoo\")",
    "else:",
    "    print(\"not Gentoo\")"
   ],
   "out": "Gentoo",
   "orders": [
    [
     0,
     1,
     2,
     3,
     4
    ]
   ]
  }
 ],
 "2": [
  {
   "id": "l2a",
   "type": "out",
   "topic": "list",
   "code": "masses = [3750, 3800, 3250, 4500]\nprint(masses[1])",
   "choices": [
    "3800",
    "3750",
    "3250",
    "!err"
   ]
  },
  {
   "id": "l2b",
   "type": "out",
   "topic": "dict",
   "code": "penguin = {\"species\": \"Adelie\", \"mass\": 3750}\nprint(penguin[\"species\"])",
   "choices": [
    "Adelie",
    "species",
    "3750",
    "!err"
   ]
  },
  {
   "id": "l2c",
   "type": "bug",
   "topic": "list",
   "code": "masses = [3750, 3800, 3250]\nprint(len(masses))\nprint(masses[3])",
   "line": 3,
   "err": "IndexError"
  },
  {
   "id": "l2d",
   "type": "parsons",
   "topic": "list",
   "lines": [
    "species = [\"Adelie\", \"Gentoo\", \"Adelie\"]",
    "species.append(\"Chinstrap\")",
    "n = len(species)",
    "print(n)"
   ],
   "out": "4",
   "orders": [
    [
     0,
     1,
     2,
     3
    ]
   ]
  }
 ],
 "3": [
  {
   "id": "l3a",
   "type": "out",
   "topic": "loop",
   "code": "total = 0\nfor m in [3000, 4000, 5000]:\n    total = total + m\nprint(total)",
   "choices": [
    "12000",
    "5000",
    "3000\n7000\n12000",
    "0"
   ]
  },
  {
   "id": "l3b",
   "type": "out",
   "topic": "loop",
   "code": "for m in [3, 4, 5]:\n    print(m * 2)",
   "choices": [
    "6\n8\n10",
    "10",
    "6 8 10",
    "3\n4\n5"
   ]
  },
  {
   "id": "l3c",
   "type": "bug",
   "topic": "loop",
   "code": "total = 0\nfor m in [3000, 4000]:\ntotal = total + m\nprint(total)",
   "line": 3,
   "err": "IndentationError"
  },
  {
   "id": "l3d",
   "type": "parsons",
   "topic": "loop",
   "lines": [
    "masses = [3000, 4000, 5000]",
    "total = 0",
    "for m in masses:",
    "    total = total + m",
    "print(total / len(masses))"
   ],
   "out": "4000.0",
   "orders": [
    [
     0,
     1,
     2,
     3,
     4
    ],
    [
     1,
     0,
     2,
     3,
     4
    ]
   ]
  }
 ],
 "4": [
  {
   "id": "l4a",
   "type": "out",
   "topic": "sort",
   "code": "masses = [3800, 3400, 6300, 3600]\nprint(sorted(masses))",
   "choices": [
    "[3400, 3600, 3800, 6300]",
    "[6300, 3800, 3600, 3400]",
    "[3800, 3400, 6300, 3600]",
    "3400"
   ]
  },
  {
   "id": "l4b",
   "type": "out",
   "topic": "sort",
   "code": "masses = sorted([3800, 3400, 6300])\nprint(masses[1])",
   "choices": [
    "3800",
    "4500",
    "3400",
    "6300"
   ]
  },
  {
   "id": "l4c",
   "type": "bug",
   "topic": "none",
   "code": "masses = [3800, None, 3600]\ntotal = 0\nfor m in masses:\n    total = total + m",
   "line": 4,
   "err": "TypeError"
  },
  {
   "id": "l4d",
   "type": "parsons",
   "topic": "none",
   "lines": [
    "masses = [3800, None, 3600]",
    "total = 0",
    "for m in masses:",
    "    if m is not None:",
    "        total = total + m",
    "print(total)"
   ],
   "out": "7400",
   "orders": [
    [
     0,
     1,
     2,
     3,
     4,
     5
    ],
    [
     1,
     0,
     2,
     3,
     4,
     5
    ]
   ]
  }
 ],
 "5": [
  {
   "id": "l5a",
   "type": "out",
   "topic": "func",
   "code": "def dist(a, b):\n    return abs(a - b)\n\nprint(dist(40, 46))",
   "choices": [
    "6",
    "-6",
    "86",
    "!err"
   ]
  },
  {
   "id": "l5b",
   "type": "out",
   "topic": "func",
   "code": "def double(x):\n    return x * 2\n\ny = double(3) + double(4)\nprint(y)",
   "choices": [
    "14",
    "7",
    "6\n8",
    "!err"
   ]
  },
  {
   "id": "l5c",
   "type": "bug",
   "topic": "func",
   "code": "print(dist(40, 46))\n\ndef dist(a, b):\n    return abs(a - b)",
   "line": 1,
   "err": "NameError"
  },
  {
   "id": "l5d",
   "type": "parsons",
   "topic": "loop",
   "lines": [
    "new = 45",
    "bills = [39, 47, 50]",
    "best = bills[0]",
    "for b in bills:",
    "    if abs(b - new) < abs(best - new):",
    "        best = b",
    "print(best)"
   ],
   "out": "47",
   "orders": [
    [
     0,
     1,
     2,
     3,
     4,
     5,
     6
    ],
    [
     1,
     0,
     2,
     3,
     4,
     5,
     6
    ],
    [
     1,
     2,
     0,
     3,
     4,
     5,
     6
    ]
   ]
  }
 ],
 "6": [
  {
   "id": "l6a",
   "type": "out",
   "topic": "slice",
   "code": "data = [1, 2, 3, 4, 5]\ntrain = data[:4]\ntest = data[4:]\nprint(test)",
   "choices": [
    "[5]",
    "[4, 5]",
    "5",
    "[1, 2, 3, 4]"
   ]
  },
  {
   "id": "l6b",
   "type": "out",
   "topic": "loop",
   "code": "truth = [\"A\", \"G\", \"A\", \"C\"]\nguess = [\"A\", \"G\", \"C\", \"C\"]\nright = 0\nfor i in range(4):\n    if truth[i] == guess[i]:\n        right = right + 1\nprint(right / 4)",
   "choices": [
    "0.75",
    "3",
    "75",
    "0.25"
   ]
  },
  {
   "id": "l6c",
   "type": "bug",
   "topic": "if",
   "code": "truth = \"Adelie\"\nguess = \"Adelie\"\nif truth = guess:\n    print(\"right\")",
   "line": 3,
   "err": "SyntaxError"
  },
  {
   "id": "l6d",
   "type": "parsons",
   "topic": "fstr",
   "lines": [
    "right = 3",
    "total = 4",
    "acc = right / total",
    "print(f\"accuracy = {acc}\")"
   ],
   "out": "accuracy = 0.75",
   "orders": [
    [
     0,
     1,
     2,
     3
    ],
    [
     1,
     0,
     2,
     3
    ]
   ]
  }
 ],
 "7": [
  {
   "id": "l7a",
   "type": "out",
   "topic": "elif",
   "code": "bill = 46\nmass = 3800\nif bill < 42:\n    print(\"Adelie\")\nelif mass > 4500:\n    print(\"Gentoo\")\nelse:\n    print(\"Chinstrap\")",
   "choices": [
    "Chinstrap",
    "Adelie",
    "Gentoo",
    "Gentoo\nChinstrap"
   ]
  },
  {
   "id": "l7b",
   "type": "out",
   "topic": "none",
   "code": "for depth in [1, 3, None]:\n    print(depth)",
   "choices": [
    "1\n3\nNone",
    "1\n3",
    "1 3 None",
    "!err"
   ]
  },
  {
   "id": "l7c",
   "type": "bug",
   "topic": "elif",
   "code": "mass = 5000\nif mass > 4500:\n    print(\"Gentoo\")\nelse if mass > 3500:\n    print(\"Chinstrap\")",
   "line": 4,
   "err": "SyntaxError"
  },
  {
   "id": "l7d",
   "type": "parsons",
   "topic": "elif",
   "lines": [
    "for f in [190, 200, 220]:",
    "    if f < 195:",
    "        print(\"Adelie\")",
    "    elif f < 210:",
    "        print(\"Chinstrap\")",
    "    else:",
    "        print(\"Gentoo\")"
   ],
   "out": "Adelie\nChinstrap\nGentoo",
   "orders": [
    [
     0,
     1,
     2,
     3,
     4,
     5,
     6
    ]
   ]
  }
 ],
 "8": [
  {
   "id": "l8a",
   "type": "out",
   "topic": "func",
   "code": "def predict(x):\n    return 10 * x + 15\n\nprint(predict(4))",
   "choices": [
    "55",
    "40",
    "415",
    "10 * 4 + 15"
   ]
  },
  {
   "id": "l8b",
   "type": "out",
   "topic": "math",
   "code": "errors = [4, -2, 3]\ntotal = 0\nfor e in errors:\n    total = total + abs(e)\nprint(total / len(errors))",
   "choices": [
    "3.0",
    "1.6666666666666667",
    "3",
    "9"
   ]
  },
  {
   "id": "l8c",
   "type": "bug",
   "topic": "fmt",
   "code": "errors = [3, 4]\nmse = (3 ** 2 + 4 ** 2) / 2\nprint(\"MSE: \" + mse)",
   "line": 3,
   "err": "TypeError"
  },
  {
   "id": "l8d",
   "type": "parsons",
   "topic": "math",
   "lines": [
    "errors = [2, -4]",
    "total = 0",
    "for e in errors:",
    "    total = total + e ** 2",
    "print(total / len(errors))"
   ],
   "out": "10.0",
   "orders": [
    [
     0,
     1,
     2,
     3,
     4
    ],
    [
     1,
     0,
     2,
     3,
     4
    ]
   ]
  }
 ],
 "9": [
  {
   "id": "l9a",
   "type": "out",
   "topic": "list",
   "code": "votes = [\"Adelie\", \"Gentoo\", \"Adelie\"]\nprint(votes.count(\"Adelie\"))",
   "choices": [
    "2",
    "1",
    "3",
    "!err"
   ]
  },
  {
   "id": "l9b",
   "type": "out",
   "topic": "dict",
   "code": "scores = {\"KNN\": 0.97, \"Forest\": 0.96}\nfor name, acc in scores.items():\n    print(name, acc)",
   "choices": [
    "KNN 0.97\nForest 0.96",
    "KNN\nForest",
    "0.97\n0.96",
    "KNN: 0.97\nForest: 0.96"
   ]
  },
  {
   "id": "l9c",
   "type": "bug",
   "topic": "dict",
   "code": "votes = {\"Adelie\": 5, \"Gentoo\": 3}\nprint(votes[\"Adelie\"])\nprint(votes[\"Chinstrap\"])",
   "line": 3,
   "err": "KeyError"
  },
  {
   "id": "l9d",
   "type": "parsons",
   "topic": "loop",
   "lines": [
    "votes = [\"Adelie\", \"Gentoo\", \"Gentoo\"]",
    "best = votes[0]",
    "for v in votes:",
    "    if votes.count(v) > votes.count(best):",
    "        best = v",
    "print(best)"
   ],
   "out": "Gentoo",
   "orders": [
    [
     0,
     1,
     2,
     3,
     4,
     5
    ]
   ]
  }
 ],
 "10": [
  {
   "id": "l10a",
   "type": "out",
   "topic": "tuple",
   "code": "step = (\"scale\", 2)\nname, k = step\nprint(name)",
   "choices": [
    "scale",
    "2",
    "('scale', 2)",
    "!err"
   ]
  },
  {
   "id": "l10b",
   "type": "out",
   "topic": "func",
   "code": "def double(x):\n    return x * 2\n\ndef add_one(x):\n    return x + 1\n\nprint(add_one(double(5)))",
   "choices": [
    "11",
    "12",
    "10",
    "6"
   ]
  },
  {
   "id": "l10c",
   "type": "bug",
   "topic": "func",
   "code": "def scale(x, mean, std):\n    return (x - mean) / std\n\nprint(scale(50))",
   "line": 4,
   "err": "TypeError"
  },
  {
   "id": "l10d",
   "type": "parsons",
   "topic": "tuple",
   "lines": [
    "steps = [(\"double\", 2), (\"add\", 3)]",
    "x = 5",
    "for name, k in steps:",
    "    if name == \"double\":",
    "        x = x * k",
    "    else:",
    "        x = x + k",
    "print(x)"
   ],
   "out": "13",
   "orders": [
    [
     0,
     1,
     2,
     3,
     4,
     5,
     6,
     7
    ],
    [
     1,
     0,
     2,
     3,
     4,
     5,
     6,
     7
    ]
   ]
  }
 ],
 "11": [
  {
   "id": "l11a",
   "type": "out",
   "topic": "zip",
   "code": "truth = [\"yes\", \"no\", \"yes\"]\npred = [\"yes\", \"yes\", \"no\"]\nfor t, p in zip(truth, pred):\n    print(t == p)",
   "choices": [
    "True\nFalse\nFalse",
    "True",
    "1",
    "True\nTrue\nFalse"
   ]
  },
  {
   "id": "l11b",
   "type": "out",
   "topic": "math",
   "code": "tp = 6\nfp = 2\nprint(tp / (tp + fp))",
   "choices": [
    "0.75",
    "3.0",
    "0.25",
    "8"
   ]
  },
  {
   "id": "l11c",
   "type": "bug",
   "topic": "math",
   "code": "tp = 0\nfp = 0\nprecision = tp / (tp + fp)\nprint(precision)",
   "line": 3,
   "err": "ZeroDivisionError"
  },
  {
   "id": "l11d",
   "type": "parsons",
   "topic": "zip",
   "lines": [
    "truth = [\"yes\", \"no\", \"yes\"]",
    "pred = [\"yes\", \"yes\", \"yes\"]",
    "tp = 0",
    "for t, p in zip(truth, pred):",
    "    if t == \"yes\" and p == \"yes\":",
    "        tp = tp + 1",
    "print(tp)"
   ],
   "out": "2",
   "orders": [
    [
     0,
     1,
     2,
     3,
     4,
     5,
     6
    ],
    [
     0,
     2,
     1,
     3,
     4,
     5,
     6
    ],
    [
     1,
     0,
     2,
     3,
     4,
     5,
     6
    ],
    [
     1,
     2,
     0,
     3,
     4,
     5,
     6
    ],
    [
     2,
     0,
     1,
     3,
     4,
     5,
     6
    ],
    [
     2,
     1,
     0,
     3,
     4,
     5,
     6
    ]
   ]
  }
 ],
 "12": [
  {
   "id": "l12a",
   "type": "out",
   "topic": "math",
   "code": "scores = [0.9, 1.0, 0.8]\nprint(round(sum(scores) / len(scores), 2))",
   "choices": [
    "0.9",
    "2.7",
    "0.8",
    "1.0"
   ]
  },
  {
   "id": "l12b",
   "type": "out",
   "topic": "list",
   "code": "species = [\"Adelie\", \"Gentoo\", \"Adelie\", \"Chinstrap\"]\nbest = max(species, key=species.count)\nprint(best)",
   "choices": [
    "Adelie",
    "Gentoo",
    "Chinstrap",
    "2"
   ]
  },
  {
   "id": "l12c",
   "type": "bug",
   "topic": "var",
   "code": "model = 0.95\nbaseline = 0.44\nprint(model - basline)",
   "line": 3,
   "err": "NameError"
  },
  {
   "id": "l12d",
   "type": "parsons",
   "topic": "if",
   "lines": [
    "model = 0.95",
    "baseline = 0.44",
    "if model > baseline:",
    "    print(\"better\")",
    "else:",
    "    print(\"no better\")"
   ],
   "out": "better",
   "orders": [
    [
     0,
     1,
     2,
     3,
     4,
     5
    ],
    [
     1,
     0,
     2,
     3,
     4,
     5
    ]
   ]
  }
 ],
 "13": [
  {
   "id": "l13a",
   "type": "out",
   "topic": "math",
   "code": "w1 = 2\nw2 = -1\nb = 1\nx1 = 3\nx2 = 4\nprint(w1 * x1 + w2 * x2 + b)",
   "choices": [
    "3",
    "11",
    "2",
    "!err"
   ]
  },
  {
   "id": "l13b",
   "type": "out",
   "topic": "func",
   "code": "def relu(x):\n    return max(0, x)\n\nprint(relu(-5), relu(3))",
   "choices": [
    "0 3",
    "-5 3",
    "0 0",
    "5 3"
   ]
  },
  {
   "id": "l13c",
   "type": "bug",
   "topic": "var",
   "code": "w = 5\nfor step in range(3):\n    w = w - lr * 2 * w\nlr = 0.1",
   "line": 3,
   "err": "NameError"
  },
  {
   "id": "l13d",
   "type": "parsons",
   "topic": "loop",
   "lines": [
    "w = 8",
    "lr = 0.25",
    "for step in range(2):",
    "    w = w - lr * 2 * w",
    "print(w)"
   ],
   "out": "2.0",
   "orders": [
    [
     0,
     1,
     2,
     3,
     4
    ],
    [
     1,
     0,
     2,
     3,
     4
    ]
   ]
  }
 ],
 "14": [
  {
   "id": "l14a",
   "type": "out",
   "topic": "math",
   "code": "pixel = 51\nprint(pixel / 255)",
   "choices": [
    "0.2",
    "51",
    "0",
    "255"
   ]
  },
  {
   "id": "l14b",
   "type": "out",
   "topic": "list",
   "code": "probs = [0.05, 0.1, 0.7, 0.15]\nprint(probs.index(max(probs)))",
   "choices": [
    "2",
    "0.7",
    "3",
    "1"
   ]
  },
  {
   "id": "l14c",
   "type": "bug",
   "topic": "list",
   "code": "image = [[0, 255],\n         [255, 0]]\nprint(image[1][0])\nprint(image[2][0])",
   "line": 4,
   "err": "IndexError"
  },
  {
   "id": "l14d",
   "type": "parsons",
   "topic": "loop",
   "lines": [
    "image = [[0, 255], [255, 0]]",
    "flat = []",
    "for row in image:",
    "    for p in row:",
    "        flat.append(p)",
    "print(flat)"
   ],
   "out": "[0, 255, 255, 0]",
   "orders": [
    [
     0,
     1,
     2,
     3,
     4,
     5
    ],
    [
     1,
     0,
     2,
     3,
     4,
     5
    ]
   ]
  }
 ],
 "15": [
  {
   "id": "l15a",
   "type": "out",
   "topic": "list",
   "code": "img = [[1, 2, 3],\n       [4, 5, 6]]\nprint(img[1][2])",
   "choices": [
    "6",
    "2",
    "5",
    "!err"
   ]
  },
  {
   "id": "l15b",
   "type": "out",
   "topic": "loop",
   "code": "patch = [1, 2, 3]\nkernel = [1, 0, -1]\ntotal = 0\nfor i in range(3):\n    total = total + patch[i] * kernel[i]\nprint(total)",
   "choices": [
    "-2",
    "6",
    "2",
    "0"
   ]
  },
  {
   "id": "l15c",
   "type": "bug",
   "topic": "loop",
   "code": "patch = [1, 2, 3]\ntotal = 0\nfor i in range(4):\n    total = total + patch[i]",
   "line": 4,
   "err": "IndexError"
  },
  {
   "id": "l15d",
   "type": "parsons",
   "topic": "loop",
   "lines": [
    "row = [3, 8, 2, 5]",
    "pooled = []",
    "for i in range(0, 4, 2):",
    "    pooled.append(max(row[i], row[i + 1]))",
    "print(pooled)"
   ],
   "out": "[8, 5]",
   "orders": [
    [
     0,
     1,
     2,
     3,
     4
    ],
    [
     1,
     0,
     2,
     3,
     4
    ]
   ]
  }
 ],
 "16": [
  {
   "id": "l16a",
   "type": "out",
   "topic": "slice",
   "code": "row = [1, 2, 3]\nprint(row[::-1])",
   "choices": [
    "[3, 2, 1]",
    "[1, 2, 3]",
    "3",
    "!err"
   ]
  },
  {
   "id": "l16b",
   "type": "out",
   "topic": "dict",
   "code": "labels = [\"cat\", \"dog\"]\npred = [0.8, 0.2]\nresult = {labels[i]: pred[i] for i in range(2)}\nprint(result[\"dog\"])",
   "choices": [
    "0.2",
    "0.8",
    "dog",
    "!err"
   ]
  },
  {
   "id": "l16c",
   "type": "bug",
   "topic": "if",
   "code": "pred = [0.8, 0.2]\nbest = max(pred)\nif best > \"0.5\":\n    print(\"sure\")",
   "line": 3,
   "err": "TypeError"
  },
  {
   "id": "l16d",
   "type": "parsons",
   "topic": "loop",
   "lines": [
    "labels = [\"cat\", \"dog\", \"cat\"]",
    "guesses = [\"cat\", \"cat\", \"cat\"]",
    "right = 0",
    "for i in range(len(labels)):",
    "    if labels[i] == guesses[i]:",
    "        right = right + 1",
    "print(right, \"/\", len(labels))"
   ],
   "out": "2 / 3",
   "orders": [
    [
     0,
     1,
     2,
     3,
     4,
     5,
     6
    ],
    [
     0,
     2,
     1,
     3,
     4,
     5,
     6
    ],
    [
     1,
     0,
     2,
     3,
     4,
     5,
     6
    ],
    [
     1,
     2,
     0,
     3,
     4,
     5,
     6
    ],
    [
     2,
     0,
     1,
     3,
     4,
     5,
     6
    ],
    [
     2,
     1,
     0,
     3,
     4,
     5,
     6
    ]
   ]
  }
 ],
 "17": [
  {
   "id": "l17a",
   "type": "out",
   "topic": "str",
   "code": "text = \"the cat sat\"\nwords = text.split()\nprint(len(words))",
   "choices": [
    "3",
    "11",
    "1",
    "the cat sat"
   ]
  },
  {
   "id": "l17b",
   "type": "out",
   "topic": "dict",
   "code": "vocab = {\"the\": 0, \"cat\": 1, \"sat\": 2}\nids = [vocab[w] for w in \"cat sat the\".split()]\nprint(ids)",
   "choices": [
    "[1, 2, 0]",
    "[0, 1, 2]",
    "['cat', 'sat', 'the']",
    "!err"
   ]
  },
  {
   "id": "l17c",
   "type": "bug",
   "topic": "str",
   "code": "vocab = {\"the\": 0, \"cat\": 1}\nword = \"Cat\"\nprint(vocab[word])",
   "line": 3,
   "err": "KeyError"
  },
  {
   "id": "l17d",
   "type": "parsons",
   "topic": "loop",
   "lines": [
    "a = [1, 0, 2]",
    "b = [2, 1, 1]",
    "dot = 0",
    "for i in range(3):",
    "    dot = dot + a[i] * b[i]",
    "print(dot)"
   ],
   "out": "4",
   "orders": [
    [
     0,
     1,
     2,
     3,
     4,
     5
    ],
    [
     0,
     2,
     1,
     3,
     4,
     5
    ],
    [
     1,
     0,
     2,
     3,
     4,
     5
    ],
    [
     1,
     2,
     0,
     3,
     4,
     5
    ],
    [
     2,
     0,
     1,
     3,
     4,
     5
    ],
    [
     2,
     1,
     0,
     3,
     4,
     5
    ]
   ]
  }
 ],
 "18": [
  {
   "id": "l18a",
   "type": "out",
   "topic": "fstr",
   "code": "question = \"2 + 2?\"\nprompt = f\"Question: {question}\"\nprint(prompt)",
   "choices": [
    "Question: 2 + 2?",
    "Question: {question}",
    "Question: 4",
    "!err"
   ]
  },
  {
   "id": "l18b",
   "type": "out",
   "topic": "dict",
   "code": "probs = {\"cat\": 0.6, \"dog\": 0.3, \"fish\": 0.1}\nword = max(probs, key=probs.get)\nprint(word)",
   "choices": [
    "cat",
    "0.6",
    "fish",
    "dog"
   ]
  },
  {
   "id": "l18c",
   "type": "bug",
   "topic": "list",
   "code": "messages = [{\"role\": \"user\", \"content\": \"Hi\"}]\nfirst = messages[0]\nprint(first[\"content\"])\nprint(messages[\"content\"])",
   "line": 4,
   "err": "TypeError"
  },
  {
   "id": "l18d",
   "type": "parsons",
   "topic": "str",
   "lines": [
    "examples = [\"good -> pos\", \"bad -> neg\"]",
    "prompt = \"Examples:\\n\"",
    "for e in examples:",
    "    prompt = prompt + e + \"\\n\"",
    "print(prompt)"
   ],
   "out": "Examples:\ngood -> pos\nbad -> neg",
   "orders": [
    [
     0,
     1,
     2,
     3,
     4
    ],
    [
     1,
     0,
     2,
     3,
     4
    ]
   ]
  }
 ],
 "19": [
  {
   "id": "l19a",
   "type": "out",
   "topic": "fmt",
   "code": "score = 0.97345\nprint(f\"{score:.3f}\")",
   "choices": [
    "0.973",
    "0.97345",
    "0.97",
    "{score:.3f}"
   ]
  },
  {
   "id": "l19b",
   "type": "out",
   "topic": "dict",
   "code": "scores = {\"KNN\": 0.93, \"Tree\": 0.95, \"Forest\": 0.97}\nbest = max(scores, key=scores.get)\nprint(best, scores[best])",
   "choices": [
    "Forest 0.97",
    "0.97",
    "KNN 0.93",
    "Forest"
   ]
  },
  {
   "id": "l19c",
   "type": "bug",
   "topic": "dict",
   "code": "scores = {\"KNN\": 0.93, \"Forest\": 0.97}\nfor name in scores:\n    print(name, scores[name])\nprint(scores[\"forest\"])",
   "line": 4,
   "err": "KeyError"
  },
  {
   "id": "l19d",
   "type": "parsons",
   "topic": "loop",
   "lines": [
    "scores = {\"KNN\": 0.93, \"Tree\": 0.95, \"Forest\": 0.97}",
    "best = \"KNN\"",
    "for name in scores:",
    "    if scores[name] > scores[best]:",
    "        best = name",
    "print(best)"
   ],
   "out": "Forest",
   "orders": [
    [
     0,
     1,
     2,
     3,
     4,
     5
    ],
    [
     1,
     0,
     2,
     3,
     4,
     5
    ]
   ]
  }
 ],
 "20": [
  {
   "id": "l20a",
   "type": "out",
   "topic": "func",
   "code": "def predict(h):\n    return round(9.5 * h + 12.3, 1)\n\nprint(predict(4))",
   "choices": [
    "50.3",
    "50",
    "50.0",
    "9.5 * 4 + 12.3"
   ]
  },
  {
   "id": "l20b",
   "type": "out",
   "topic": "func",
   "code": "def hello(name):\n    return \"Hi, \" + name\n\nf = hello\nprint(f(\"Ali\"))",
   "choices": [
    "Hi, Ali",
    "Hi, name",
    "hello",
    "!err"
   ]
  },
  {
   "id": "l20c",
   "type": "bug",
   "topic": "func",
   "code": "def predict(h):\n    return 9.5 * h + 12.3\n\nprint(predict(\"4\"))",
   "line": 2,
   "err": "TypeError"
  },
  {
   "id": "l20d",
   "type": "parsons",
   "topic": "func",
   "lines": [
    "def predict(h):",
    "    score = 9.5 * h + 12.3",
    "    return round(score, 1)",
    "print(predict(2))"
   ],
   "out": "31.3",
   "orders": [
    [
     0,
     1,
     2,
     3
    ]
   ]
  }
 ],
 "21": [
  {
   "id": "l21a",
   "type": "out",
   "topic": "math",
   "code": "baseline = 0.44\nmodel = 0.97\nprint(round((model - baseline) * 100))",
   "choices": [
    "53",
    "0.53",
    "97",
    "44"
   ]
  },
  {
   "id": "l21b",
   "type": "out",
   "topic": "list",
   "code": "columns = [\"species\", \"bill\", \"mass\", \"island\"]\nfeatures = [c for c in columns if c != \"species\"]\nprint(features)",
   "choices": [
    "['bill', 'mass', 'island']",
    "['species']",
    "['species', 'bill', 'mass', 'island']",
    "3"
   ]
  },
  {
   "id": "l21c",
   "type": "bug",
   "topic": "tuple",
   "code": "X_tr, X_te, y_tr = [\"a\", \"b\", \"c\", \"d\"]\nprint(X_tr)",
   "line": 1,
   "err": "ValueError"
  },
  {
   "id": "l21d",
   "type": "parsons",
   "topic": "fstr",
   "lines": [
    "baseline = 0.44",
    "model = 0.97",
    "gain = model - baseline",
    "print(f\"better by {gain:.2f}\")"
   ],
   "out": "better by 0.53",
   "orders": [
    [
     0,
     1,
     2,
     3
    ],
    [
     1,
     0,
     2,
     3
    ]
   ]
  }
 ],
 "22": [
  {
   "id": "l22a",
   "type": "out",
   "topic": "str",
   "code": "text = \"45,4000\"\nparts = text.split(\",\")\nprint(parts)",
   "choices": [
    "['45', '4000']",
    "[45, 4000]",
    "45 4000",
    "['45,4000']"
   ]
  },
  {
   "id": "l22b",
   "type": "out",
   "topic": "str",
   "code": "parts = [\"45\", \"4000\"]\nnums = [float(p) for p in parts]\nprint(nums[0] + 1)",
   "choices": [
    "46.0",
    "451",
    "46",
    "!err"
   ]
  },
  {
   "id": "l22c",
   "type": "bug",
   "topic": "str",
   "code": "text = \"45 mm\"\nvalue = float(text)\nprint(value)",
   "line": 2,
   "err": "ValueError"
  },
  {
   "id": "l22d",
   "type": "parsons",
   "topic": "func",
   "lines": [
    "def predict(text):",
    "    parts = text.split(\",\")",
    "    nums = [float(p) for p in parts]",
    "    return str(sum(nums))",
    "print(predict(\"1,2,3\"))"
   ],
   "out": "6.0",
   "orders": [
    [
     0,
     1,
     2,
     3,
     4
    ]
   ]
  }
 ],
 "23": [
  {
   "id": "l23a",
   "type": "out",
   "topic": "func",
   "code": "def predict(x):\n    print(x * 2)\n\nresult = predict(5)\nprint(result)",
   "choices": [
    "10\nNone",
    "10\n10",
    "10",
    "None"
   ]
  },
  {
   "id": "l23b",
   "type": "out",
   "topic": "try",
   "code": "try:\n    value = float(\"abc\")\nexcept ValueError:\n    value = 0\nprint(value)",
   "choices": [
    "0",
    "abc",
    "0.0",
    "!err"
   ]
  },
  {
   "id": "l23c",
   "type": "bug",
   "topic": "list",
   "code": "words = [\"a\", \"b\"]\nprint(words.length)",
   "line": 2,
   "err": "AttributeError"
  },
  {
   "id": "l23d",
   "type": "parsons",
   "topic": "try",
   "lines": [
    "def safe(text):",
    "    try:",
    "        return float(text) * 2",
    "    except ValueError:",
    "        return \"error\"",
    "print(safe(\"4\"), safe(\"abc\"))"
   ],
   "out": "8.0 error",
   "orders": [
    [
     0,
     1,
     2,
     3,
     4,
     5
    ]
   ]
  }
 ],
 "24": [
  {
   "id": "l24a",
   "type": "out",
   "topic": "list",
   "code": "lessons = list(range(1, 25))\nprint(len(lessons), lessons[-1])",
   "choices": [
    "24 24",
    "24 23",
    "25 24",
    "23 24"
   ]
  },
  {
   "id": "l24b",
   "type": "out",
   "topic": "dict",
   "code": "votes = [\"app\", \"pitch\", \"app\", \"app\"]\ncount = {}\nfor v in votes:\n    count[v] = count.get(v, 0) + 1\nprint(count)",
   "choices": [
    "{'app': 3, 'pitch': 1}",
    "{'app': 1, 'pitch': 1}",
    "3",
    "['app', 'pitch']"
   ]
  },
  {
   "id": "l24c",
   "type": "bug",
   "topic": "func",
   "code": "name = \"Ali\"\nprint \"Thanks, \" + name",
   "line": 2,
   "err": "SyntaxError"
  },
  {
   "id": "l24d",
   "type": "parsons",
   "topic": "math",
   "lines": [
    "scores = [8, 9, 10]",
    "avg = sum(scores) / len(scores)",
    "print(f\"Demo Day: {avg}\")"
   ],
   "out": "Demo Day: 9.0",
   "orders": [
    [
     0,
     1,
     2
    ]
   ]
  }
 ]
};
