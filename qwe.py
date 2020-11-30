import emoji

class LabirintTurtle:
    def __init__(self):
        self.map = []  # карта лабиринта
        self.work_map = []  # рабочая карта состоящая из чисел
        self.m2 = list()
        self.x = None  # координаты черепахи
        self.y = None

    def load_map(self, name):
        file = open(name, 'r')
        lab = file.read().split('\n')
        file.close()

        self.x = lab.pop()
        self.y = lab.pop()

        self.map = [list(line) for line in lab]     # преобразуем каждую считанную строку в массив
        # for i in self.map:            # * меняются на стены
        #     p = 0
        #     for u in i:
        #         if u == "*":
        #             self.map[self.map.index(i)][p] = '\N{Ladder}'
        #         p += 1
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
        except:
            return False

        for line in self.map:  # проверка присутствия только символов "*" и " "
            for symbol in line:
                # if not symbol in ['\N{Ladder}', ' ']:
                if not symbol in ['*', ' ']:
                    return False

            ext += int(line[0] == ' ') + int(line[-1] == ' ')  # проверка наличия боковых выходов

        ext += self.map[0].count(' ') + self.map[-1].count(' ')  # общее количество выходов
        if ext != 1:  # если выходов нет или их больше 1
            return False

        if self.map[self.x][self.y] != ' ':  # если координаты черепахи совпадают со стеной
            return False

        self.voln(self.x, self.y, 1)  # проверка наличия тупиков
        if self.get_exit_coord():
            ex = self.get_exit_coord()[0]
            ey = self.get_exit_coord()[1]
        else:
            return False
        if self.work_map[ex][ey] == 0:
            return False

        return True

    def show_map(self, turtle=None):
        if self.x == None:
            return
        for i in self.map:
            self.m2.append(list(i))
        self.m2[int(self.y)][int(self.x)] = "A"
        if turtle:
            for i in self.m2:
                print(*i, end='\n', sep='\t')
        else:
            for i in self.map:
                print(*i)
    def get_exit_coord(self):
        ext = []
        for i in range(len( self.map )):
            if self.map[i][0] == ' ':
                ext.append( i)
                ext.append( 0 )
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
        return ext

    def voln(self, x, y, cur=1):
        if not self.x:
            return
        print( self.work_map[x][y] )
        self.work_map[x][y] = cur
        n = len( self.work_map )
        m = len( self.work_map[0] )
        if y + 1 < m:
            if self.work_map[x][y + 1] == 0 or (self.work_map[x][y + 1] != -1 and self.work_map[x][y + 1] > cur):
                self.voln( x, y + 1, cur + 1 )
        if x + 1 < n:
            if self.work_map[x + 1][y] == 0 or (self.work_map[x + 1][y] != -1 and self.work_map[x + 1][y] > cur):
                self.voln( x + 1, y, cur + 1 )
        if x - 1 >= 0:
            if self.work_map[x - 1][y] == 0 or (self.work_map[x - 1][y] != -1 and self.work_map[x - 1][y] > cur):
                self.voln( x - 1, y, cur + 1 )
        if y - 1 >= 0:
            if self.work_map[x][y - 1] == 0 or (self.work_map[x][y - 1] != -1 and self.work_map[x][y - 1] > cur):
                self.voln( x, y - 1, cur + 1 )
        return self.work_map

    def exit_count_step(self):
        if not self.x:
            return

        self.check()
        ex, ey = self.get_exit_coord()
        print("\033[4m\033[36m\033[43m{}\033[0m".format(self.work_map[ey][ex]))

    def get_path(self):
        if not self.x:
            return

        x, y = self.get_exit_coord()

        path = [[x, y]]

        while not [self.x, self.y] in path:
            if x > 0 and self.work_map[x - 1][y] == self.work_map[x][y] - 1 and self.map[x - 1][y] == ' ':
                path.append([x - 1, y])
                x = x - 1
            elif x < len(self.work_map) and self.work_map[x + 1][y] == self.work_map[x][y] - 1 and self.map[x + 1][y] == ' ':
                path.append([x + 1, y])
                x = x + 1
            elif y > 0 and self.work_map[x][y - 1] == self.work_map[x][y] - 1 and self.map[x][y - 1] == ' ':
                path.append([x, y - 1])
                y = y - 1
            elif y < len(self.work_map[0]) and self.work_map[x][y + 1] == self.work_map[x][y] - 1 and self.map[x][
                y + 1] == ' ':
                path.append([x, y + 1])
                y = y + 1
        return path

    def exit_show_step(self):
        if not self.x:
            return

        self.check()
        path = self.get_path()
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if i == self.x and j == self.y:
                    print(emoji.emojize(":turtle:"), end='')
                    # print('\N{Ladder}', end=' ' )  # сремянка, стена
                elif [i, j] in path:
                    print("\033[34m{}\033[0m".format('•'),  end='')
                else:
                    print(self.map[i][j],  end='')
            print()
    def exit(self):
        pass

a = LabirintTurtle()
# a.load_map('hard_test1.txt')
a.load_map("l1.txt")
# a.show_map(turtle=True)
# a.get_exit_coord()
# a.exit_count_step()
# a.check_map()
# print(a.get_path())
a.exit_show_step()
a.exit_count_step()


