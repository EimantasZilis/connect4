import argparse
import sys
from itertools import tee
from pathlib import Path
from typing import Optional, Tuple


class ArgParser:
    """Get input argument and validate that it exists"""

    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description="Connect Z")
        parser.add_argument(
            "inputfilename", type=str, nargs="*", help="Enter file name"
        )
        self.args = parser.parse_args()

    def get_file(self) -> Path:
        """
        Get file from inputfilename argument.
        It makes sure that the file also exists.
        """
        input_file = self._validate_inputfilename()
        return Path(input_file)

    def _validate_inputfilename(self) -> None:
        """
        Validate that one inputfilename argument is specified.
        It stops the program otherwise.
        """
        input_file, *bad_params = self.args.inputfilename
        if input_file is None or bad_params:
            sys.exit("connectz.py: Provide one input file")
        else:
            return input_file


def parse_file_header(header: str) -> Tuple[int]:
    """
    Given a file header, parse the information
    into board width, height and winning moves.
    """

    try:
        width, height, winning_moves = map(int, header.split(" "))
        return width, height, winning_moves
    except ValueError:
        # File contents do not meet expected format
        sys.exit("8")


def validate_board_setup(width: int, height: int, winning_moves: int) -> None:
    game_specs = (width, height, winning_moves)
    if any(map(lambda x: x <= 0, game_specs)):
        # invalid values in input file
        sys.exit("8")

    if width < winning_moves and height < winning_moves:
        # Illegal game. Game can never be won, because
        # there are not enough rows/columns.
        sys.exit("7")


def sliding_window(iterable: Optional[int], size: int) -> Optional[int]:
    """
    Applies a sliding window of a given size to an iterable
    and returns (every) smaller list that can fit into an iterable"""
    iters = tee(iterable, size)
    for i in range(1, size):
        for each in iters[i:]:
            next(each)
    return zip(*iters)
