# dnevnikru
> Модуль для работы с сайтом dnevnik.ru на python

Объект dnevnik принимает в себя login и password от аккаунта в дневнике <br/>
Методы: homework, marks, searchpeople, birthdays

## Установка

Windows:

Поместите файл ```dnevnikrupy.py``` в папку с вашим проектом
```
import dnevnikrupy
```

## Примеры использования

```
import dnevnikrupy

dn = dnevnik(login='Your login', password='Your password')

homework = dn.homework(studyYear=2020, datefrom='01.12.2020', dateto='30.12.2020')
marks = dn.marks(index=0, period=1)
11_b = dn.searchpeople(klass='11Б')
birthdays = dn.birthdays(day='01', month='09')
```

_Ещё больше примеров использования на странице [Wiki][wiki]._

## Зависимости

Для работы модуля понадобятся библеотеки
requests,
fake-useragent,
lxml,
bs4

```
pip install -r requirements.txt
```

## Релизы

* 0.0.1
    * Первая версия проекта


## Связь

Alexandr – [@paracosm17](https://t.me/paracosm17) – paracosm17@yandex.ru

Distributed under the Apache License 2.0 license. See ``LICENSE`` for more information.


<!-- Markdown link & img dfn's -->
[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/paracosm17/dnevnikrupy/wiki
