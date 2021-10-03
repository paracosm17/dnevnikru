# dnevnikru

> Модуль для работы с сайтом dnevnik.ru на python

Объект dnevnik принимает в себя login и password от аккаунта в дневнике <br/>
Методы: homework, marks, searchpeople, birthdays

## Установка

Windows:

Поместите файл ```dnevnikru.py``` в папку с вашим проектом

```python
import dnevnikru
```

## Примеры использования

```python
from dnevnikru import Dnevnik

dn = Dnevnik(login='Your login', password='Your password')

homework = dn.homework(studyyear=2020, datefrom='01.12.2020', dateto='30.12.2020')
marks = dn.marks(index=0, period=1)
class_11b = dn.searchpeople(grade='11Б')
birthdays = dn.birthdays(day=9, month=5)
shedule_next_week = dn.week_schedule(weeks=1)
```

_Ещё больше примеров использования на странице [Wiki][wiki]._

## Зависимости

Для работы модуля понадобятся библиотеки `requests`, `fake-useragent`, `lxml`, `bs4`

```cmd
pip install -r requirements.txt
```

Или используя менеджер [Pipenv](https://github.com/pypa/pipenv)

Если не установлен pipenv, выполнить

```cmd
python -m pip install pipenv
```

Создать виртуальное окружение в директории с проектом

```cmd
pipenv shell
```

Установить все требуемые библиотеки из Pipfile

```cmd
pipenv install --ignore-pipfile
```

## Релизы

* 0.0.1
  * Первая версия проекта

## Связь

Alexandr – [@paracosm17](https://t.me/paracosm17) – paracosm17@yandex.ru <br>
<br>
Contributors: <br>
<br>
<a href="https://github.com/stepanskryabin"><img src="https://avatars.githubusercontent.com/u/47498917?v=4" /></a>

Distributed under the Apache License 2.0 license. See ``LICENSE`` for more information.

<!-- Markdown link & img dfn's -->
[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/paracosm17/dnevnikru/wiki
