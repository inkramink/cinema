class Sitting:
    def __init__(self, i, j):
        self.pos = (i, j)
        self.table = []


class MovieHall:
    def __init__(self, name, x, y):
        self.name = name
        self.sittings = [[0 for j in range(y)] for i in range(x)]
        self.table = []
        self.scedual = {}
    
    def init_sittings(self, col, row):
        self.sittings = [[Sitting(i, j) for j in range(col)] for i in range(row)]
    
    def change_len_sittings(self, row, new_col):
        self.sittings[row] = [Sitting(row, i) for i in range(new_col)]
    
    def add_film(self, film, time):
        self.scedual[time] = film


class Kino:
    def __init__(self, name):
        self.name = name
        self.movie_halls = {}
    
    def add_movie_hall(self, movie_hall_name, x, y):
        self.movie_halls[movie_hall_name] = MovieHall(movie_hall_name, x, y)
    
    def add_film(self, time, film, hall):
        self.movie_halls[hall].add_film(film, time)


class Owner:
    def __init__(self):
        self.kinos = {}
    
    def add_kino(self, name):
        self.kinos[name] = Kino(name)
    
    def add_hall(self, kino_name, hall_name, h_x, h_y):
        self.kinos[kino_name].add_movie_hall(hall_name, h_x, h_y)
    
    def add_film(self, film, kino, hall, time):
        self.kinos[kino].add_film(time, film, hall)


class Film:
    def __init__(self, name, length):
        self.length = length
        self.name = name


def init_kino_system():
    print('Здравствуйте, это билетная система. Начнем с того, что зададим кинозалы и сеансы')
    
    while True:
        owner = Owner()
        films = {}
        print('Команды:')
        print('kino {имя кинотеатра} - добавить кинотеатр')
        print('hall {имя кинотеатра} {имя зала} {x} {y} -', end=' ')
        print('добавить кинозал с количеством рядом х и количеством рядов y')
        print('film {название фильма} {длительность} - создать фильм')
        print('seans {время} {кинозал} {кинотеатр} {фильм} - задать сеанс')
        print('finish - закончить планировать систему кинотеатров')
        
        inp = [i for i in input().split()]
        if inp[0] == 'kino':
            owner.add_kino(inp[1])
        elif inp[0] == 'hall':
            owner.add_hall(inp[1], inp[2], inp[3], inp[4])
        elif inp[0] == 'film':
            films[inp[1]] = Film(inp[1], inp[2])
        elif inp[0] == 'seans':
            owner.add_film(films[inp[4]], inp[3], inp[2], inp[1])
        elif inp[0] == 'finish':
            break
        else:
            print('вы ввели что-то неправильно')


def main():
    init_kino_system()
