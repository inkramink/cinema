import datetime
from data import db_session
from data.films import Films
from random import choice
import sqlite3

con = sqlite3.connect('db/cinema.db')
cur = con.cursor()
result = cur.execute("""SELECT * FROM films""").fetchall()
names = {}
for i in result:
    names[i[1]] = 0
times = [int(i[2]) + 10 for i in result]


def xxx():
    f = open("static/schedule.txt", 'w')
    f.write(str(datetime.datetime.now().date()) + '\n')
    sredn = sum(times) // len(times)
    day = (25 - 8) * 60
    films_on_day = (halls * day) / sredn
    for i in range(halls):
        rasp_of_halls[i] = {}
        if (films_on_day / halls > films_on_day // halls):
            u = films_on_day // halls + 1
        else:
            u = films_on_day // halls
        time = 8 * 60
        for j in range(int(u)):
            x = list(names.keys()).index(choice(list(names.keys())))
            while names[list(names.keys())[x]] > films_on_day // len(names):
                if names[list(names.keys())[x]] - films_on_day // len(names) == 1:
                    break
                x = list(names.keys()).index(choice(list(names.keys())))
            rasp_of_halls[i][f'{time // 60}:{f"{time % 60}0" if len(list(str(time % 60))) < 2 else time % 60}'] = \
                list(names.keys())[x]
            time += times[x]
            names[list(names.keys())[x]] += 1
        f.write(f"{i}: {str(rasp_of_halls[i])}\n")


halls = 5
rasp_of_halls = {}


def do():
    try:
        f = open("static/schedule.txt", encoding='windows-1251').read()
        x = f[:10]
        y = str(datetime.datetime.now().date())
        assert x == y
    except FileNotFoundError:
        xxx()
    except AssertionError:
        xxx()


def remake_shedule():
    do()
    sessions_for_films = {}
    n = 0
    f = open("static/schedule.txt", encoding='windows-1251').read()
    for i in names.keys():
        sessions_for_films[i] = []
        for j in range(f.count(i)):
            x = f.find(i)
            y = f[:x].rfind('{')
            y = f[y - 3:y - 2]
            try:
                l = int(f[x - 9:x - 7])
                time = f[x - 9: x - 4]
            except ValueError:
                time = f[x - 8: x - 4]
            sessions_for_films[i].append([time, int(y), n])
            n += 1
            f = f[:x] + f[x:x + len(list(i))].upper() + f[x + len(list(i)):]
        sessions_for_films[i] = sorted([i for i in sessions_for_films[i]],
                                       key=lambda m: int(m[0].split(':')[0]) * 60 + int(m[0].split(':')[1]))
    return sessions_for_films
