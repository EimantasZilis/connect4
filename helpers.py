import argparse
from itertools import tee
from pathlib import Path
from typing import Generator, Optional

from config import GAME_STATUSES


class ArgParser:
    """Get input argument and validate that it exists"""

    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description="Connect4")
        parser.add_argument(
            "filename", type=str, help="Filename describing the game play"
        )
        self.args = parser.parse_args()

    def get_path(self) -> Path:
        """Get path from path argument"""
        return Path(self.args.filename)


def sliding_window(iterable: Optional[int], size: int) -> Generator[int, None, None]:
    """
    Applies a sliding window of a given size to an iterable
    and returns (every) smaller list that can fit into an iterable"""
    iters = tee(iterable, size)
    for i in range(1, size):
        for each in iters[i:]:
            next(each)
    return zip(*iters)


def show_summary(status: str) -> None:
    if status == "0":
        print("Draw")
    elif status in ("1", "2"):
        print(f"Player {status} won")
    elif status in map(str, range(3, 10)):
        print(f"Game Error: {GAME_STATUSES[status]}")
    else:
        print(f"Unknown Error - code: {status}")
