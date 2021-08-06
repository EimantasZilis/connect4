import io
from pathlib import Path
from typing import List, Tuple, Union
from unittest.mock import MagicMock, Mock, patch

import pytest

from config import GAME_STATUSES
from helpers import ArgParser, show_summary, sliding_window


class TestArgParser:
    @patch("helpers.argparse.ArgumentParser")
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


@patch("sys.stdout", new_callable=io.StringIO)
def test_show_summary_draw(mock_stdout: MagicMock) -> None:
    show_summary("0")
    assert mock_stdout.getvalue().strip() == "Draw"


@pytest.mark.parametrize(
    "player,output", ((player, f"Player {player} won") for player in ("1", "2"))
)
@patch("sys.stdout", new_callable=io.StringIO)
def test_show_summary_game_player_won(
    mock_stdout: MagicMock, player: str, output: str
) -> None:
    show_summary(player)
    assert mock_stdout.getvalue().strip() == output.strip()


@pytest.mark.parametrize(
    "code,output",
    ((x, f"Game Error: {GAME_STATUSES[x]}") for x in map(str, range(3, 10))),
)
@patch("sys.stdout", new_callable=io.StringIO)
def test_show_summary_game_error(
    mock_stdout: MagicMock, code: str, output: str
) -> None:
    show_summary(code)
    assert mock_stdout.getvalue().strip() == output.strip()


@pytest.mark.parametrize("code", (-1, 11, 100, 0, "", "abcd", None))
@patch("sys.stdout", new_callable=io.StringIO)
def test_show_summary_unknown_error(
    mock_stdout: MagicMock, code: Union[int, str]
) -> None:
    show_summary(code)
    assert mock_stdout.getvalue().strip() == f"Unknown Error - code: {code}".strip()
