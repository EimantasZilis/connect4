from constants import status_codes
from game import GameError, GameOver, start_game
from helpers import ArgParser


def evaluate_game(file):
    try:
        start_game(file)
    except GameOver as game_code:
        if game_code == 0:
            print("Game Over: draw")
        else:
            print(f"Game over. Player {game_code} won")
    except GameError as error_code:
        print(f"Game Error: {status_codes[error_code]}")


def main() -> None:
    arg_parser = ArgParser()
    file = arg_parser.get_file()

    evaluate_game(file)


if __name__ == "__main__":
    main()
