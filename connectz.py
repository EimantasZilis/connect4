import argparse
import sys
from pathlib import Path


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
        self.board = [[None for col in range(width)] for row in range(height)]
        self.turn = 1  # Specifies if it's player turn 1 or 2

    def player_moves(self) -> int:
        """A generator method which reads and returns moves made by players"""
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


def main() -> None:
    arg_parser = ArgParser()
    file = arg_parser.get_file()

    with file.open(encoding="ascii") as file_object:
        header = next(file_object).rstrip("\n")
        setup = next(file_object).rstrip("\n")
        width, height, winning_moves, *_ = map(int, setup.split(" "))
        board = GameBoard(width, height, winning_moves, file_object)
        for move in board.player_moves():
            print(move)


if __name__ == "__main__":
    main()
