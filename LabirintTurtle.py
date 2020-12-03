import emoji
class LabirintTurtle:

    def __init__(self):
        self.map = []  # карта лабиринта
        self.work_map = []  # рабочая карта состоящая из чисел
        self.x = None  # координаты черепахи
        self.y = None

    def load_map(self, name):  # Загружаем карту
        file = open(name, 'r')  # Открываем файл на чтение
        lab = file.read().split('\n')  # Считываем файл и делаем сплит по символу конца строки
        file.close()  # закрываем файл

        self.x = lab.pop()  # Достаем из считанного массива координаты черепахи
        self.y = lab.pop()

        self.map = [list(line) for line in lab]  # преобразуем каждую считанную строку в массив

        self.work_map = [list(map(int, list(line.replace('*', '1').replace(' ', '0')))) for line in lab]  #на основе считанного массива строим массив из 0 и 1
    def check_map(self):
        if not self.check():  # проверяем валидность карты
            self.map = []  # сбрасываем параметры и выводим сообщение
            self.work_map = []
            self.x = None
            self.y = None
            print('Невалидная карта')

    def check(self):  # проверка валидности карты
        ext = 0  # количество выходов из лабиринта

        try:
            self.x = int(self.x)  # проверка валидности координат
            self.y = int(self.y)
        except ValueError:
            return False

        for line in self.map:  # проверка присутствия только символов "*" и " "
            for symbol in line:
                if not symbol in ['*', ' ']:
                    return False

            ext += int(line[0] == ' ') + int(line[-1] == ' ')  # проверка наличия боковых выходов

        ext += self.map[0].count(' ') + self.map[-1].count(' ')  # общее количество выходов
        if ext == 0:  # если выходов нет
            return False

        if self.map[self.x][self.y] != ' ':  # если координаты черепахи совпадают со стеной
            return False

        self.voln(self.x, self.y, 1)  # проверка наличия тупиков
        ex,ey = self.get_exit_coord()
        if self.work_map[ex][ey] == 0:
            return False

        return True

    def show_map(self, turtle=False):
        self.check()
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if turtle and i == self.x and j == self.y:
                    print('🐢', end=' ') # Черепаха
                elif i == 0 or j == 0 or i == len(self.map) - 1 or j == len(self.map[0]) - 1:
                    if self.map[i][j] == "*":
                        print('⬛', end=' ') # Ограда
                    else:
                        print('✅', end=' ') # Выход
                elif self.map[i][j] == ' ':
                    print('🟩', end=' ') # Пустое место
                else:
                    print('⬛', end=' ') # Стена внутри лабиринта
            print()

    def get_exit_coord(self):
        ext = []
        for i in range(len(self.map)):
            if self.map[i][0] == ' ':
                ext.append(i)
                ext.append(0)
                break
            elif self.map[i][-1] == ' ':
                ext.append(i)
                ext.append(len(self.map[i]) - 1)
                break
        if ' ' in self.map[0]:
            ext.append(0)
            ext.append(self.map[0].index(' '))
        elif ' ' in self.map[-1]:
            ext.append(len(self.map))
            ext.append(self.map[-1].index(' '))
        if len(ext) == 0:
            print("нет выхода")
            return
        m = 10000
        x = ext[0]
        y = ext[1]
        self.voln( self.x, self.y, 1 )
        for i in range(0, len(ext)-2, 2):
            if self.work_map[ext[i]][ext[i + 1]] < m:
                m = self.work_map[ext[i]][ext[i + 1]]
                x = ext[i]
                y = ext[i+1]
        return x, y

    def voln(self, x, y, cur=1):
        if not self.x:
            return
        self.work_map[x][y] = cur
        n = len(self.work_map)
        m = len(self.work_map[0])
        if y + 1 < m:
            if self.work_map[x][y + 1] == 0 or (self.work_map[x][y + 1] != -1 and self.work_map[x][y + 1] > cur):
                self.voln(x, y + 1, cur + 1)
        if x + 1 < n:
            if self.work_map[x + 1][y] == 0 or (self.work_map[x + 1][y] != -1 and self.work_map[x + 1][y] > cur):
                self.voln(x + 1, y, cur + 1)
        if x - 1 >= 0:
            if self.work_map[x - 1][y] == 0 or (self.work_map[x - 1][y] != -1 and self.work_map[x - 1][y] > cur):
                self.voln(x - 1, y, cur + 1)
        if y - 1 >= 0:
            if self.work_map[x][y - 1] == 0 or (self.work_map[x][y - 1] != -1 and self.work_map[x][y - 1] > cur):
                self.voln(x, y - 1, cur + 1)
        return self.work_map

    def exit_count_step(self):
        if not self.x:
            return

        self.check()
        ex, ey = self.get_exit_coord()
        print("\033[4m\033[36m\033[43m{}\033[0m".format(self.work_map[ex][ey] - 1))

    def get_path(self, long=False):
        if not self.x:
            return

        x, y = self.get_exit_coord()
        xm, ym = self.get_max_cell()

        path = [[x, y]]
        pathm = [[xm,ym]]

        while not [self.x, self.y] in path:
            if x > 0 and self.work_map[x - 1][y] == self.work_map[x][y] - 1 and self.map[x - 1][y] == ' ':
                path.append([x - 1, y])
                x = x - 1
            elif x < len(self.work_map) and self.work_map[x + 1][y] == self.work_map[x][y] - 1 and self.map[x + 1][
                y] == ' ':
                path.append([x + 1, y])
                x = x + 1
            elif y > 0 and self.work_map[x][y - 1] == self.work_map[x][y] - 1 and self.map[x][y - 1] == ' ':
                path.append([x, y - 1])
                y = y - 1
            elif y < len(self.work_map[0]) and self.work_map[x][y + 1] == self.work_map[x][y] - 1 and self.map[x][
                y + 1] == ' ':
                path.append([x, y + 1])
                y = y + 1
        while not [self.x, self.y] in pathm:

            if xm > 0 and self.work_map[xm - 1][ym] == self.work_map[xm][ym] - 1 and self.map[xm - 1][ym] == ' ':
                pathm.append([xm - 1, ym])
                xm = xm - 1
            elif xm < len(self.work_map) and self.work_map[xm + 1][ym] == self.work_map[xm][ym] - 1 and self.map[xm + 1][
                ym] == ' ':
                pathm.append([xm + 1, ym])
                xm = xm + 1
            elif ym > 0 and self.work_map[xm][ym - 1] == self.work_map[xm][ym] - 1 and self.map[xm][ym - 1] == ' ':
                pathm.append([xm, ym - 1])
                ym = ym - 1
            elif ym < len(self.work_map[0]) and self.work_map[xm][ym + 1] == self.work_map[xm][ym] - 1 and self.map[xm][
                ym + 1] == ' ':
                pathm.append([xm, ym + 1])
                ym = ym + 1

        if long:
            return pathm[:-1] + path
        else:
            return path

    def exit_show_step(self, long=False):
        if not self.x:
            return
        self.check()
        path = self.get_path(long=long)
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                # if i > 0 and j == 0 or j == len(self.map[0]):
                #     print(emoji.emojize("\033[32m{}\033[0m".format('|')))
                if i == self.x and j == self.y:
                    print(emoji.emojize(":turtle:"), end=' ')               # Черепаха
                elif [i, j] in path:
                    print("❇️", end=' ')  # Символ троектории ❇️
                elif self.map[i][j] == ' ':
                    print('🦋️', end=' ')  # Пустое место
                else:
                    print('🚷', end=' ')  # Стена
            print()

    def get_max_cell(self):
        x = y = None
        m = -1
        for i in range(len(self.work_map)):
            for j in range(len(self.work_map[0])):
                if self.work_map[i][j] > m:
                    m = self.work_map[i][j]
                    x, y = i, j
        return [x, y]

    def exit(self):
        a = "поверните налево"
        b = "поверните направо"
        c = "вперёд шаг"
        e = "развернитесь"
        d = 'u'
        self.check()
        path = list(reversed(self.get_path()))[1:]
        q = [self.x, self.y]
        for i in path:
            if i[1] > q[1] and i[0] == q[0]: # клетка справа
                if d == "u":
                    print(b)
                elif d == "d":
                    print(a)
                elif d == "l":
                    print(e)
                d = 'r'
            elif i[1] < q[1] and i[0] == q[0]:  # клетка слева
                if d == "u":
                    print(a)
                elif d == "d":
                    print(b)
                elif d == "r":
                    print(e)
                d = 'l'
            elif i[1] == q[1] and i[0] < q[0]:  # клетка слева
                if d == "l":
                    print(b)
                elif d == "d":
                    print(e)
                elif d == "r":
                    print(a)
                d = 'u'
            elif i[1] == q[1] and i[0] > q[0]:  # клетка слева
                if d == "l":
                    print(a)
                elif d == "u":
                    print(e)
                elif d == "r":
                    print(b)
                d = 'd'
            print(c)
            q = i

a = LabirintTurtle()
a.load_map('l200.txt')
# a.load_map('hard_test1.txt')
# a.show_map(turtle=True)
# print(*a.work_map,sep='\n')
# a.exit_count_step()
# a.check_map()
# print(*a.work_map, sep='\n')
# print(a.get_max_cell())
a.exit_show_step() # long = True
# print(a.get_path(long=True))
# a.exit()
