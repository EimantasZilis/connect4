from pathlib import Path
from typing import Union

from constants import status_codes
from game import Game, GameError, GameOver
from helpers import ArgParser


class Connect4:
    def __init__(self, file: Path) -> None:
        self.file = file

    def __enter__(self) -> Game:
        self._fp = self.file.open(mode="r")
        return Game(self._fp)

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self._fp.close()
        self.print_summary(exc_type, exc_val)
        return True

    def print_summary(self, exception: Union[GameOver, GameError], value: int) -> None:
        print(f" >> value: {value}, type: {type(value)}")
        print(f" >> stage: {exception}")

        if exception == GameOver:  # state == GameOver:
            if value == 0:
                print("Draw")
            else:
                print(f"Player {value} won")
        elif exception == GameError:
            print(f"Game Error: {status_codes[int(e)]}")
        else:
            print(f"Unknown Error: {exception} - value: {value}")


def main() -> None:
    arg_parser = ArgParser()
    file = arg_parser.get_file()

    with Connect4(file) as game:
        game.play()


if __name__ == "__main__":
    main()
