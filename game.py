from itertools import cycle
from typing import List, Optional, TextIO, Tuple

from helpers import sliding_window


class GameOver(Exception):
    """
    An exception to indicate that the game has been completed.
    This can only be achieved if the game has been won by one
    of the players or if there is a draw.
    """


class GameError(Exception):
    """An exception to indicate that there was an error in the game"""


class GameChecker:
    """
    A class for checking if the game has been won.
    It looks at all lines around a recent piece and
    checks if there are any lines that have a winning
    number of pieces belonging to the same player.
    """

    @property
    def first_column(self) -> int:
        """
        Get the first column (on the left) that should be checked
        for wins based on current piece.
        """
        if (first_col := self.current_column - self.winning_moves) < 0:
            # The expected first column would be outside the board on the left.
            # Return the actual first column on the board
            first_col = 0
        return first_col

    @property
    def last_column(self) -> int:
        """
        Get the last column (on the right) that should be checked
        for wins based on current piece.
        """
        if (last_col := self.current_column + self.winning_moves) > self.width:
            # The expected last column would be on the outside the board
            # on the right. Return the actual last column on the board.
            last_col = self.width
        return last_col

    @property
    def first_row(self) -> int:
        """
        Get the first row (at the bottom) that should be checked
        for wins based on current piece.
        """
        if (first_row := self.current_row - self.winning_moves) < 0:
            # The expected first row would be on the outside the board
            # at the bottom. Return the actual first row on the board.
            first_row = 0
        return first_row

    @property
    def last_row(self) -> int:
        """
        Get the last row (at the top) that should be checked
        for wins based on current piece.
        """
        if (last_row := self.current_row + self.winning_moves) > self.height:
            # The expected last row would be on the outside the board
            # at the top. Return the actual last row on the board.
            last_row = self.height
        return last_row

    def check_for_wins(self) -> None:
        """Check if the game has been won"""
        if self.total_moves >= 2 * self.winning_moves - 1:
            # Only start checking for wins if the first player has
            # managed to put the lowest possible winning moves
            self._check_lines_for_wins()

    def check_line_for_win(self, line: List[int]) -> None:
        """Check if the current player has won based on a given line"""
        if len(line) < self.winning_moves:
            # The line isn't long enough to be able to win
            return

        for offset in range(1, self.winning_moves + 1):
            # Loop backwards through line positions starting
            # from the piece that was added in this turn.
            # Only check the winning number of moves, because
            # others have already been checked previously

            if line[-offset] != self.current_player:
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

        row = [
            self.board[column][self.current_row]
            for column in range(self.first_column, self.last_column)
        ]

        # Get every possible line of length self.winning_moves
        # by applying a slidng window to the row
        for line in sliding_window(row, self.winning_moves):
            self.check_line_for_win(line)

    def check_left_diagonal_upper_line(self) -> None:
        """
        Check if the player has won by looking at the left
        diagonal pointing upwards starting with a new piece
        """

        # If the board width is bigger than the number of winning
        # moves required going upwards, there is more than one way
        # to build a line diagonally. Apply a sliding window along
        # the left diagonal to find  every possible line. Check if
        # it has a winning combination.

        row = [
            self.board[col][row]
            for col, row in zip(
                reversed(range(self.first_column, self.last_column)),
                range(self.first_row, self.last_row),
            )
        ]
        for line in sliding_window(row, self.winning_moves):
            self.check_line_for_win(line)

    def check_right_diagonal_upper_line(self) -> None:
        """
        Check if the player has won by looking at the right
        diagonal pointing upwards starting with a new piece
        """

        # Similar to check_left_diagonal_upper_line, apply a sliding
        # window to check all possible lines.

        row = [
            self.board[col][row]
            for col, row in zip(
                range(self.first_column, self.last_column),
                range(self.first_row, self.last_row),
            )
        ]
        for line in sliding_window(row, self.winning_moves):
            self.check_line_for_win(line)

    def _check_lines_for_wins(self) -> None:
        """Check if the game has been won"""
        try:
            self.check_vertical_line()
            self.check_left_diagonal_line()
            self.check_right_diagonal_line()
            self.check_horizontal_lines()
            self.check_left_diagonal_upper_line()
            self.check_right_diagonal_upper_line()
        except GameOver as e:
            self.winner = int(str(e))


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
        """
        Start the game and make moves until the game is
        finished or until the there is an error.
        """
        for move in self.get_moves():
            self.make_move(move)
        self.finish_game()

    def make_move(self, move: int) -> None:
        """
        Make a move by adding a piece and checking for wins
        """
        if self.winner is None:
            self.add_piece(move)
            self.check_for_wins()
        else:
            # Trying to make an illegal move
            raise GameError(4)

    def add_piece(self, move: int) -> None:
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
        elif self.winner is None:
            # Draw
            raise GameOver(0)
        else:
            # Game winner
            raise GameOver(self.winner)


class Game:
    def __init__(self, file_pointer: TextIO) -> None:
        self.file_pointer = file_pointer

    def play(self) -> None:
        try:
            self.initialise()
        except (GameOver, GameError) as game_status:
            # Change game_status exception object into a string
            return str(game_status)

    def initialise(self) -> None:
        header = next(self.file_pointer).rstrip("\n")
        width, height, winning_moves = self.parse_header(header)

        self.validate_board_setup(width, height, winning_moves)
        board = GameBoard(width, height, winning_moves, self.file_pointer)
        board.start_game()

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
