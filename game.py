from itertools import cycle
from typing import List, Optional, TextIO, Tuple

from exceptions import GameError, GameOver
from helpers import sliding_window


class GameChecker:
    """
    A class for checking if the game has been won.
    It looks at all lines around a recent piece and
    checks if there are any lines that have a winning
    number of pieces belonging to the same player.
    """

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
            except GameOver as e:
                self.winner = e

    def check_line_for_win(self, line: Optional[int]) -> None:
        """Check if the current player has won based on a given line"""
        if len(line) < self.winning_moves:
            # The line isn't long enough to be able to win
            return

        for position in reversed(range(self.winning_moves)):
            # Loop backwards through line positions starting
            # from the piece that was added in this turn.
            if line[position] != self.current_player:
                # There's a piece belonging to another player. You
                # won't get a winning number of pieces in a row
                return

        # The line has been checked successfully without:
        # 1. running out of positions on the board
        # 2. without having any blank or other player's pieces in a row
        # The current player has won the game.
        self.winner = self.current_player
        raise GameOver(self.winner)

    def check_vertical_line(self) -> None:
        """
        Check if the player has one by looking at
        the column that has a new piece
        """
        #  Get a line of pieces in a column with the one recently added
        line = self.board[self.current_column][: self.current_row + 1]
        self.check_line_for_win(line)

    def get_diagonal_line(self, orientation: str = "right") -> Optional[int]:
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
        diagonal pointing downwards starting with a new piece
        """
        line = self.get_diagonal_line(orientation="right")
        self.check_line_for_win(line)

    def check_left_diagonal_line(self) -> None:
        """
        Check if the player has won by looking at the left
        diagonal pointing downwards starting with a new piece
        """
        line = self.get_diagonal_line(orientation="left")
        self.check_line_for_win(line)

    def check_horizontal_lines(self) -> None:
        """
        Check if the player has won by looking at the horizonal
        line that the new piece has been put in"""

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
    """
    A class to setup the game board and carry out the moves.
    """

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

    def start_game(self) -> None:
        for move in self.get_moves():
            if self.winner is None:
                self.make_move(move)
                self.check_for_wins()
            else:
                # Trying to make an illegal move
                raise GameError(4)

        self.finish_game()

    def make_move(self, move: int) -> None:
        """
        Make a move and mark it on the board.
        """
        column = move - 1
        try:
            # Find the first blank position along the column for next move
            row = next(x for x, psn in enumerate(self.board[column]) if psn is None)
        except StopIteration:
            # Illegal row. The column is already full.
            raise GameError(5)
        except IndexError:
            # Illegal column. Column chosen outside the board
            raise GameError(6)
        else:
            self.current_column = column
            self.current_row = row
            self.total_moves += 1
            self.current_player = next(self.player)
            self.board[column][row] = self.current_player

    def get_moves(self) -> List[int]:
        """A generator which returns next player moves"""
        for next_move in self.file_object:
            next_move = next_move.rstrip("\n")
            try:
                next_move = int(next_move)
            except ValueError:
                # Moves should only be denoted by a digit
                raise GameError(8)

            if next_move <= 0:
                # It doesn't make sense to have a column <= 0
                raise GameError(8)
            else:
                yield next_move

    def finish_game(self) -> None:
        """
        Perform final evaluations at the end
        of the game to determine output code
        """
        if self.winner is None and self.total_moves < self.width * self.height:
            # Game is not finished, but no further moves were made
            raise GameError(3)
        if self.winner is None:
            # Draw
            raise GameOver(0)
        else:
            # Game winner
            raise GameOver(self.winner)


class Game:
    def __init__(self, file_pointer: TextIO) -> None:
        self.file_pointer = file_pointer

    def play(self) -> None:
        header = self.get_file_header()
        width, height, winning_moves = self.parse_header(header)

        self.validate_board_setup(width, height, winning_moves)
        board = GameBoard(width, height, winning_moves, self.file_pointer)
        board.start_game()

    def get_file_header(self) -> str:
        try:
            return next(self.file_pointer).rstrip("\n")
        except (OSError, IOError, UnicodeError):
            # There are some issues with opening or reading the file
            raise GameError(9)

    def parse_header(self, header: str) -> Tuple[int]:
        """
        Given a file header, parse the information
        into board width, height and winning moves.
        """
        try:
            width, height, winning_moves = map(int, header.split(" "))
            return width, height, winning_moves
        except ValueError:
            # File contents do not meet expected format
            raise GameError(8)

    def validate_board_setup(self, width: int, height: int, winning_moves: int) -> None:
        game_specs = (width, height, winning_moves)
        if any(map(lambda x: x <= 0, game_specs)):
            # invalid values in input file
            raise GameError(8)

        if width < winning_moves and height < winning_moves:
            # Illegal game. Game can never be won, because
            # there are not enough rows/columns.
            raise GameError(7)
