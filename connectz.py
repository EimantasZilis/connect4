import argparse
import sys
from itertools import cycle, tee
from pathlib import Path
from typing import List, Optional


def sliding_window(iterable, size):
    """
    Applies a sliding window of a given size to an iterable
    and returns (every) smaller list that can fit into an iterable"""
    iters = tee(iterable, size)
    for i in range(1, size):
        for each in iters[i:]:
            next(each)
    return zip(*iters)


class GameWinner(Exception):
    """An exception to indicate that the game has been won"""


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


class GameChecker:
    def check_for_wins(self) -> None:
        """Check if the game has been won"""
        if self.total_moves >= 2 * self.winning_moves - 1:
            # Only start checking for wins if the first player has
            # managed to put the lowest possible winning moves
            try:
                self.check_vertical_line()
                self.check_left_diagonal_line()
                self.check_right_diagonal_line()
                self.check_horizontal_lines()
            except GameWinner as e:
                self.winner = e

    def check_line_for_win(self, line: Optional[int]) -> None:
        """Check if the current player has won based on a given line"""
        if len(line) < self.winning_moves:
            # The line isn't long enough to be able to win
            return

        for position in reversed(range(self.winning_moves)):
            # Loop backwards through line positions starting
            # from the checker that was added in this turn.
            if line[position] != self.current_player:
                # There's a checker belonging to another player. You
                # won't get a winning number of checkers in a row
                return

        # The line has been checked successfully without:
        # 1. running out of positions on the board
        # 2. without having any blank or other player's checkers in a row
        # The current player has won the game.
        self.winner = str(self.current_player)
        raise GameWinner(f"{self.current_player}")

    def check_vertical_line(self):
        """
        Check if the player has one by looking at
        the column that has a new checker
        """
        #  Get a line of checkers in a column with the one recently added
        line = self.board[self.current_column][: self.current_row + 1]
        self.check_line_for_win(line)

    def get_diagonal_line(self, orientation="right") -> Optional[int]:
        """
        Get a diagonal line pointing downwards. Orientation
        specifies if the diagonal is pointing "left" or "right".
        """
        line = []

        def column_value(position):
            if orientation == "right":
                return self.current_column + position
            elif orientation == "left":
                return self.current_column - position

        try:
            for psn in range(self.max_diagonal_length):
                row = self.current_row - psn
                column = column_value(psn)
                line.append(self.board[column][row])
        except IndexError:
            # Ran out of cols/rows.
            # It has already built a full diagonal line
            pass
        finally:
            return line

    def check_right_diagonal_line(self) -> None:
        """
        Check if the player has won by looking at the right
        diagonal pointing downwards starting with a new checker
        """
        line = self.get_diagonal_line(orientation="right")
        self.check_line_for_win(line)

    def check_left_diagonal_line(self) -> None:
        """
        Check if the player has won by looking at the left
        diagonal pointing downwards starting with a new checker
        """
        line = self.get_diagonal_line(orientation="left")
        self.check_line_for_win(line)

    def check_horizontal_lines(self) -> None:
        """
        Check if the player has won by looking at the horizonal
        line that the new checker has been put in"""

        # If the board width is bigger than the number of winning
        # moves required, there is more than one way to build a line.
        # Apply a sliding window along row to find every possible
        # line and check if it has a winning combination.

        # Get the first possible column to check
        first_col = self.current_column - self.winning_moves
        actual_starting_col = 0 if first_col < 0 else first_col

        # Get the last possible column to check
        last_col = self.current_column + self.winning_moves
        actual_finishing_col = self.width if last_col > self.width else last_col

        row = [
            self.board[column][self.current_row]
            for column in range(actual_starting_col, actual_finishing_col)
        ]

        # Get every possible line of length self.winning_moves
        # by applying a slidng window to the row
        for line in sliding_window(row, self.winning_moves):
            self.check_line_for_win(line)


class GameBoard(GameChecker):
    def __init__(
        self, width: int, height: int, winning_moves: int, file_object
    ) -> None:
        self.file_object = file_object
        self.winning_moves = winning_moves
        self.player = cycle(range(1, 3))  #  Alternate player turn (1 or 2)

        self.board = [[None for row in range(height)] for col in range(width)]
        self.winner = None

        self.current_player = None
        self.current_column = None
        self.current_row = None
        self.total_moves = 0

        # The maximum number of items in a diagonal line to check
        self.max_diagonal_length = min(height, width)
        self.width = width
        self.height = height

    def make_move(self, move: int):
        column = move - 1
        try:
            # Find the first blank position along the column for next move
            row = next(x for x, psn in enumerate(self.board[column]) if psn is None)
        except StopIteration:
            # Illegal row. The column is already full.
            sys.exit("5")
        except IndexError:
            # Illegal column. Column chosen outside the board
            sys.exit("6")
        else:
            self.current_column = column
            self.current_row = row
            self.total_moves += 1
            self.current_player = next(self.player)
            self.board[column][row] = self.current_player

    def get_player_moves(self) -> List[int]:
        """A generator which returns next player moves"""
        for next_move in self.file_object:
            next_move = next_move.rstrip("\n")
            try:
                next_move = int(next_move)
            except ValueError:
                # Moves should only be denoted by a digit
                sys.exit("8")

            if next_move <= 0:
                # It doesn't make sense to have a column <= 0
                sys.exit("8")
            else:
                yield next_move

    def finish_game(self):
        """
        Perform final evaluations at the end of the game
        to determine output code"""
        if self.winner is None and self.total_moves < self.width * self.height:
            # Game is not finished, but no further moves were made
            sys.exit("3")
        if self.winner is None:
            # Draw
            sys.exit("0")
        else:
            # Game winner
            sys.exit(self.winner)

    def print_real_board(self):
        real_board = list(map(list, zip(*self.board)))
        self._print_board(real_board)

    def print_internal_board(self):
        self._print_board(self.board)

    @staticmethod
    def _print_board(board):
        for row in board:
            print(row)
        print()


def play_game(file: Path) -> None:
    """
    Start the game by reading the file and making the moves.
    It will check if the game has been won.
    """
    with file.open(encoding="ascii") as file_object:
        try:
            next(file_object).rstrip("\n")
            setup = next(file_object).rstrip("\n")
        except StopIteration:
            # File contents do not meet expected format
            sys.exit("8")

        width, height, winning_moves, *_ = map(int, setup.split(" "))
        if width < winning_moves and height < winning_moves:
            # Illegal game. Game can never be won, because
            # there are not enough rows/columns.
            sys.exit("7")

        board = GameBoard(width, height, winning_moves, file_object)
        for move in board.get_player_moves():
            if board.winner is None:
                board.make_move(move)
                board.check_for_wins()
            else:
                # Trying to make an illegal move
                sys.exit("4")

        board.finish_game()


def main() -> None:
    arg_parser = ArgParser()
    file = arg_parser.get_file()
    try:
        play_game(file)
    except (OSError, IOError, UnicodeError):
        # There are some issues opening and reading the file
        sys.exit("9")


if __name__ == "__main__":
    main()
