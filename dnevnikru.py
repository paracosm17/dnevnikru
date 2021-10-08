import enum
import fake_useragent
import requests
from datetime import date, timedelta, datetime
from bs4 import BeautifulSoup
import urllib.parse


class Defaults(enum.Enum):
    """
    Дефолтные значения для параметров и ссылок
    """
    dateFrom = date.today().strftime("%d.%m.%Y")
    dateTo = (date.today() + timedelta(days=10)).strftime("%d.%m.%Y")
    studyYear = date.today().strftime("%Y")
    day = date.today().day
    month = date.today().month
    choose = urllib.parse.quote("Показать")
    base_link = "https://schools.dnevnik.ru/"
    hw_link = "".join((base_link, "homework.aspx?school={}&tab=&studyYear={}&subject=&datefrom={}&dateto={}&choose=", choose))
    marks_link = "".join((base_link, "marks.aspx?school={}&index={}&tab=period&period={}&homebasededucation=False"))
    searchpeople_link = "".join((base_link, "school.aspx?school={}&view=members&group={}&filter=&search={}&class={}"))
    birthdays_link = "".join((base_link, "birthdays.aspx?school={}&view=calendar&action=day&day={}&month={}&group={}"))
    week_link = "https://dnevnik.ru/currentprogress/choose?userComeFromSelector=True"


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
        except Exception:
            return None

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
        return tuple(content)

    @staticmethod
    def get_week_response(session, school, weeks):
        link = Defaults.week_link.value
        data_response = session.get(link).text
        day = datetime.strptime(Defaults.dateFrom.value, "%d.%m.%Y") + timedelta(7 * weeks)
        weeks_list = []
        week = date(2021, 7, 19)
        for _ in range(35):
            week = week + timedelta(7)
            weeks_list.append(week.strftime("%d.%m.%Y"))
        for i in weeks_list:
            if day <= datetime.strptime(i, "%d.%m.%Y"):
                week = weeks_list[weeks_list.index(i) - 1]
                break
        soup = BeautifulSoup(data_response, 'lxml')
        user_id = soup.find('option')["value"]
        link = "https://dnevnik.ru/currentprogress/result/{}/{}/{}/{}?UserComeFromSelector=True".format(
            user_id, school, Defaults.studyYear.value, week)
        week_response = session.get(link).text
        return week_response


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
        self.main_session.post('https://login.dnevnik.ru/login', data={"login": self.login, "password": self.password})
        try:
            school = self.main_session.cookies['t0']
            self.school = school
        except Exception:
            raise DnevnikError('Неверный логин или пароль!', 'LoginError')

    def homework(self, datefrom=Defaults.dateFrom.value, dateto=Defaults.dateTo.value,
                 studyyear=Defaults.studyYear.value, days=10):
        """
        Возвращает список домашней работы
        Можно передать дату начала, дату конца
        Также можно передать на сколько дней вперед показать д/з
        :param datefrom:
        :param dateto:
        :param studyyear:
        :param days:
        :return:
        """
        if datefrom != Defaults.dateFrom.value or days != 10:
            dt = datetime.strptime(datefrom, '%d.%m.%Y')
            dateto = (dt + timedelta(days=days)).strftime("%d.%m.%Y")
        if len(datefrom) != 10 or len(dateto) != 10:
            raise DnevnikError("Неверно указаны dateto или datefrom", "Parameters error")
        if str(studyyear) not in datefrom:
            raise DnevnikError("StudyYear должен соответствовать datefrom", "Parameters error")

        link = Defaults.hw_link.value.format(self.school, studyyear, datefrom, dateto)
        homework_response = self.main_session.get(link, headers={"Referer": link}).text
        last_page = Utils.last_page(homework_response)

        if last_page is not None:
            subjects = []
            for page in range(1, int(last_page) + 1):
                homework_response = self.main_session.get(link + f"&page={page}", headers={"Referer": link}).text
                for i in Utils.save_content(homework_response, class2='grid gridLines vam hmw'):
                    subject = [i[2],
                               i[0].replace("\n\r\n" + " " * 24, "").replace("\r\n" + " " * 20 + "\n", ""),
                               i[3].replace("\n" * 2, "").replace("\xa0", " ").replace("\r\n" + " " * 8 + "\t" * 3, "").
                               replace("\r\n" + " " * 16 + "\r\n" + "\t" * 4 + " " * 4 + "\n", '')]
                    subjects.append(subject)
            return subjects
        if last_page is None:
            try:
                subjects = []
                for i in Utils.save_content(homework_response, class2='grid gridLines vam hmw'):
                    subject = [i[2],
                               i[0].replace("\n\r\n" + " " * 24, "").replace("\r\n" + " " * 20 + "\n", ""),
                               i[3].replace("\n" * 2, "").replace("\xa0", " ").replace("\r\n" + " " * 8 + "\t" * 3, "").
                               replace("\r\n" + " " * 16 + "\r\n" + "\t" * 4 + " " * 4 + "\n", '')]
                    subjects.append(subject)
                return subjects
            except Exception:
                return ["Домашних заданий не найдено!"]

    def marks(self, index="", period=""):
        """
        Возвращает список оценок (По умолчанию текущий период)
        Можно передать индекс (отвечает за учебный год)
        И период (Отвечает за семестр/четверть)
        :param index:
        :param period:
        :return:
        """
        link = Defaults.marks_link.value.format(self.school, index, period)
        marks_response = self.main_session.get(link, headers={"Referer": link}).text
        try:
            marks = Utils.save_content(response=marks_response, class2='grid gridLines vam marks')
            for mark in marks:
                mark[2] = mark[2].replace(" ", "")
            return marks
        except DnevnikError:
            raise DnevnikError("Какой-то из параметров введен неверно", "Parameters Error")

    def searchpeople(self, group="", name="", grade=""):
        """
        Возвращает список людей и их группы
        Можно передать имя (ФИО, ФИ), группу, класс
        :param group:
        :param name:
        :param grade:
        :return:
        """
        assert group in ['all', 'students', 'staff', 'director', 'management', 'teachers', 'administrators',
                         ""], "Неверная группа!"

        link = Defaults.searchpeople_link.value.format(self.school, group, name, grade)
        searchpeople_response = self.main_session.get(link).text
        last_page = Utils.last_page(searchpeople_response)

        if last_page is not None:
            members = []
            for page in range(1, int(last_page) + 1):
                members_response = self.main_session.get(link + f"&page={page}").text
                for content in Utils.save_content(members_response, class2='people grid'):
                    member = [content[1].split('\n')[1], content[1].split('\n')[2]]
                    members.append(member)
            return members
        if last_page is None:
            members = []
            try:
                for content in Utils.save_content(searchpeople_response, class2='people grid'):
                    member = [content[1].split('\n')[1], content[1].split('\n')[2]]
                    members.append(member)
                return members
            except Exception:
                return ["По этому запросу ничего не найдено"]

    def birthdays(self, day: int = Defaults.day.value, month: int = Defaults.month.value, group=""):
        """
        Возвращает список людей у кого в этот день день рождения
        По умолчанию текущая дата
        Можно передать день (int), месяц (int), группу
        :param day:
        :param month:
        :param group:
        :return:
        """
        assert group in ['all', 'students', 'staff', 'director', 'management', 'teachers', 'administrators',
                         ""], "Неверная группа!"
        assert day in list(range(1, 32)) or month not in list(range(1, 13)), "Неверный день или месяц!"

        link = Defaults.birthdays_link.value.format(self.school, day, month, group)
        birthdays_response = self.main_session.get(link).text
        last_page = Utils.last_page(birthdays_response)

        if last_page is not None:
            birthdays = []
            for page in range(1, int(last_page) + 1):
                birthdays_response = self.main_session.get(link + f"&page={page}").text
                for i in Utils.save_content(birthdays_response, class2='people grid'):
                    birthdays.append(i[1].split('\n')[1])
            return birthdays
        if last_page is None:
            birthdays = []
            if "в школе именинников нет" in birthdays_response:
                return [f"К сожалению, {day}.{month} среди этой группы в школе именинников нет."]
            else:
                for i in Utils.save_content(birthdays_response, class2='people grid'):
                    birthdays.append(i[1].split('\n')[1])
                return birthdays

    def week(self, info, weeks=0):
        """
        info - "themes", "attendance", "marks", "schedule", "homeworks"
        weeks - По умолчанию текущая неделя
        Если передать weeks, то можно увидеть следующие/предыдущие недели
        Для предыдущих используется отрицательное число
        :param info:
        :param weeks:
        :return:
        """

        assert info in ["themes", "attendance", "marks", "schedule", "homeworks"], \
            'info must be "themes" or "attendance" or "marks" or "schedule" or "homeworks"'
        head = "current-progress-{}".format(info)
        item = "current-progress-{}__item"
        item = item.format("list") if info != "schedule" else item.format("schedule")
        week_response = Utils.get_week_response(session=self.main_session,
                                                school=self.school, weeks=weeks)
        soup = BeautifulSoup(week_response, 'lxml')
        title = soup.findAll("h5", {"class": "h5 h5_bold"})[0].text
        h = soup.find_all("div", {"class": head})[0]
        all_li = h.findAll("li", {"class": item})
        week = [i.replace("\n", " ").strip(" ") for i in [i.text for i in all_li]]
        return [title] + week

