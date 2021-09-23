from  datetime import *
import enum
import fake_useragent
import requests
from bs4 import BeautifulSoup


class Defaults(enum.Enum):
    """
    Дефолтные значения для параметров
    """
    dateFrom = date.today().strftime("%d.%m.%Y")
    dateTo = (date.today() + timedelta(days=10)).strftime("%d.%m.%Y")
    studyYear = date.today().strftime("%Y")
    choose = '%D0%9F%D0%BE%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D1%8C'
    group = 'all'
    base_link = "https://schools.dnevnik.ru/"
    hw_link = base_link + "homework.aspx?school={}&tab=&studyYear={}&subject=&datefrom={}&dateto={}&choose=" + choose


class DnevnikError(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = f'DnevnikException[{errors}]'


class Utils:
    @staticmethod
    def last_page(response):
        try:
            soup = BeautifulSoup(response, 'lxml')
            all_pages = soup.find('div', {'class': 'pager'})
            pages = all_pages.find_all('li')
            last_page = pages[-1].text
            return last_page
        except DnevnikError:
            last_page = None
            return last_page

    @staticmethod
    def save_content(response, class2):
        soup = BeautifulSoup(response, 'lxml')
        table = soup.find('table', {'class': class2})
        content = []
        all_rows = table.findAll('tr')
        for row in all_rows:
            content.append([])
            all_cols = row.findAll('td')
            for col in all_cols:
                the_strings = [str(s) for s in col.findAll(text=True)]
                the_text = ''.join(the_strings)
                content[-1].append(the_text)
        content = [a for a in content if a != []]
        return content


class Dnevnik:
    def __init__(self, login, password):
        """
        Принимает логин и пароль юзера от Дневника.ру
        :param login:
        :param password:
        """
        self.login, self.password = login, password
        self.main_session = requests.Session()
        self.main_session.cookies.update({"User-Agent": fake_useragent.UserAgent().random})
        self.main_session.post(f'https://login.dnevnik.ru/login', {"login": self.login, "password": self.password})
        try:
            school = self.main_session.cookies['t0']
            self.school = school
        except DnevnikError:
            raise DnevnikError('Invalid login data or wrong auth method', 'LoginError')

    def homework(self, datefrom=Defaults.dateFrom.value, dateto=Defaults.dateTo.value, studyyear=Defaults.studyYear.value):
        if len(datefrom) != 10 or len(dateto) != 10:
            raise DnevnikError("Incorrect dateto or datefrom", "Parameters error")
        if str(studyyear) not in datefrom or str(studyyear) not in dateto:
            raise DnevnikError("StudyYear must be in dateto or in datefrom", "Parameters error")

        link = Defaults.hw_link.value.format(self.school, studyyear, datefrom, dateto)
        homework_response = self.main_session.get(link, headers={"Referer": link}).text
        last_page = Utils.last_page(homework_response)

        if last_page is not None:
            subjects = []
            for page in range(1, int(last_page) + 1):
                homework_response = self.main_session.get(link+f"&page={page}", headers={"Referer": link}).text
                for i in Utils.save_content(homework_response, class2='grid gridLines vam hmw'):
                    subject = [i[2],
                               i[0].replace('\n\r\n                        ', '').replace(
                                   '\r\n                    \n', ''),
                               i[3].replace('\n\n', '').replace('\xa0', ' ').replace('\r\n        \t\t\t ', '').replace(
                                   '\r\n                \r\n\t\t\t\t    \n', '')]
                    subjects.append(subject)
            return subjects
        if last_page is None:
            try:
                subjects = []
                for i in Utils.save_content(homework_response, class2='grid gridLines vam hmw'):
                    subject = [i[2],
                               i[0].replace('\n\r\n                        ', '').replace(
                                   '\r\n                    \n', ''),
                               i[3].replace('\n\n', '').replace('\xa0', ' ').replace('\r\n        \t\t\t ', '').replace(
                                   '\r\n                \r\n\t\t\t\t    \n', '')]
                    subjects.append(subject)
                return subjects
            except DnevnikError:
                return "Домашних заданий не найдено!"









