from dnevnikru import settings
from dnevnikru.exceptions import DnevnikError

from bs4 import BeautifulSoup
from typing import Optional, Union
from datetime import date, timedelta, datetime


class Parser:
    @staticmethod
    def last_page(response: str) -> Optional[int]:
        """Функция для получения номера последней страницы (если она есть)"""
        try:
            soup = BeautifulSoup(response, 'lxml')
            all_pages = soup.find('div', {'class': 'pager'})
            pages = all_pages.find_all('li')
            last_page = pages[-1].text
            return last_page
        except AttributeError:
            return None

    @staticmethod
    def save_content(response: str, class2: str, map2 = {}) -> tuple:
        """
        Функция для парсинга и сохранения таблиц с сайта
        map2: необязательный фильтр на колонки вида {1:(), 2:('tag'), 3:('tag', 'attr')}
        """
        soup = BeautifulSoup(response, 'lxml')
        table = soup.find('table', {'class': class2})
        content = []
        the_text = ''
        all_rows = table.findAll('tr')
        for row in all_rows:
            content.append([])
            all_cols = row.findAll('td')
            for (col_i, col) in enumerate(all_cols):
                if len(map2) == 0:
                    the_strings = [str(s) for s in col.findAll(text=True)]
                    the_text = ''.join(the_strings)
                    content[-1].append(the_text)
                else:
                    if col_i in map2:
                        if len(map2[col_i]) == 0:
                            the_strings = [str(s) for s in col.findAll(text=True)]
                            the_text = ''.join(the_strings)
                            content[-1].append(the_text)
                        else:
                            the_text = tuple((s.text, s.attrs[map2[col_i][1]] if len(map2[col_i]) > 1 else '') for s in col.findAll(map2[col_i][0]))
                            content[-1].append(the_text)
        content = [a for a in content if a != []]
        return tuple(content)

    @staticmethod
    def get_week_response(session, school: Union[int, str], weeks: int) -> str:
        """Функция для получения html страницы с результатами недели"""
        link = settings.WEEK_LINK
        data_response = session.get(link).text
        day = datetime.strptime(settings.DATEFROM, "%d.%m.%Y") + timedelta(7 * weeks)
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
            user_id, school, settings.STUDYYEAR, week)
        week_response = session.get(link).text
        return week_response

    @staticmethod
    def get_homework(self, link: str, last_page: Union[str, int], homework_response: str) -> dict:
        """Функция для получения домашних заданий"""
        if last_page is not None:
            subjects = []
            for page in range(1, int(last_page) + 1):
                homework_response = self._main_session.get(link + f"&page={page}", headers={"Referer": link}).text
                for i in Parser.save_content(homework_response, class2='grid gridLines vam hmw'):
                    subject = [i[2], i[0].strip(),
                               " ".join([_.strip() for _ in i[3].split()])]
                    subjects.append(tuple(subject))
            return {"homeworkCount": len(subjects), "homework": tuple(subjects)}
        if last_page is None:
            try:
                subjects = []
                for i in Parser.save_content(homework_response, class2='grid gridLines vam hmw'):
                    subject = [i[2], i[0].strip(),
                               " ".join([_.strip() for _ in i[3].split()])]
                    subjects.append(tuple(subject))
                return {"homeworkCount": len(subjects), "homework": tuple(subjects)}
            except Exception as e:
                raise DnevnikError(e, "DnevnikError")

    @staticmethod
    def get_marks(marks_response: str) -> tuple:
        """Функция для получения оценок"""
        try:
            marks = Parser.save_content(response=marks_response, class2='grid gridLines vam marks', map2={0:(),1:(),2:('span', 'title'),6:()})
            return tuple(marks)
        except Exception as e:
            raise DnevnikError(e, "DnevnikError")

    @staticmethod
    def search_people(self, last_page: Union[int, str], link: str, searchpeople_response: str) -> dict:
        """Функция для поиска людей по школе"""
        if last_page is not None:
            members = []
            for page in range(1, int(last_page) + 1):
                members_response = self._main_session.get(link + f"&page={page}").text
                for content in Parser.save_content(members_response, class2='people grid'):
                    member = [content[1].split('\n')[1], content[1].split('\n')[2]]
                    members.append(tuple(member))
            return {"peopleCount": len(members), "people": tuple(members)}
        if last_page is None:
            members = []
            try:
                for content in Parser.save_content(searchpeople_response, class2='people grid'):
                    member = [content[1].split('\n')[1], content[1].split('\n')[2]]
                    members.append(tuple(member))
                return {"peopleCount": len(members), "people": tuple(members)}
            except Exception as e:
                raise DnevnikError(e, "DnevnikError")

    @staticmethod
    def get_birthdays(self, birthdays_response: str, link: str) -> dict:
        """Функция для поиска дней рождений по школе"""
        if "в школе именинников нет." in birthdays_response:
            return {"peopleCount": 0, "people": ()}
        last_page = Parser.last_page(birthdays_response)

        if last_page is not None:
            birthdays = []
            for page in range(1, int(last_page) + 1):
                birthdays_response = self._main_session.get(link + f"&page={page}").text
                for i in Parser.save_content(birthdays_response, class2='people grid'):
                    birthdays.append(i[1].split('\n')[1])
            return {"birthdaysCount": len(birthdays), "birthdays": tuple(birthdays)}
        if last_page is None:
            birthdays = []
            try:
                for i in Parser.save_content(birthdays_response, class2='people grid'):
                    birthdays.append(i[1].split('\n')[1])
                return {"birthdaysCount": len(birthdays), "birthdays": tuple(birthdays)}
            except Exception as e:
                raise DnevnikError(e, "DnevnikError")

    @staticmethod
    def get_week(self, info: str, weeks: int) -> dict:
        """Функция для получения результатов недели"""
        head = "current-progress-{}".format(info)
        item = "current-progress-{}__item"
        item = item.format("list") if info != "schedule" else item.format("schedule")
        week_response = Parser.get_week_response(session=self._main_session,
                                                 school=self._school, weeks=weeks)
        week = {}
        soup = BeautifulSoup(week_response, 'lxml')
        student = soup.findAll("h5", {"class": "h5 h5_bold"})[0].text
        h = soup.find_all("div", {"class": head})[0]
        all_li = h.findAll("li", {"class": item})
        if info == "schedule":
            for li in all_li:
                day = li.find("div").text
                schedule = li.findAll("li")
                schedule = [x.text for x in schedule]
                week.update({day: tuple(schedule)})
            return {"student": student, "schedule": week}
        else:
            week = [i.replace("\n", " ").strip(" ") for i in [i.text for i in all_li]]
            return {"student": student, info: tuple(week)}
