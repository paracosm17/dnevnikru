from typing import Optional
from typing import Union

from dnevnikru import consts
from dnevnikru.authorization import auth
from dnevnikru.models import HomeworkArgsModel, HomeWorkModel, HomeWorkListModel, MarksArgsModel, MarksListModel, \
    MarksModel, SearchPeopleArgs, PeopleModel, PeopleListModel, BirthdaysArgsModel, BirthdaysModel, BirthdaysListModel
from dnevnikru.parsers import Parser


class Dnevnik:
    """""Базовый класс Дневника"""""

    def __init__(self, login: str, password: str, region: Optional[str] = None) -> None:
        self._main_session, self._user_data = auth(login, password, region)

    def homework(self, datefrom: str = consts.DATEFROM, dateto: str = consts.DATETO,
                 days: int = 10) -> dict:
        args = HomeworkArgsModel(datefrom=datefrom, dateto=dateto, days=days)
        link = consts.HW_LINK.format(self._user_data.school, args.studyyear, args.datefrom, args.dateto)
        homework_response = self._main_session.get(link, headers={"Referer": link}).text
        homework = Parser.get_homework(self, link=link, homework_response=homework_response)
        homework = HomeWorkListModel(homework=[HomeWorkModel(subject=i[0], work=i[1], date=i[2]) for i in homework])
        return homework.dict()

    def marks(self, index: Union[int, str] = '', period: Union[int, str] = '') -> dict:
        args_model = MarksArgsModel(index=index, period=period)
        link = consts.MARKS_LINK.format(self._user_data.school, args_model.index, args_model.period)
        marks_response = self._main_session.get(link, headers={"Referer": link}).text
        mark = Parser.get_marks(marks_response=marks_response)
        marks = []
        for i in mark:
            marks.append(MarksModel(
                id=i[0],
                subject=i[1],
                marks=list(i[2]),
                lateness=i[3],
                all_passes=i[4],
                sick_passes=i[5],
                average_mark=i[6],
                final_mark=i[7]
            ))
        return MarksListModel(marks=marks).dict()

    def searchpeople(self, group: str = '', name: str = '',
                     grade: Union[int, str] = '') -> dict:
        searchpeople_model = SearchPeopleArgs(group=group, name=name, grade=grade)
        link = consts.SEARCHPEOPLE_LINK.format(self._user_data.school, searchpeople_model.group,
                                                 searchpeople_model.name, searchpeople_model.grade)

        searchpeople_response = self._main_session.get(link).text
        people = Parser.search_people(self, link=link, searchpeople_response=searchpeople_response)
        people = PeopleListModel(people=[PeopleModel(name=i[0], role=i[1]) for i in people])

        return people.dict()

    def birthdays(self, day: int = consts.DAY, month: int = consts.MONTH, group: str = '') -> dict:
        birthdays_model = BirthdaysArgsModel(day=day, month=month, group=group)
        link = consts.BIRTHDAYS_LINK.format(self._user_data.school, birthdays_model.day, birthdays_model.month,
                                              birthdays_model.group)
        birthdays_response = self._main_session.get(link).text
        birthdays = Parser.get_birthdays(self, birthdays_response=birthdays_response, link=link)
        birthdays = BirthdaysListModel(date=f'{birthdays_model.day}.{birthdays_model.month}',
                                       birthdays=[BirthdaysModel(name=i) for i in birthdays])
        return birthdays.dict()

    def week(self, info: consts.WEEK_INFORMATION = 'schedule', weeks: int = 0) -> dict:
        return Parser.get_week(session=self._main_session, school=self._user_data.school, info=info, weeks=weeks)
