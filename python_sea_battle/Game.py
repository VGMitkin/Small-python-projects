from random import randint, shuffle
from typing import Union


class Ship:
    """Ship representation"""

    HORIZONTAL = 1
    VERTICAL = 2

    def __init__(self, length: int, tp: int = HORIZONTAL, x: int = None, y: int = None):
        self._length = length
        self._tp = tp
        self._x = x
        self._y = y
        self._is_move = True
        self._cells = [1] * length

    def __repr__(self):
        return f'({self._length}-палубный, {"Горизонтальный" if self._tp == 1 else "Вертикальный"}, ' \
               f'{"Целый" if self._is_move else "Подбитый"}, ' \
               f'x={self._x} y={self._y})'

    def __setattr__(self, key, value):
        if key in ('_x', '_y', '_length'):
            if not isinstance(value, int) and value is not None or \
                    isinstance(value, int) and value < 0:
                raise TypeError('Координаты и длина должны быть целыми положительными числами')

        if key == '_tp':
            if not isinstance(value, int) or value not in (1, 2):
                raise ValueError('Значение ориентации должно быть 1 или 2')

        super().__setattr__(key, value)

    def __bool__(self):
        """Method for checking ship status
         False - if the ship is completely destroyed,
         True - if there are still whole decks"""
        return not all(x == 2 for x in self._cells)

    @property
    def tp(self):
        return self._tp

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def length(self):
        return self._length

    @property
    def is_move(self):
        return self._is_move

    @is_move.setter
    def is_move(self, value):
        if type(value) == bool:
            self._is_move = value

    def set_start_coords(self, x: int, y: int):
        """Method for setting initial ship coordinates"""
        self._x = x
        self._y = y

    def get_start_coords(self) -> tuple:
        """Getting the initial coordinates of the ship"""
        return self._x, self._y

    def move(self, go: int):
        """The method implements the movement of the ship in the direction of its orientation to 'go' cells"""
        if self._is_move:
            x, y = self.get_start_coords()
            if self._tp == self.HORIZONTAL:
                self.set_start_coords(x + go, y)
            elif self._tp == self.VERTICAL:
                self.set_start_coords(x, y + go)

    @staticmethod
    def _get_place_and_around_coordinates(ship_orientation: int, ship: 'Ship') -> tuple:
        """Method for getting the coordinates of the location of the entire ship and
         coordinates around the ship"""
        indexes = (-1, 0), (1, 0), (0, 1), (0, -1), (-1, -1), (1, -1), (-1, 1), (1, 1), (0, 0)
        all_coord = set()
        ship_coord = set()
        x, y, length = ship._x, ship._y, ship._length

        if ship_orientation == ship.HORIZONTAL:
            ship_coord = {(x + j, y) for j in range(length)}

        elif ship_orientation == ship.VERTICAL:
            ship_coord = {(x, y + i) for i in range(length)}

        for a, b in indexes:
            for c, d in ship_coord:
                all_coord.add((a + c, b + d))

        return all_coord, ship_coord

    def is_collide(self, ship: 'Ship') -> bool:
        """Method for checking for collision or contact with another 'ship'"""
        if isinstance(ship, Ship):
            all_coord_self, self_coord = self._get_place_and_around_coordinates(self._tp, self)
            all_coord_ship, ship_coord = ship._get_place_and_around_coordinates(ship._tp, ship)
            common_coord = all_coord_self & all_coord_ship
            result = (self_coord & common_coord) | (ship_coord & common_coord)
            return len(result) != 0

    def is_out_pole(self, size: int) -> bool:
        """Method for checking if a ship is out of bounds"""
        x, y = self._x, self._y
        last_part_coord = (x + self._length - 1, y) if self._tp == self.HORIZONTAL else (x, y + self._length - 1)
        return x < 0 or last_part_coord[0] > size - 1 or y < 0 or last_part_coord[1] > size - 1

    def _check_index(self, index) -> bool:
        """Method for checking the index for working with the _cells list"""
        return 0 <= index < len(self._cells)

    def __getitem__(self, item: int) -> int:
        """Method for reading a value from the _cells list at the item index"""
        if self._check_index(item):
            return self._cells[item]

    def __setitem__(self, key, value):
        """Method for writing a new value to _cells at index key"""
        if self._check_index(key) and isinstance(value, int) and value in (1, 2):
            self._cells[key] = value


