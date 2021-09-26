from src.error.InvalidMoveError import InvalidMoveError
from ..base import SapperGridGenerator


class Field:
    def __init__(self, *args):
        if len(args) == 3:
            self.length = args[0]
            self.width = args[1]
            self.mines = args[2]
            self.grid, self.cnt_mines_around = SapperGridGenerator.generate(self.length, self.width, self.mines)
            self.visitable_cell = set()
            self.flag_cell = set()
            self.state = "game_running"
            self.last_move = ""
            self.remains_open = self.length * self.width - self.mines
        else:
            self.grid = args[0]
            self.visitable_cell = args[1]
            self.flag_cell = args[2]
            self.cnt_mines_around = args[3]
            self.length = args[4]
            self.width = args[5]
            self.mines = args[6]
            self.state = args[7]
            self.last_move = args[8]
            self.remains_open = args[9]

    def __str__(self):
        res = "[state : " + self.state + " | last_move : " + self.last_move + " | length : " + str(self.length) + \
              " | width " + str(self.width) + " | mines : " + str(self.mines) + \
              " | remains open " + str(self.remains_open) + "]\n"
        for y in range(self.length):
            for x in range(self.width):
                if not (y, x) in self.visitable_cell and not (y, x) in self.flag_cell:
                    res += "X"
                elif (y, x) in self.visitable_cell:
                    res += str(self.cnt_mines_around[y][x])
                elif (y, x) in self.flag_cell:
                    res += "F"
            res += "\n"
        return res

    def check_cell(self, y, x):
        return 0 <= y < self.length and 0 <= x < self.width

    def check_move(self, y, x, action):
        if not self.check_cell(y, x):
            raise InvalidMoveError("the coordinates of the cell must be in the field ")
        if action not in {'open', 'flag'}:
            raise InvalidMoveError("cell action should be 'open' or 'flag'")
        if (y, x) in self.visitable_cell:
            raise InvalidMoveError("this cell already in use")

    def open_all_possible(self, y, x):
        if self.grid[y][x] == 0 and (y, x) not in self.visitable_cell:
            self.visitable_cell.add((y, x))
            self.remains_open -= 1
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for direction in directions:
                dir_y = direction[0]
                dir_x = direction[1]
                if self.check_cell(dir_y + y, dir_x + x):
                    self.open_all_possible(dir_y + y, dir_x + x)

    def make_move(self, y, x, action):
        self.last_move = str(x + 1) + " " + str(y + 1) + " " + action
        if action == 'open':
            if self.grid[y][x] == 1:
                self.state = "lose"
                return
            self.open_all_possible(y, x)
            if self.remains_open == 0:
                self.state = "win"
        elif action == 'flag':
            self.flag_cell.add((y, x))
