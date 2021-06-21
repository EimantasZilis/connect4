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
