from game import Game
from helpers import ArgParser


def main() -> None:
    arg_parser = ArgParser()
    file = arg_parser.get_path()

    with file.open(mode="r") as fp:
        game = Game(fp)
        game.play()
        game.show_summary()


if __name__ == "__main__":
    main()
