from dnevnikru.exceptions import DnevnikError
from dnevnikru.parsers import Parser
from dnevnikru import settings

from datetime import timedelta, datetime
from typing import Union
import requests


class Dnevnik:
    """Базовый класс Дневника"""

    def __init__(self, login: str, password: str) -> None:
        self.__login, self.__password = login, password
        self._main_session = requests.Session()
        self._main_session.headers.update(settings.USER_AGENT)
        self._main_session.post('https://login.dnevnik.ru/login',
                                data={"login": self.__login, "password": self.__password})
        if self._main_session.cookies.get("t0"):
            self._school = self._main_session.cookies.get("t0")
            return
        raise DnevnikError('Authorization error', 'LoginError')

    def homework(self, datefrom=settings.DATEFROM, dateto=settings.DATETO, studyyear=settings.STUDYYEAR,
                 days: int = 10) -> dict:
        """Method for getting homework"""
        # Checking the correctness of arguments
        if datefrom != settings.DATEFROM or days != 10:
            days_count = datetime.strptime(datefrom, '%d.%m.%Y')
            dateto = (days_count + timedelta(days=days)).strftime("%d.%m.%Y")
        if len(datefrom) != 10 or len(dateto) != 10:
            raise DnevnikError("Invalid dateto or datefrom", "Arguments error")
        if str(studyyear) not in datefrom:
            raise DnevnikError("StudyYear must match datefrom", "Arguments error")

        # Get homework
        link = settings.HW_LINK.format(self._school, studyyear, datefrom, dateto)
        homework_response = self._main_session.get(link, headers={"Referer": link}).text
        if "Домашних заданий не найдено." in homework_response:
            return {"homeworkCount": 0, "homework": ()}
        last_page = Parser.last_page(homework_response)
        return Parser.get_homework(self, link=link, last_page=last_page, homework_response=homework_response)

    def marks(self, index: Union[str, int] = "", period: Union[str, int] = "") -> tuple:
        """Method for getting marks"""
        # Get marks
        link = settings.MARKS_LINK.format(self._school, index, str(period))
        marks_response = self._main_session.get(link, headers={"Referer": link}).text
        return Parser.get_marks(marks_response=marks_response)

    def searchpeople(self, group: str = "", name: str = "", grade: Union[str, int] = "") -> dict:
        """Method for getting people from user's school"""
        # Checking the correctness of arguments
        assert group in settings.PEOPLE_GROUPS, "Неверная группа!"

        # Get people
        link = settings.SEARCHPEOPLE_LINK.format(self._school, group, name, str(grade))
        searchpeople_response = self._main_session.get(link).text
        if "Никого не найдено. Измените условия поиска." in searchpeople_response:
            return {"peopleCount": 0, "people": ()}
        last_page = Parser.last_page(searchpeople_response)
        return Parser.search_people(self, last_page=last_page, link=link, searchpeople_response=searchpeople_response)

    def birthdays(self, day: int = settings.DAY, month: int = settings.MONTH, group: str = "") -> dict:
        """Method for getting birthdays"""
        # Checking the correctness of arguments
        assert group in settings.BIRTHDAYS_GROUPS, "Неверная группа!"
        assert day in list(range(1, 32)) or month not in list(range(1, 13)), "Неверный день или месяц!"

        # Get birthdays
        link = settings.BIRTHDAYS_LINK.format(self._school, day, month, group)
        birthdays_response = self._main_session.get(link).text
        return Parser.get_birthdays(self, birthdays_response=birthdays_response, link=link)

    def week(self, info: str = "schedule", weeks: int = 0) -> dict:
        """Method for getting week"""
        # Checking the correctness of arguments
        assert info in settings.WEEK_INFORMATION, 'Invalid info'

        # get week
        return Parser.get_week(self, info=info, weeks=weeks)