class GamePole:
    """Class for describing the playing field"""

    def __init__(self, size: int = 10):
        self._size = size
        self._ships = []
        self._field = [[0] * self._size for _ in range(self._size)]
        self._name = ''
        self._count_dead_ships = 0
        self._generate_ships()

    def __bool__(self):
        return self._count_dead_ships == 10

    @property
    def ships(self):
        return self._ships

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str):
            self._name = value

    @property
    def count_dead_ships(self):
        return self._count_dead_ships

    @count_dead_ships.setter
    def count_dead_ships(self, value):
        if isinstance(value, int):
            self._count_dead_ships = value

    def _check_ships_around(self, length: int, head_coord: tuple, orientation: int) -> int:
        """Method for checking the presence of ships around and at the installation site of the ship"""
        indexes = (-1, 0), (1, 0), (0, 1), (0, -1), (-1, -1), (1, -1), (-1, 1), (1, 1), (0, 0)
        head_x, head_y = head_coord
        result = 0

        if orientation == 1:  # horizontal
            j = head_x
            k = 0
            while length > k:
                result += sum(self._field[head_y + x][j + y] for x, y in indexes
                              if 0 <= head_y + x < self._size and 0 <= j + y < self._size)
                j += 1
                k += 1

        elif orientation == 2:  # vertical
            i = head_y
            k = 0
            while length > k:
                result += sum(self._field[i + x][head_x + y] for x, y in indexes
                              if 0 <= i + x < self._size and 0 <= head_x + y < self._size)
                i += 1
                k += 1

        return result

    def _generate_ships(self):
        """Method for creating ships with random orientation and no initial coordinates"""
        self._ships = [Ship(4, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)),
                       Ship(2, tp=randint(1, 2)), Ship(2, tp=randint(1, 2)), Ship(2, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2)), Ship(1, tp=randint(1, 2)), Ship(1, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2))]

    def init(self):
        """Method for the initial initialization of the playing field"""
        for ship in self._ships:
            tp, length = ship.tp, ship.length
            while True:
                x, y = randint(0, self._size - 1), randint(0, self._size - 1)
                if tp == ship.HORIZONTAL:
                    if x + (length - 1) > self._size - 1:
                        continue

                    result = self._check_ships_around(length, (x, y), tp)

                    if not result:
                        k = 0
                        for j in range(x, x + length):
                            self._field[y][j] = ship[k]
                            k += 1
                    else:
                        continue

                elif tp == ship.VERTICAL:
                    if y + (length - 1) > self._size - 1:
                        continue

                    result = self._check_ships_around(length, (x, y), tp)

                    if not result:
                        k = 0
                        for i in range(y, y + length):
                            self._field[i][x] = ship[k]
                            k += 1
                    else:
                        continue

                ship.set_start_coords(x, y)
                break

    def get_ships(self) -> list:
        """Method for returning a list of ships on the field"""
        return self._ships

    def update_game_field(self):
        """Method for updating the playing field
         after the movement of the ships and after each move"""
        for i in range(self._size):
            for j in range(self._size):
                self._field[i][j] = 0

        for ship in self._ships:
            x, y, length = ship.x, ship.y, ship.length
            ship_part = 0

            if ship.tp == ship.HORIZONTAL:
                for j in range(x, x + length):
                    self._field[y][j] = ship[ship_part]
                    ship_part += 1
            elif ship.tp == ship.VERTICAL:
                for i in range(y, y + length):
                    self._field[i][x] = ship[ship_part]
                    ship_part += 1

    def move_ships(self):
        """Method to move each ship one space"""
        for ship in self._ships:
            old_x, old_y = ship.get_start_coords()
            directions = ['forward', 'back']
            is_conflict = False
            while directions or not is_conflict:
                shuffle(directions)
                direction = directions.pop()

                x = y = 0
                if direction == 'forward' and ship.tp == ship.HORIZONTAL and ship.is_move:
                    x = ship.x + 1
                    y = ship.y
                elif direction == 'back' and ship.tp == ship.HORIZONTAL and ship.is_move:
                    x = ship.x - 1
                    y = ship.y
                elif direction == 'forward' and ship.tp == ship.VERTICAL and ship.is_move:
                    x = ship.x
                    y = ship.y + 1
                elif direction == 'back' and ship.tp == ship.VERTICAL and ship.is_move:
                    x = ship.x
                    y = ship.y - 1
                else:
                    break

                try:
                    ship.set_start_coords(x, y)
                except TypeError:
                    continue

                if ship.is_out_pole(self._size):
                    ship.set_start_coords(old_x, old_y)
                    continue

                for curr_ship in self._ships:
                    if curr_ship != ship:
                        if not ship.is_collide(curr_ship):
                            continue
                        else:
                            ship.set_start_coords(old_x, old_y)
                            is_conflict = True
                            break
                if is_conflict:
                    continue
                break

        self.update_game_field()

    def show(self):
        """Method for displaying the playing field in the console"""
        print(f'{self.name:^{self._size * 2}}')
        print(' '.join(chr(i) for i in range(97, 97 + self._size)))
        print('-' * (self._size * 2 - 1))

        for i, row in enumerate(self._field, 1):
            print(f'{" ".join(str(s) for s in row)}  {i}')
        print('_' * (self._size * 2 - 1))
        print()

    def get_pole(self) -> tuple:
        """Method for getting the current playing field"""
        return tuple(tuple(row) for row in self._field)

    def __repr__(self) -> str:
        return f'Размер поля - {self._size} x {self._size}'


