import io
from pathlib import Path
from typing import List, Tuple, Union
from unittest.mock import MagicMock, Mock, patch

import pytest

from game_solver.config import GAME_OUTPUT_MESSAGES, GameCode
from game_solver.helpers import ArgParser, show_summary, sliding_window


class TestArgParser:
    @patch("game_solver.helpers.argparse.ArgumentParser")
    def test_init(self, mock_arg_parser: MagicMock) -> None:
        arguments = "yes"
        mock_parser = Mock()
        mock_parser.parse_args.return_value = arguments
        mock_arg_parser.return_value = mock_parser

        arg_parser = ArgParser()
        mock_parser.add_argument.assert_called_once()
        mock_parser.parse_args.assert_called_once()
        assert arg_parser.args == arguments

    @patch.object(ArgParser, "__init__", return_value=None)
    def test_get_path(self, mock_init: MagicMock) -> None:
        path = "/random/path"
        arg_parser = ArgParser()
        arg_parser.args = Mock()
        arg_parser.args.filename = path
        assert arg_parser.get_path() == Path(path)


@pytest.mark.parametrize(
    "iterable,window_size,expected_windows",
    [
        ([1, 2, 3, 4], 1, [(1,), (2,), (3,), (4,)]),
        ([1, 2, 3, 4], 2, [(1, 2), (2, 3), (3, 4)]),
        ([1, 2, 3, 4], 3, [(1, 2, 3), (2, 3, 4)]),
        ([1, 2, 3, 4], 4, [(1, 2, 3, 4)]),
    ],
)
def test_sliding_window(
    iterable: List[int], window_size: int, expected_windows: List[Tuple[int]]
):
    assert list(sliding_window(iterable, window_size)) == expected_windows


@pytest.mark.parametrize("status", (status for status in GameCode))
@patch("sys.stdout", new_callable=io.StringIO)
def test_show_summary_game_player_won(mock_stdout: MagicMock, status: GameCode) -> None:
    show_summary(status)
    assert mock_stdout.getvalue().strip() == GAME_OUTPUT_MESSAGES[status]


@pytest.mark.parametrize("code", (-1, 11, 100, "", "abcd", None, "1"))
def test_show_summary_invalid_code(code: Union[int, str]) -> None:
    with pytest.raises(KeyError):
        show_summary(code)
