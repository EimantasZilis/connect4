import sys

from game import play_game
from helpers import ArgParser


def main() -> None:
    arg_parser = ArgParser()
    file = arg_parser.get_file()
    try:
        play_game(file)
    except (OSError, IOError, UnicodeError):
        # There are some issues with opening or reading the file
        sys.exit("9")


if __name__ == "__main__":
    main()
