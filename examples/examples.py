# Больше примеров есть на странице Wiki - https://github.com/paracosm17/dnevnikru/wiki

from dnevnikru import Dnevnik
from pprint import pprint

login = "Your login"
password = "Your password"
dairy = Dnevnik(login=login,
                password=password)

pprint(dairy.week(info="themes"), sort_dicts=False)  # Вывести список пройденных тем за текущую неделю

total = 0  # Счётчик пропусков
for subject in dairy.marks():  # Проходимся циклом по всем предметам в журнале оценок
    total += int(subject[4])   # Суммируем количество пропусков с каждого предмета

print(total)
