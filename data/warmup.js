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
 ]
};
