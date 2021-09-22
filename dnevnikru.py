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


class Exception_dnevnik(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = f'DnevnikException[{errors}]'


class utils:
    @staticmethod
    def last_page(response):
        soup = BeautifulSoup(response, 'lxml')
        all_pages = soup.find('div', {'class': 'pager'})
        pages = all_pages.find_all('li')
        last_page = pages[-1].text
        return last_page

    @staticmethod
    def save_content(response, class2):
        soup = BeautifulSoup(response, 'lxml')
        table = soup.find('table', {'class': class2})
        content = []
        allrows = table.findAll('tr')
        for row in allrows:
            content.append([])
            allcols = row.findAll('td')
            for col in allcols:
                thestrings = [str(s) for s in col.findAll(text=True)]
                thetext = ''.join(thestrings)
                content[-1].append(thetext)
        content = [a for a in content if a != []]
        return content


class Dnevnik:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.main_session = requests.Session()
        self.main_session.cookies.update({"User-Agent": fake_useragent.UserAgent().random})
        self.main_session.post(f'https://login.dnevnik.ru/login', {"login": self.login, "password": self.password})
        try:
            school = self.main_session.cookies['t0']
            self.school = school
        except:
            raise Exception_dnevnik('Invalid login data or wrong auth method', 'LoginError')




