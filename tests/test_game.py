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
