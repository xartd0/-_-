### Задача 1
Реализовать на Jsonnet приведенный ниже пример в формате JSON. Использовать в реализации свойство программируемости и принцип DRY.
```bash
{
  groups: [
    std.join("-", ["ИКБО", std.toString(i), "20"]) for i in std.range(1, 24)
  ],

  students: [
    { age: 19, group: "ИКБО-4-20", name: "Иванов И.И." },
    { age: 18, group: "ИКБО-5-20", name: "Петров П.П." },
    { age: 18, group: "ИКБО-5-20", name: "Сидоров С.С." },
    { age: 20, group: "ИКБО-6-20", name: "Кузнецов К.К." } // новый студент
  ],

  subject: "Конфигурационное управление"
}
```

### Задача 2
Реализовать на Dhall приведенный ниже пример в формате JSON. Использовать в реализации свойство программируемости и принцип DRY.
```bash
{
  "groups": [
    "ИКБО-1-20",
    "ИКБО-2-20",
    "ИКБО-3-20",
    "ИКБО-4-20",
    "ИКБО-5-20",
    "ИКБО-6-20",
    "ИКБО-7-20",
    "ИКБО-8-20",
    "ИКБО-9-20",
    "ИКБО-10-20",
    "ИКБО-11-20",
    "ИКБО-12-20",
    "ИКБО-13-20",
    "ИКБО-14-20",
    "ИКБО-15-20",
    "ИКБО-16-20",
    "ИКБО-17-20",
    "ИКБО-18-20",
    "ИКБО-19-20",
    "ИКБО-20-20",
    "ИКБО-21-20",
    "ИКБО-22-20",
    "ИКБО-23-20",
    "ИКБО-24-20"
  ],
  "students": [
    {
      "age": 19,
      "group": "ИКБО-4-20",
      "name": "Иванов И.И."
    },
    {
      "age": 18,
      "group": "ИКБО-5-20",
      "name": "Петров П.П."
    },
    {
      "age": 18,
      "group": "ИКБО-5-20",
      "name": "Сидоров С.С."
    },
    <добавьте ваши данные в качестве четвертого студента>
  ],
  "subject": "Конфигурационное управление"
} 
```

```bash
let Prelude = https://prelude.dhall-lang.org/v20.2.0/package.dhall
let generateGroup = λ(i : Natural) → "ИКБО-" ++ Prelude.Natural.show i ++ "-20"

in  { groups =
      [ generateGroup 1, generateGroup 2, generateGroup 3, generateGroup 4
      , generateGroup 5, generateGroup 6, generateGroup 7, generateGroup 8
      , generateGroup 9, generateGroup 10, generateGroup 11, generateGroup 12
      , generateGroup 13, generateGroup 14, generateGroup 15, generateGroup 16
      , generateGroup 17, generateGroup 18, generateGroup 19, generateGroup 20
      , generateGroup 21, generateGroup 22, generateGroup 23, generateGroup 24
      ]
    , students =
      [ { age = 19, group = "ИКБО-4-20", name = "Иванов И.И." }
      , { age = 18, group = "ИКБО-5-20", name = "Петров П.П." }
      , { age = 18, group = "ИКБО-5-20", name = "Сидоров С.С." }
      , { age = 20, group = "ИКБО-6-20", name = "Кузнецов К.К." } -- новый студент
      ]
    , subject = "Конфигурационное управление"
 }
```

### Задача 3
Язык нулей и единиц.

10
100
11
101101
000

```bash
BNF = '''
E = 10 | 100 | 11 | 101101 | 000
'''

for i in range(10):
    print(generate_phrase(parse_bnf(BNF), 'E'))
```

### Задача 4
Язык правильно расставленных скобок двух видов.

(({((()))}))
{}
{()}
()
{}

```bash
BNF = '''
E = "()" | "{}" | E E | "(" E ")" | "{" E "}"
'''

for i in range(10):
    print(generate_phrase(parse_bnf(BNF), 'E'))
```

Задача 5
Язык выражений алгебры логики.
```bash
BNF = '''
E = "~" E | E "&" E | E "|" E | "(" E ")" | "x" | "y"
'''

for i in range(10):
    print(generate_phrase(parse_bnf(BNF), 'E'))
```