class LabirintTurtle():
    def __init__(self):
        self.f = None
    def load_map(self, name):
        self.f = open(name, "r")
        return self.f.read()
    def show_map(self):
        pass
    def check_map(self):
        pass
    def exit_count_step(self):
        pass
    def exit_show_step(self):
        pass

b = LabirintTurtle()
print(b.load_map("1map.txt"))