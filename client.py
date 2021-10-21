from networking import Client
from functions import *
import re
from pyfiglet import figlet_format as banner


class App:
    def __init__(self):
        self.client = Client()
        self.client.setup()

        self.icon = self.client.get()
        print(f"Icon: {self.icon}\n")

        self.board = get_board()

        self.done = False
        while not self.done:
            self.data = str_to_dict(self.client.get())

            if self.data["reason"] == "your-turn":
                self.board = str_to_board(self.data["content"])
                clear()
                print_board(self.board)

                print("Your turn")
                is_valid = False
                while not is_valid:
                    placement = input("> ").lower()
                    if (re.match("[abc][123]", placement) and self.board[list(placement)[0]][list(placement)[1]] == "-") or placement == "exit":
                        is_valid = True
                    else:
                        if placement == "exit":
                            quit()
                        else:
                            print("Invalid field")

                placement = list(placement)
                self.board[placement[0]][placement[1]] = self.icon

                self.client.post(board_to_str(self.board))

                clear()
                print_board(self.board)

            elif self.data["reason"] == "end":
                state = self.data["content"].split(";")[0]
                board = str_to_board(self.data["content"].split(";")[1])

                print(f'\n{"-"*10}\n')
                print_board(board)
                if state == "tie":
                    print(banner("It's a tie!"))
                elif state == self.icon:
                    print(banner("You won!"))
                else:
                    print(banner("You lose"))
                quit()


if __name__ == "__main__":
    app = App()
