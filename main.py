from pathlib import Path

from game import Game
from helpers import ArgParser


class Connect4:
    def __init__(self, file: Path) -> None:
        self.file = file

    def __enter__(self) -> Game:
        self._fp = self.file.open(mode="r")
        return Game(self._fp)

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._fp.close()


def main() -> None:
    arg_parser = ArgParser()
    file = arg_parser.get_file()

    with Connect4(file) as game:
        game.play()
        game.show_summary()


if __name__ == "__main__":
    main()
