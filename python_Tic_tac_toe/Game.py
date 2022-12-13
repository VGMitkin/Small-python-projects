from random import randint


class TicTacToe:
    FREE_CELL = 0  # свободная клетка
    HUMAN_X = 1  # крестик (игрок - человек)
    COMPUTER_O = 2  # нолик (игрок - компьютер)

    def __init__(self):
        self.pole = tuple(tuple(Cell() for _ in range(3)) for i in range(3))
        self.__is_human_win = False
        self.__is_computer_win = False
        self.__is_draw = False

    def clear(self):
        self.pole = tuple(tuple(Cell() for _ in range(3)) for i in range(3))

    def init(self):
        self.clear()
        self.is_human_win = False
        self.is_computer_win = False
        self.is_draw = False

    def check(self, idx):
        if type(idx) != tuple or len(idx) != 2:
            raise IndexError('неверный индекс клетки')
        if any(not (0 <= x <= 2) for x in idx if type(x) == int):
            raise IndexError('неверный индекс клетки')

    def __getitem__(self, idx):
        self.check(idx)
        x, y = idx
        if isinstance(x, slice):
            return tuple([self.pole[i][y].value for i in range(3)])
        elif isinstance(y, slice):
            return tuple([self.pole[x][i].value for i in range(3)])
        else:
            return self.pole[x][y].value

    def __setitem__(self, idx, value):
        self.check(idx)
        x, y = idx
        if not self.pole[x][y]:
            raise ValueError('клетка уже занята')
        self.pole[x][y].value = value
        if value == self.HUMAN_X and self.winner_check(value):
            self.is_human_win = True
        if value == self.COMPUTER_O and self.winner_check(value):
            self.is_computer_win = True
        self.is_draw_check()

    def show(self):
        for row in self.pole:
            print(*[item.value for item in row], flush=True)
        print()

    def winner_check(self, player):
        for row in self.pole:
            if all(item.value == player for item in row):
                return True

        for i in range(3):
            if all(val == player for val in (row[i].value for row in self.pole)):
                return True

        if all(self.pole[i][i].value == player for i in range(3)):
            return True

    def is_draw_check(self):
        if all(self.pole[x][y].value for x in range(3) for y in
               range(3)) and self.is_human_win == False and self.is_computer_win == False:
            self.is_draw = True

    def human_go(self):
        while True:
            x, y = map(int, input('Ведите координаты клетки через пробел').split())
            if not (0 <= x <= 2) or not (0 <= y <= 2):
                continue
            if self[x, y] == self.FREE_CELL:
                self[x, y] = self.HUMAN_X
                break
            else:
                continue

    def computer_go(self):
        while True:
            x, y = randint(0, 2), randint(0, 2)
            if not (0 <= x <= 2) or not (0 <= y <= 2):
                continue
            if self[x, y] == self.FREE_CELL:
                self[x, y] = self.COMPUTER_O
                break
            else:
                continue

    @property
    def is_human_win(self):
        return self.__is_human_win

    @is_human_win.setter
    def is_human_win(self, value):
        self.__is_human_win = value

    @property
    def is_computer_win(self):
        return self.__is_computer_win

    @is_computer_win.setter
    def is_computer_win(self, value):
        self.__is_computer_win = value

    @property
    def is_draw(self):
        return self.__is_draw

    @is_draw.setter
    def is_draw(self, value):
        self.__is_draw = value

    def __bool__(self):
        return not any([self.is_human_win, self.is_computer_win, self.is_draw])


class Cell:
    def __init__(self):
        self.value = 0

    def __bool__(self):
        return self.value == 0