# Normal forms

# Запуск
Запуск происходит из командной строки с помощью вызова main.py в папке проекта и возможно с несколькими аргументами, чтобы задать конкретную конфигурацию вывода ответа.

# Аргументы

```
usage: main.py [-h] [--nnf] [--cnf] [--dnf] [--verbose] input

positional arguments:
  input       Input expression. Important that there are only 3 logical operators in this order: unary NOT(-), binary AND(&), binary OR(|). 
              It is also possible to place brackets in your expression.

optional arguments:
  -h, --help  show this help message and exit
  --nnf       when checked outputs negative normal form
  --cnf       when checked outputs conjunctive normal form
  --dnf       when checked outputs disjunctive normal form
  --verbose   Show all info about input and all forms
```

# Пример запуска

```
$ main.py --verbose "a|-(-b&c|-d)"
I have received this expression:
a|-(-b&c|-d)
And there are chosen normal forms:

a|(b|-c)&d
t8&(-t8|a|t7)&(t8|-a)&(t8|-t7)&(t7|-t6|-d)&(-t7|t6)&(-t7|d)&(-t6|b|-c)&(t6|-b)&(t6|c)
a|(b&d)|(-c&d)

```

# Тесты.

На unit-тесты настроен CI. Однако юнит тесты можно также запустить из командной строки. Для этого должен быть установлен модуль pytest:
```
python -m pytest
```
