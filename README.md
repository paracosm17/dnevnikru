[![PyPI](https://img.shields.io/pypi/v/dnevnikru)](https://pypi.org/project/dnevnikru/)
[![Python Versions](https://img.shields.io/pypi/pyversions/dnevnikru)](https://pypi.org/project/dnevnikru)
# dnevnikru

> Module for working with the site dnevnik.ru with python

Dnevnik object accepts login and password from the dnevnik.ru account <br/>
Methods: homework, marks, searchpeople, birthdays, week <br>
##### Read the full functionality of the module here: [Wiki][wiki] <br>
(Doesn't work in regions where you can enter the Diary only through GosUslugi !)
## Installation

Windows:

Run the command in the terminal: <br>
```cmd
pip install dnevnikru
```

## Examples of use

```python
from dnevnikru import Dnevnik

dairy = Dnevnik(login='Your login', password='Your password')

homework = dairy.homework(studyyear=2020, datefrom='01.12.2020', dateto='30.12.2020')
marks = dairy.marks(index=0, period=1)
class_11b = dairy.searchpeople(grade='11B')
birthdays = dairy.birthdays(day=9, month=5)
schedule = dairy.week(info="schedule", weeks=-1)
```

#### _For more examples of uses and parameters in methods, see [Wiki][wiki]._

## Requires

The module requires `requests`, `lxml`, `bs4` libraries

## Releases

* 1.0

## Contact

Aleksandr – tg: [@paracosm17](https://t.me/paracosm17) – email: paracosm17@aol.com <br>

## LICENSE
Distributed under the Apache License 2.0 license. See ``LICENSE`` for more information.

<!-- Markdown link & img dfn's -->
[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/paracosm17/dnevnikru/wiki
