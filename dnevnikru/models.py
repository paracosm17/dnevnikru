from datetime import datetime
from datetime import timedelta
from typing import Optional, List, Union

from pydantic import BaseModel, validator, conint

from dnevnikru.exceptions import DnevnikError
from dnevnikru.consts import PEOPLE_GROUPS, BIRTHDAYS_GROUPS


class LoginData(BaseModel):
    login: str
    password: str
    region: Optional[str]


class UserData(LoginData):
    school: int


class HomeworkArgsModel(BaseModel):
    days: int
    datefrom: str
    dateto: str
    studyyear: Optional[int] = None

    @validator('datefrom', 'dateto', pre=True, always=True)
    def validate_date(cls, v: str):
        try:
            date = datetime.strptime(v, '%d.%m.%Y')
        except ValueError as e:
            raise DnevnikError('Error. Date must ba dd.mm.YYYY format', 'DateFormatError')
        else:
            return v

    @validator('dateto', pre=True, always=True)
    def validate_days(cls, v: str, values, **kwargs):
        datefrom = datetime.strptime(values['datefrom'], '%d.%m.%Y')
        dateto = datetime.strptime(v, '%d.%m.%Y')
        difference = dateto - datefrom
        if difference.days < 0:
            raise DnevnikError('dateto не может быть меньше datefrom', 'DateError')
        if values['days'] != 10:
            datefrom = datetime.strptime(values['datefrom'], '%d.%m.%Y')
            v = (datefrom + timedelta(days=values['days'])).strftime("%d.%m.%Y")
        return v

    @validator('studyyear', pre=True, always=True)
    def validate_studyyear(cls, v: int, values, **kwargs):
        datefrom = datetime.strptime(values['datefrom'], '%d.%m.%Y')
        month = datefrom.month
        v = datefrom.year if month > 8 else datefrom.year - 1
        return v


class HomeWorkModel(BaseModel):
    subject: str
    work: str
    date: str


class HomeWorkListModel(BaseModel):
    homework: List[HomeWorkModel]


class MarksArgsModel(BaseModel):
    index: Union[str, int]
    period: Union[str, int]


class MarksModel(BaseModel):
    id: int
    subject: str
    marks: list
    lateness: int
    all_passes: int
    sick_passes: int
    average_mark: Optional[float]
    final_mark: Optional[int]

    @validator('average_mark', pre=True, always=True)
    def validate_average_mark(cls, v: str):
        if v == '':
            return None
        v = v.replace(',', '.')
        return float(v)

    @validator('final_mark', pre=True, always=True)
    def validate_final_mark(cls, v: str):
        if v == '':
            return None
        v = v.replace(',', '.')
        return int(v)


class MarksListModel(BaseModel):
    marks: List[MarksModel]


class SearchPeopleArgs(BaseModel):
    group: PEOPLE_GROUPS
    name: str
    grade: Union[str, int]

    @validator('grade', pre=True, always=True)
    def validate_grade(cls, v):
        if v == '':
            return v
        try:
            return int(v)
        except ValueError:
            raise DnevnikError('Grade must be "" or integer', 'Error')


class PeopleModel(BaseModel):
    name: str
    role: str


class PeopleListModel(BaseModel):
    people: List[PeopleModel]


class BirthdaysArgsModel(BaseModel):
    day: conint(ge=1, le=31)
    month: conint(ge=1, le=12)
    group: BIRTHDAYS_GROUPS

    @validator('month', pre=True, always=True)
    def validate_date(cls, v: int, values, **kwargs):
        months = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if months[v - 1] < values['day']:
            assert DnevnikError('Error date', 'Error')
        return v


class BirthdaysModel(BaseModel):
    name: str


class BirthdaysListModel(BaseModel):
    date: str
    birthdays: List[BirthdaysModel]
