from typing import List
from unittest.mock import MagicMock, patch

import pytest

from game import GameChecker, GameOver

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
    def test_check_for_wins_make_checks(
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
    def test_check_line_for_win_game_has_been_won(
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

    @patch.object(GameChecker, "check_vertical_line")
    def test_check_lines_for_wins_vertical_line_win(
        self,
        mock_check_vertical_line: MagicMock,
        game_checker: GameChecker,
    ) -> None:
        winner = "1"
        mock_check_vertical_line.side_effect = GameOver(winner)

        assert game_checker.winner == None
        game_checker._check_lines_for_wins()
        assert str(game_checker.winner) == winner

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
    def test_check_lines_for_wins_all_scenarios(
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

    @patch.object(GameChecker, "check_vertical_line")
    @patch.object(GameChecker, "check_left_diagonal_line")
    @patch.object(GameChecker, "check_right_diagonal_line")
    @patch.object(GameChecker, "check_horizontal_lines")
    def test_check_lines_for_wins_player_1_won(
        self,
        mock_check_horizontal_lines: MagicMock,
        mock_check_right_diagonal_line: MagicMock,
        mock_check_left_diagonal_line: MagicMock,
        mock_check_vertical_line: MagicMock,
        game_checker: GameChecker,
    ) -> None:
        winner = "1"
        mock_check_vertical_line.side_effect = GameOver(winner)

        assert game_checker.winner == None
        game_checker._check_lines_for_wins()
        assert str(game_checker.winner) == winner

    @patch.object(GameChecker, "check_vertical_line")
    @patch.object(GameChecker, "check_left_diagonal_line")
    @patch.object(GameChecker, "check_right_diagonal_line")
    @patch.object(GameChecker, "check_horizontal_lines")
    def test_check_lines_for_wins_noone_won(
        self,
        mock_check_horizontal_lines: MagicMock,
        mock_check_right_diagonal_line: MagicMock,
        mock_check_left_diagonal_line: MagicMock,
        mock_check_vertical_line: MagicMock,
        game_checker: GameChecker,
    ) -> None:
        assert game_checker.winner == None
        game_checker._check_lines_for_wins()
        assert game_checker.winner == None
