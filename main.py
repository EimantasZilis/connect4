from pathlib import Path

from game import Game
from helpers import ArgParser, show_summary


def start_game(file: Path) -> str:
    """Use the game file to make moves and play the game"""
    try:
        with file.open(mode="r") as fp:
            game = Game(fp)
            return game.play()
    except (OSError, IOError, UnicodeError):
        return "9"


def main() -> None:
    arg_parser = ArgParser()
    file = arg_parser.get_path()

    status = start_game(file)
    show_summary(status)


if __name__ == "__main__":
    main()
