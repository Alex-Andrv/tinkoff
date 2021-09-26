import pickle
import os
import random

from src.error.InvalidMoveError import InvalidMoveError
from src.error.InvalidCommandError import InvalidCommandError
from src.base.Field import Field


class Game:
    commands = ["move", "save", "exit"]

    types_of_games = {1: 'default game', 2: 'custom game'}
    int_to_item = {1: 'new game', 2: 'load game', 3: 'exit'}

    def __init__(self, player):
        self.player = player
        self.field = None

    def print_menu(self, dict):
        print("#######Menu##########")
        for i in dict:
            print(str(i) + ") " + dict[i])
        print()

    def getInt(self, item):
        if self.is_int(item):
            return int(item)
        else:
            return -1

    def is_int(self, x):
        try:
            int(x)
            return True
        except ValueError:
            return False

    def run_game(self):
        try:
            os.mkdir("saves")
        except OSError:
            print(">>> Creation of the directory saves failed")
        else:
            print(">>> Successfully created the directory saves")
        while self.field is None:
            self.print_menu(self.int_to_item)
            item = input().strip()
            item_int = self.getInt(item)
            if item == "new game" or item_int == 1:
                self.print_menu(self.types_of_games)
                item = input().strip()
                item_int = self.getInt(item)
                if item == "default game" or item_int == 1:
                    self.field = Field(5, 5, random.randint(2, 5))
                elif item == "custom game" or item_int == 2:
                    while self.field is None:
                        print(">>> Enter the length of the field. Where 0 < length < 10.")
                        length = self.getInt(input())
                        print(">>> Enter the width of the field. Where 0 < length < 10.")
                        width = self.getInt(input())
                        print(">>> Enter the count of mines. Where 0 < mines <= length * width / 2.")
                        mines = self.getInt(input())
                        if 0 < length < 10 and 0 < width < 10 and 0 < mines <= length * width / 2:
                            self.field = Field(length, width, mines)
                        else:
                            print(">>> Invalid data format")
                else:
                    print(">>> Invalid menu item")
            elif item == "load game" or item_int == 2:
                data = None
                print(">>> Enter filename without .pkl")
                filename = input()
                try:
                    with open("saves/" + filename + ".pkl", "rb") as f:
                        data = pickle.load(f)
                except Exception:
                    print(">>> There is no such file or it damaged")
                self.field = Field(data['grid'], data['visitable_cell'],
                                   data['flag_cell'], data['cnt_mines_around'], data['length'],
                                   data['width'], data['mines'], data['state'], data['last_move'],
                                   data['remains_open'])
            elif item == "exit" or item_int == 3:
                exit(0)
            else:
                print(">>> Invalid menu item")

        while self.field.state == "game_running":
            print(self.field)
            try:
                command = self.player.get_command()
                if command not in self.commands:
                    raise InvalidCommandError("There is no such command")
                elif command == "save":
                    filename = self.player.get_save_filename()
                    data = {'grid': self.field.grid,
                            'visitable_cell': self.field.visitable_cell,
                            'flag_cell': self.field.flag_cell,
                            'cnt_mines_around': self.field.cnt_mines_around,
                            'length': self.field.length,
                            'width': self.field.width,
                            'mines': self.field.mines,
                            'state': self.field.state,
                            'last_move': self.field.last_move,
                            'remains_open': self.field.remains_open}
                    with open("saves/" + filename + ".pkl", "wb") as f:
                        pickle.dump(data, f)
                    print(">>> Game saved to saves/" + filename + ".pkl")
                elif command == "move":
                    x, y, action = self.player.get_move()
                    self.field.check_move(y, x, action)
                    self.field.make_move(y, x, action)
                elif command == "exit":
                    exit(0)

            except InvalidMoveError as e:
                self.player.put_error(str(e))
            except InvalidCommandError as e:
                self.player.put_error(str(e))
            except ValueError:
                self.player.put_error("Invalid command format")
        print(self.field)
        if self.field.state == "win":
            print(">>> You successfully win!")
        elif self.field.state == "lose":
            print(">>> You lose")
        input()
