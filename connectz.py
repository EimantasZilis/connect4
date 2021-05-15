import argparse
import sys
from itertools import cycle
from pathlib import Path
from typing import List


class ArgParser:
    """Get input argument and validate that it exists"""

    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description="Connect Z")
        parser.add_argument(
            "inputfilename", type=str, nargs="?", help="Enter file name"
        )
        self.args = parser.parse_args()

    def get_file(self) -> Path:
        """
        Get file from inputfilename argument.
        It makes sure that the file also exists.
        """
        self._validate_inputfilename()
        return self._validate_path()

    def _validate_inputfilename(self) -> None:
        """
        Validate that inputfilename argument is specified.
        It stops the program otherwise.
        """
        if self.args.inputfilename is None:
            sys.exit("connectz.py: Provide one input file")

    def _validate_path(self) -> Path:
        """
        Validate that inputfilename argument is a path and that it exists
        """
        input_file = Path(self.args.inputfilename)
        if input_file.exists():
            return input_file
        else:
            sys.exit("9")


class GameBoard:
    def __init__(
        self, width: int, height: int, winning_moves: int, file_object
    ) -> None:
        self.file_object = file_object
        self.winning_moves = winning_moves
        self.player = cycle(range(1, 3))  #  The turn of the player (1 or 2)
        self.total_moves = 0

        # Internal representation of the game board.
        # It is actually stored transposed to make it easier
        # to use and access elements elsewhere in the code.
        self.board = [[None for row in range(height)] for col in range(width)]
        self.height = height

    def check_for_wins(self):
        pass

    def make_move(self, move: int):
        column = move - 1
        try:
            new_position = next(
                x for x, psn in enumerate(self.board[column]) if psn is None
            )
        except StopIteration:
            # Illegal row. The column is already full.
            sys.exit("5")
        except IndexError:
            # Illegal column. Column chosen outside the board
            sys.exit("6")
        else:
            self.total_moves += 1
            self.board[column][new_position] = next(self.player)

    def get_player_moves(self) -> List[int]:
        """Return a list of tuples containing (Player, Move)"""
        for next_move in self.file_object:
            next_move = next_move.rstrip("\n")
            try:
                next_move = int(next_move)
            except ValueError:
                # Moves should only be denoted by a digit
                sys.exit("8")

            if next_move <= 0:
                # It doesn't make sense to have a column <= 0
                sys.exit("8")
            else:
                yield next_move

    def print_real_board(self):
        real_board = list(map(list, zip(*self.board)))
        self._print_board(real_board)

    def print_internal_board(self):
        self._print_board(self.board)

    @staticmethod
    def _print_board(board):
        for row in board[::-1]:
            print(row)
        print()


def main() -> None:
    arg_parser = ArgParser()
    file = arg_parser.get_file()

    with file.open(encoding="ascii") as file_object:
        header = next(file_object).rstrip("\n")
        setup = next(file_object).rstrip("\n")
        width, height, winning_moves, *_ = map(int, setup.split(" "))

        if width < winning_moves and height < winning_moves:
            # Illegal game. Game can never be won, because
            # there are not enough rows/columns.
            sys.exit("7")

        board = GameBoard(width, height, winning_moves, file_object)
        for move in board.get_player_moves():
            board.make_move(move)
            board.check_for_wins()

        board.print_real_board()


if __name__ == "__main__":
    main()
