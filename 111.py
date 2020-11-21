class LabirintTurtle():
    def __init__(self):
        self.f = None
        self.m = list()
        self.m2 = list()
        self.ex = list()
        self.x = None
        self.y = None
    def load_map(self, name):
        self.f = list(open(name, "r").read().split("\n"))
        for i in self.f[:-2]:
            self.m.append(list(i))
        if self.f[-2].isdigit():
            self.x = int(self.f[-2])
            self.y = int(self.f[-1])
    def show_map(self, turtle=None):
        for i in self.m:
            self.m2.append(list(i))
        self.m2[self.y][self.x] = "A"
        if turtle:
            for i in self.m2:
                print(*i)
        else:
            for i in self.m:
                print(*i)
    def check_map(self):
        s = 0
        w = 0
        for i in self.m:
            for t in i:
                if t != "*" and t != " ":
                    s += 1
        for i in [0, -1]:
            if " " in self.m[i]:
                w += 1
        for i in range(1, len(self.m) - 1):
            if " " == self.m[i][0] or " " == self.m[i][-1]:
                w += 1
        if s != 0 or w != 1 or self.x == None or self.y == None or self.m[self.y][self.x] != " ":
            print("Загрузите другую карту")

    def exit_count_step(self):
        q = 0
        for i in 0, -1:
            for t in self.m[i]:
                if " " == t and i == 0 or i == len(self.m):
                    self.ex.append(i)
                    self.ex.append(q)
                q += 1
        for i in range(1,len(self.m) - 1):
            if " " == self.m[i][0]:
                self.ex.append(i)
                self.ex.append(0)

        print(self.ex)
        # while self.m[self.y -1 ][self.x] == "*":
        #     while self.m[self.y][self.x + 1] ==
    def exit_show_step(self):
        pass

b = LabirintTurtle()
b.load_map("l1.txt")
b.show_map(turtle=True)
b.check_map()
b.exit_count_step()


