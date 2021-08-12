from enum import IntEnum


class GameCode(IntEnum):
    DRAW = 0
    PLAYER_1_WIN = 1
    PLAYER_2_WIN = 2
    INCOMPLETE_GAME = 3
    ILLEGAL_CONTINUE = 4
    ILLEGAL_ROW = 5
    ILLEGAL_COLUMN = 6
    ILLEGAL_GAME = 7
    ILLEGAL_FILE = 8
    FILE_ERROR = 9


GAME_OUTPUT_MESSAGES = {
    GameCode.DRAW: "Game Over: Draw",
    GameCode.PLAYER_1_WIN: "Game Over: Player 1 win",
    GameCode.PLAYER_2_WIN: "Game Over: Player 2 win",
    GameCode.INCOMPLETE_GAME: (
        "Game Error: Incomplete Game.\n"
        " >> The game has not been finished and there are valid moves "
        "possible, but none were taken"
    ),
    GameCode.ILLEGAL_CONTINUE: (
        "Game Error: Illegal Continue.\n"
        " >> Players cannot make moves after the game is finished"
    ),
    GameCode.ILLEGAL_ROW: (
        "Game Error: Invalid Row.\n"
        " >> Players cannot put pieces in a row that does not exist"
    ),
    GameCode.ILLEGAL_COLUMN: (
        "Game Error: Invalid Column.\n"
        " >> Players cannot put pieces in a column that does not exist"
    ),
    GameCode.ILLEGAL_GAME: (
        "Game Error: Invalid game.\n"
        " >> The game description is valid, but the game could never be won"
    ),
    GameCode.ILLEGAL_FILE: (
        "Game Error: Invalid file.\n"
        " >> The game description is not valid or described a game that is impossible"
    ),
    GameCode.FILE_ERROR: (
        "Game Error: File error.\n"
        " >> The file cannot be found, opened or read for some reason."
    ),
}
