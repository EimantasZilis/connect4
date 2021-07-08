from typing import List
from unittest.mock import MagicMock, Mock, call, patch

import pytest

from game import Game, GameBoard, GameChecker, GameError, GameOver

BASE_PATH = "game.GameChecker"


class TestGameChecker:
    @pytest.fixture
    def game_checker(self):
        checker = GameChecker()
        checker.total_moves = 3
        checker.winning_moves = 2
        checker.winner = None
        return checker

    @patch.object(GameChecker, "_check_lines_for_wins")
    def test_check_for_wins_make_checks(
        self, mock_check_lines_for_wins: MagicMock, game_checker: GameChecker
    ) -> None:
        game_checker.check_for_wins()
        mock_check_lines_for_wins.assert_called_once()

    @patch.object(GameChecker, "_check_lines_for_wins")
    def test_check_for_wins_dont_check(
        self, mock_check_lines_for_wins: MagicMock, game_checker: GameChecker
    ) -> None:
        game_checker.total_moves = 2
        game_checker.check_for_wins()
        mock_check_lines_for_wins.assert_not_called()

    @pytest.mark.parametrize(
        "winning_moves,current_player,line",
        [
            (1, 1, []),
            (3, 1, [1, 0]),
            (3, 1, [1, 0, 1]),
            (3, 1, [0, 0, 1]),
            (3, 1, [0, 0, 0]),
            (3, 1, [None, None, None]),
            (3, 1, [None, 1, None]),
            (2, 1, [None, None, 1, None]),
            (2, 1, [1, None, 1, None, 1]),
            (2, 1, [1, None, 1, None, 1, 0, 1]),
            (2, 1, [1, None, 1, None, 0, 0, 0]),
        ],
    )
    def test_check_line_for_win_not_won(
        self,
        winning_moves: int,
        current_player: int,
        line: List[int],
        game_checker: GameChecker,
    ) -> None:
        game_checker.winning_moves = winning_moves
        game_checker.current_player = current_player
        assert game_checker.check_line_for_win(line) == None

    @pytest.mark.parametrize(
        "winning_moves,current_player,line",
        [
            (3, 1, [1, 1, 1]),
            (3, 1, [1, 1, 1, 1]),
            (3, 1, [1, None, 0, 1, 1, 1]),
            (3, 0, [1, 0, 0, 0, 0, 0, 0]),
            (3, 0, [1, 0, 1, 0, None, 0, 0, 0]),
        ],
    )
    def test_check_line_for_win_game_won(
        self,
        winning_moves: int,
        current_player: int,
        line: List[int],
        game_checker: GameChecker,
    ) -> None:
        game_checker.winning_moves = winning_moves
        game_checker.current_player = current_player

        with pytest.raises(GameOver):
            game_checker.check_line_for_win(line)
            assert game_checker.winner == current_player

    @patch.object(GameChecker, "check_line_for_win")
    def test_check_vertical_line(
        self, mock_check_line_for_win: MagicMock, game_checker: GameChecker
    ) -> None:
        game_checker.current_column = 0
        game_checker.current_row = 2
        game_checker.board = [
            [1, 1, 1, None],
            [0, None, None, None],
            [0, None, None, None],
        ]
        game_checker.check_vertical_line()

        line = [1, 1, 1]
        mock_check_line_for_win.assert_called_once_with(line)

    def test_get_diagonal_line_right(self, game_checker: GameChecker) -> None:
        game_checker.current_column = 0
        game_checker.current_row = 3
        game_checker.max_diagonal_length = 3
        game_checker.board = [[1, 0, 1, 0], [0, 1, 0, None], [1, 0, None, None]]

        line = game_checker.get_diagonal_line(orientation="right")
        assert line == [0, 0, 0]

    def test_get_diagonal_line_left(self, game_checker: GameChecker) -> None:
        game_checker.current_column = 2
        game_checker.current_row = 4
        game_checker.max_diagonal_length = 3
        game_checker.board = [
            [1, 0, 1, 0, 1, 0, 0, 1],
            [0, 1, 0, 1, 1, 1, None, None],
            [1, 0, 1, 0, 1, None, None, None],
        ]

        line = game_checker.get_diagonal_line(orientation="left")
        assert line == [1, 1, 1]

    @patch.object(GameChecker, "get_diagonal_line")
    @patch.object(GameChecker, "check_line_for_win")
    def test_check_right_diagonal_line(
        self,
        mock_check_line_for_win: MagicMock,
        mock_get_diagonal_line: MagicMock,
        game_checker: GameChecker,
    ) -> None:
        line = [1, 0, 1, None]
        mock_get_diagonal_line.return_value = line
        game_checker.check_right_diagonal_line()

        mock_get_diagonal_line.assert_called_once_with(orientation="right")
        mock_check_line_for_win.assert_called_once_with(line)

    @patch.object(GameChecker, "get_diagonal_line")
    @patch.object(GameChecker, "check_line_for_win")
    def test_check_left_diagonal_line(
        self,
        mock_check_line_for_win: MagicMock,
        mock_get_diagonal_line: MagicMock,
        game_checker: GameChecker,
    ) -> None:
        line = [1, 0, 1, None]
        mock_get_diagonal_line.return_value = line
        game_checker.check_left_diagonal_line()

        mock_get_diagonal_line.assert_called_once_with(orientation="left")
        mock_check_line_for_win.assert_called_once_with(line)

    @pytest.mark.parametrize(
        "current_player,winning_moves, horizontal_line",
        [
            (1, 1, [1, 0, 1, 0, None]),
            (1, 2, [1, 0, 1, 1, None]),
            (1, 3, [1, 1, 1, 0, None]),
            (1, 4, [0, 1, 1, 1, 1]),
            (1, 5, [1, 1, 1, 1, 1]),
        ],
    )
    def test_check_horizontal_lines_game_won(
        self,
        current_player: int,
        winning_moves: int,
        horizontal_line: List[int],
        game_checker: GameChecker,
    ) -> None:
        width = 5
        height = 3
        game_checker.width = width
        game_checker.height = height
        game_checker.current_player = current_player
        game_checker.winning_moves = winning_moves
        game_checker.current_column = 3
        game_checker.current_row = 2

        game_checker.board = [[None for row in range(height)] for col in range(width)]
        for x, piece in enumerate(horizontal_line):
            game_checker.board[x][2] = piece

        with pytest.raises(GameOver):
            game_checker.check_horizontal_lines()

        assert game_checker.winner == current_player

    @pytest.mark.parametrize(
        "current_player,winning_moves,horizontal_line",
        [
            (1, 1, [0, 0, 0, None, None]),
            (1, 2, [1, 0, 1, 0, None]),
            (1, 3, [0, 0, 1, 0, None]),
            (1, 4, [1, 1, 0, 0, None]),
            (1, 5, [1, 1, 1, 1, 0]),
        ],
    )
    def test_check_horizontal_lines_game_not_won(
        self,
        current_player: int,
        winning_moves: int,
        horizontal_line: List[int],
        game_checker: GameChecker,
    ) -> None:
        width = 5
        height = 3
        game_checker.width = width
        game_checker.height = height
        game_checker.current_player = current_player
        game_checker.winning_moves = winning_moves
        game_checker.current_column = 3
        game_checker.current_row = 2

        game_checker.board = [[None for row in range(height)] for col in range(width)]
        for x, piece in enumerate(horizontal_line):
            game_checker.board[x][2] = piece

        game_checker.check_horizontal_lines()
        assert game_checker.winner == None

    @pytest.mark.parametrize(
        "board,row,column,winning_moves",
        (
            ([[1, 1, 1, None], [0, 1, 0, None], [0, 0, None, None]], 2, 0, 3),
            ([[1, 0, 1, None], [0, 0, 1, None], [1, 0, 1, None]], 2, 2, 3),
            ([[1, 0, 0, None], [0, 0, 1, None], [1, 0, 1, None]], 2, 2, 2),
            ([[1, 0, 1, None], [0, 1, 0, None], [1, 0, 0, None]], 2, 0, 3),
            ([[1, 0, 0, None], [0, 1, 0, None], [1, 0, 1, None]], 2, 2, 3),
        ),
    )
    def test_check_lines_for_wins_game_won(
        self,
        board: List[List[int]],
        row: int,
        column: int,
        winning_moves: int,
        game_checker: GameChecker,
    ) -> None:
        current_player = 1
        game_checker.width = 3
        game_checker.height = 4
        game_checker.max_diagonal_length = 3
        game_checker.winning_moves = winning_moves
        game_checker.current_player = current_player
        game_checker.current_column = column
        game_checker.current_row = row
        game_checker.board = board

        assert game_checker.winner == None
        game_checker._check_lines_for_wins()
        assert game_checker.winner == current_player

    @pytest.mark.parametrize(
        "board,row,column,winning_moves",
        (
            ([[1, 0, 1, None], [0, 1, None, None], [0, 1, None, None]], 2, 0, 3),
            ([[1, 0, 0, 1], [0, 1, 1, None], [1, 0, 0, 1]], 3, 0, 3),
            ([[1, 1, 0, 1], [0, 0, 1, 1], [1, 0, 1, 0]], 3, 2, 3),
            ([[1, 0, 0, 1], [0, 1, 1, 0], [1, 0, 0, 1]], 1, 0, 3),
            ([[None, None, None, None], [0, 1, 0, 1], [1, 0, 1, None]], 3, 1, 3),
        ),
    )
    def test_check_lines_for_wins_not_won(
        self,
        board: List[List[int]],
        row: int,
        column: int,
        winning_moves: int,
        game_checker: GameChecker,
    ) -> None:
        current_player = 1
        game_checker.width = 3
        game_checker.height = 4
        game_checker.max_diagonal_length = 3
        game_checker.winning_moves = winning_moves
        game_checker.current_player = current_player
        game_checker.current_column = column
        game_checker.current_row = row
        game_checker.board = board

        assert game_checker.winner == None
        game_checker._check_lines_for_wins()
        assert game_checker.winner == None


