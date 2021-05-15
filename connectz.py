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


class ImportGame:
    """
    A class for importing game from file.
    It reads the input file, validates that file contents
    are correct and parses the information within.
    """

    def __init__(self, file: Path) -> None:
        self.file = file
        self.columns = None
        self.rows = None
        self.winning_moves = None

    def __enter__(self) -> None:
        """Read game setup from file"""
        self.file_object = self.file.open(encoding="ascii")
        header = self.file_object.readline().rstrip("\n")
        setup = self.file_object.readline().rstrip("\n")

        self.width, self.height, self.winning_moves, *bad_args = map(
            int, setup.split(" ")
        )

        if header != "X Y Z":
            # Invalid headers
            sys.exit("8-1")
        elif bad_args:
            # There shouldn't be any more than 3 args
            sys.exit("8-2")

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Close file"""
        self.file_object.close()

    def next_move(self):
        """Generator method to read file line-by-line"""
        # Skip the first two lines and go straight to the moves
        next(self.file_object)
        next(self.file_object)

        for line in self.file_object:
            stripped_line = line.rstrip("\n")
            print(stripped_line)
            yield int(stripped_line)


def main() -> None:
    arg_parser = ArgParser()
    file = arg_parser.get_file()

    with ImportGame(file) as game:
        pass

        # for move in game_setup.moves:
        # print(move)


if __name__ == "__main__":
    main()