class SeaBattle:
    """Class for setting up and running the gameplay"""
    _x_coord_translate = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10}
    _comp_ships_coord = {}
    _human_ships_coord = {}

    def __init__(self, size_field, name_1: str = 'Computer', name_2: str = 'Human'):
        self._size_field = size_field
        self.computer, self.human = GamePole(size_field), GamePole(size_field)
        self.computer.name, self.human.name = name_1, name_2
        self._hit_points_comp = []
        self._hit_points_human = []
        self.result_field = [['-'] * self._size_field for _ in range(self._size_field)]

    def init(self):
        """Method for initializing computer and human fields.
         The method produces the placement of ships on the fields of rivals"""
        self.computer.init()
        self.human.init()
        self._comp_ships_coord = self.get_all_ships_parts_coord(self.computer)
        self._human_ships_coord = self.get_all_ships_parts_coord(self.human)

    @staticmethod
    def get_all_ships_parts_coord(field: GamePole) -> dict:
        """Method for getting the coordinates of all ship decks"""
        ships = field.ships
        ship_coord = {ship: [] for ship in ships}
        for ship, coord in ship_coord.items():
            x, y = ship.get_start_coords()
            length = ship.length
            for i in range(length):
                next_x_y = (x + i, y) if ship.tp == ship.HORIZONTAL else (x, y + i)
                coord.append(next_x_y)

        return ship_coord

    def recognize_shell_place(self, shell_coord: tuple, gamer: GamePole) -> Union[Ship, None]:
        """Method for recognizing the location of a projectile impact"""
        ships = self._comp_ships_coord if gamer is self.human else self._human_ships_coord
        place = list(filter(lambda x: shell_coord in ships[x], ships))
        return place[0] if place else None

    def human_go(self):
        """Method for realizing a person's move"""
        x = y = None
        while True:
            try:
                coord = input('Введите координаты поля для выстрела в формате \'a1\': ')
                x, y = coord[0], str(coord[1:])
            except (TypeError, IndexError, ValueError):
                print('Введен не верный тип и/или диапазон координат')
                continue
            else:
                if coord[0].lower() in [chr(let) for let in range(97, 97 + self._size_field)] and \
                        coord[1] in [str(d) for d in range(1, self._size_field + 1)]:
                    x, y = self._x_coord_translate.get(x) - 1, int(y) - 1
                    if (x, y) in self._hit_points_human:
                        print('Координаты уже использовались')
                        continue
                    break
                continue

        shell_place = self.recognize_shell_place((x, y), self.human)
        self._hit_points_human.append((x, y))

        if shell_place is not None:
            self._marked_broken_ship_part(self.human, shell_place, (x, y))
            self.computer.update_game_field()
            self.show_shot_location(x, y, 'X')
        else:
            self.show_shot_location(x, y, '*')

    def _marked_broken_ship_part(self, gamer: GamePole, shell_place: Ship, coord_place: tuple):
        """The method implements a search for a damaged ship deck and marks it as destroyed"""
        ships_coord = self._human_ships_coord if gamer is self.computer else self._comp_ships_coord
        part_num = ships_coord.get(shell_place).index(coord_place)
        shell_place[part_num] = 2
        shell_place.is_move = False
        if not shell_place:
            gamer.count_dead_ships += 1

    def computer_go(self):
        """Method to implement computer move
          randomly into free cells"""
        while True:
            x, y = randint(0, self._size_field - 1), randint(0, self._size_field - 1)
            if (x, y) in self._hit_points_comp:
                continue
            break

        shell_place = self.recognize_shell_place((x, y), self.computer)
        self._hit_points_comp.append((x, y))

        if shell_place is not None:
            self._marked_broken_ship_part(self.computer, shell_place, (x, y))
            self.human.update_game_field()
        self.human.show()

    def show_shot_location(self, x: int, y: int, state: str):
        """The method displays a field with the place where the projectile hit after the shot
         The field is displayed only after the person's move; X - there was a hit in the ship;
         * - shot past"""
        self.result_field[y][x] = state

        print(' '.join(chr(i) for i in range(97, 97 + self._size_field)))
        print('-' * (self._size_field * 2 - 1))

        for i, row in enumerate(self.result_field, 1):
            print(f'{" ".join(str(s) for s in row)}  {i}')
        print('_' * (self._size_field * 2 - 1))
        print()

    def __bool__(self):
        """The method determines the end of the battle.
         If someone has destroyed all 10 ships, the game stops"""
        return not self.human and not self.computer