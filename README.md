[![PyPI](https://img.shields.io/pypi/v/dnevnikru)](https://pypi.org/project/dnevnikru/)
[![Python Versions](https://img.shields.io/pypi/pyversions/dnevnikru)](https://pypi.org/project/dnevnikru)
# dnevnikru

> Модуль для работы с сайтом dnevnik.ru на python

Объект Dnevnik принимает в себя login и password от аккаунта в дневнике <br/>
Методы: homework, marks, searchpeople, birthdays, week <br>
##### Ознакомиться с полным функционалом модуля можно тут: [Wiki][wiki] <br>
(Не работает в регионах, где вход в Дневник осуществляется только через ГосУслуги!)
## Установка

Windows:

Выполните в терминале команду: <br>
```cmd
pip install dnevnikru
```

## Примеры использования

```python
from dnevnikru import Dnevnik

dairy = Dnevnik(login='Your login', password='Your password')

homework = dairy.homework(studyyear=2020, datefrom='01.12.2020', dateto='30.12.2020')
marks = dairy.marks(index=0, period=1)
class_11b = dairy.searchpeople(grade='11Б')
birthdays = dairy.birthdays(day=9, month=5)
schedule = dairy.week(info="schedule", weeks=-1)
```

#### _Ещё больше примеров использования и параметров в методах смотрите на странице [Wiki][wiki]._

## Зависимости

Для работы модуля понадобятся библиотеки `requests`, `lxml`, `bs4`

## Релизы

* 1.0
  * Первая версия проекта

## Связь

Aleksandr – tg: [@paracosm17](https://t.me/paracosm17) – email: paracosm17@yandex.ru <br>

## LICENSE
Distributed under the Apache License 2.0 license. See ``LICENSE`` for more information.

<!-- Markdown link & img dfn's -->
[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/paracosm17/dnevnikru/wiki
