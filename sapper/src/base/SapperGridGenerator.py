from random import randint


def generate(length, width, mines):
    grid = [[0 for x in range(width)] for y in range(length)]
    remained_mines = mines;
    while remained_mines > 0:
        x = randint(0, width - 1)
        y = randint(0, length - 1)
        if grid[y][x] == 0:
            grid[y][x] = 1
            remained_mines -= 1
    cnt_mines_around = [[0 for x in range(width)] for y in range(length)]
    for y in range(length):
        for x in range(width):
            direction_x = [-1, 0, 1]
            direction_y = [-1, 0, 1]
            for dir_y in direction_y:
                for dir_x in direction_x:
                    if 0 <= dir_y + y < length and 0 <= dir_x + x < width:
                        cnt_mines_around[y][x] += grid[y + dir_y][x + dir_x]
    return grid, cnt_mines_around
