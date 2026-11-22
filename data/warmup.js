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
 ]
};