class TestGameBoard:
    @pytest.fixture
    def game_board(self) -> GameBoard:
        width = 3
        height = 4
        winning_moves = 3
        file_object = Mock()
        return GameBoard(width, height, winning_moves, file_object)

    def test_init(self):
        width = 3
        height = 4
        winning_moves = 2
        file_object = Mock()

        board = GameBoard(width, height, winning_moves, file_object)

        assert board.width == width
        assert board.height == height
        assert board.max_diagonal_length == 3
        assert board.file_object == file_object

        assert board.winner == None
        assert board.current_player == None
        assert board.current_column == None
        assert board.current_row == None
        assert board.total_moves == 0

        assert board.board == [
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
        ]

    @patch.object(GameBoard, "make_move")
    @patch.object(GameBoard, "get_moves")
    @patch.object(GameBoard, "finish_game")
    def test_start_game(
        self,
        mock_finish_game: MagicMock,
        mock_get_moves: MagicMock,
        mock_make_move: MagicMock,
        game_board: GameBoard,
    ) -> None:
        moves = [1, 2, 3]
        mock_get_moves.return_value = moves
        game_board.start_game()

        mock_finish_game.assert_called_once()
        assert mock_make_move.call_args_list == [call(move) for move in moves]

    def test_make_move_game_error(self, game_board: GameBoard) -> None:
        game_board.winner = 1
        with pytest.raises(GameError) as exc:
            game_board.make_move(1)

        assert int(str(exc.value)) == 4

    @patch.object(GameBoard, "add_piece")
    @patch.object(GameBoard, "check_for_wins")
    def test_make_move_no_winner(
        self,
        mock_check_for_wins: MagicMock,
        mock_add_piece: MagicMock,
        game_board: GameBoard,
    ) -> None:
        move = 1
        game_board.winner = None
        game_board.make_move(1)

        mock_add_piece.assert_called_once_with(move)
        mock_check_for_wins.assert_called_once()

    def test_add_piece_illegal_row(self, game_board: GameBoard) -> None:
        game_board.board = [[0, 1, 1]]
        with pytest.raises(GameError) as exc:
            game_board.add_piece(1)

        assert int(str(exc.value)) == 5

    def test_add_piece_illegal_column(self, game_board: GameBoard) -> None:
        game_board.board = [[0, 1, 1]]
        with pytest.raises(GameError) as exc:
            game_board.add_piece(2)

        assert int(str(exc.value)) == 6

    def test_add_piece(self, game_board: GameBoard) -> None:
        game_board.board = [[1, 2, None]]

        assert game_board.current_column == None
        assert game_board.current_row == None
        assert game_board.total_moves == 0
        assert game_board.current_player == None

        game_board.add_piece(1)

        assert game_board.current_column == 0
        assert game_board.current_row == 2
        assert game_board.total_moves == 1
        assert game_board.board[0][2] == 1

    def test_get_moves(self, game_board: GameBoard) -> None:
        vals = range(1, 6)
        game_board.file_object = [f"{x}\n" for x in vals]
        assert list(game_board.get_moves()) == list(vals)

    def test_get_moves_not_digit(self, game_board: GameBoard) -> None:
        game_board.file_object = [f"{x}\n" for x in (1, 2, 3, "a")]
        with pytest.raises(GameError) as exc:
            list(game_board.get_moves())
        assert int(str(exc.value)) == 8

    def test_get_moves_0_value(self, game_board: GameBoard) -> None:
        game_board.file_object = [f"{x}\n" for x in (1, 2, 0, 3)]
        with pytest.raises(GameError) as exc:
            list(game_board.get_moves())
        assert int(str(exc.value)) == 8

    def test_get_moves_negative_value(self, game_board: GameBoard) -> None:
        game_board.file_object = [f"{x}\n" for x in (1, 2, 3, -1)]
        with pytest.raises(GameError) as exc:
            list(game_board.get_moves())
        assert int(str(exc.value)) == 8

    def test_finish_game_not_finished(self, game_board: GameBoard) -> None:
        game_board.winner = None
        game_board.total_moves = 7
        game_board.width = 4
        game_board.height = 2

        with pytest.raises(GameError) as exc:
            game_board.finish_game()

        assert int(str(exc.value)) == 3

    def test_finish_game_draw(self, game_board: GameBoard) -> None:
        game_board.winner = None
        game_board.total_moves = 8
        game_board.width = 4
        game_board.height = 2

        with pytest.raises(GameOver) as exc:
            game_board.finish_game()

        assert int(str(exc.value)) == 0

    def test_finish_game_won(self, game_board: GameBoard) -> None:
        winner = 1
        game_board.winner = winner
        game_board.total_moves = 8
        game_board.width = 4
        game_board.height = 2

        with pytest.raises(GameOver) as exc:
            game_board.finish_game()

        assert int(str(exc.value)) == winner


class TestGame:
    @pytest.fixture
    def file_object(self) -> MagicMock:
        return Mock()

    @pytest.fixture
    def game(self, file_object: MagicMock) -> None:
        return Game(file_object)

    def test_init(self) -> None:
        file_pointer = Mock()
        game = Game(file_pointer)
        assert game.file_pointer == file_pointer

    @patch.object(Game, "initialise")
    def test_play_game_not_finished(
        self, mock_initialise: MagicMock, game: Game
    ) -> None:
        assert game.play() == None
        mock_initialise.assert_called_once()

    @pytest.mark.parametrize("exception", (GameError, GameError))
    @patch.object(Game, "initialise")
    def test_play_game_not_finished(
        self, mock_initialise: MagicMock, exception, game: Game
    ) -> None:
        status = 1
        mock_initialise.side_effect = exception(status)
        game_status = game.play()

        mock_initialise.assert_called_once()
        assert game_status == str(status)
