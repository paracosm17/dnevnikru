from dnevnikru import Dnevnik
from pprint import pprint

dn = Dnevnik(login="popov.aleksandr09050", password="qazwsxer12345")
pprint(dn.week_schedule())