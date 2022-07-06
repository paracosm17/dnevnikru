from datetime import date, timedelta
import urllib.parse
from typing import Literal

DAY = date.today().day
MONTH = date.today().month
STUDYYEAR = date.today().strftime("%Y") if MONTH > 8 else int(date.today().strftime("%Y")) - 1
DATEFROM = date.today().strftime("%d.%m.%Y")
DATETO = (date.today() + timedelta(days=10)).strftime("%d.%m.%Y")
CHOOSE = urllib.parse.quote("Показать")
BASE_LINK = "https://schools.dnevnik.ru/"
HW_LINK = "".join(
    (BASE_LINK, "homework.aspx?school={}&tab=&studyYear={}&subject=&datefrom={}&dateto={}&choose=", CHOOSE))
MARKS_LINK = "".join((BASE_LINK, "marks.aspx?school={}&index={}&tab=period&period={}&homebasededucation=False"))
SEARCHPEOPLE_LINK = "".join((BASE_LINK, "school.aspx?school={}&view=members&group={}&filter=&search={}&class={}"))
BIRTHDAYS_LINK = "".join((BASE_LINK, "birthdays.aspx?school={}&view=calendar&action=day&day={}&month={}&group={}"))
WEEK_LINK = "https://dnevnik.ru/currentprogress/choose?userComeFromSelector=True"
USER_AGENT = {"User-Agent": "Mozilla/5.0 (Wayland; Linux x86_64) AppleWebKit/537.36 ("
                            "KHTML, like Gecko) Chrome/94.0.4606.72 Safari/537.36"}
PEOPLE_GROUPS = Literal['all', 'students', 'staff', 'director', 'management', 'teachers', 'administrators', '']
BIRTHDAYS_GROUPS = Literal['all', 'students', 'staff', 'class', '']
WEEK_INFORMATION = Literal['themes', 'attendance', 'marks', 'schedule', 'homeworks']
