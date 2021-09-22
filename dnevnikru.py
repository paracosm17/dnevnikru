from  datetime import *
import enum
import fake_useragent
import requests
from bs4 import BeautifulSoup


class constants(enum.Enum):
    datefrom = date.today().strftime("%d.%m.%Y")
    dateto = (date.today() + timedelta(days=10)).strftime("%d.%m.%Y")
    studyYear = date.today().year
    choose = '%D0%9F%D0%BE%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D1%8C'
    group = 'all'




