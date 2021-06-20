from pathlib import Path
from typing import List, Tuple
from unittest.mock import MagicMock, Mock, patch

import pytest

from helpers import ArgParser, sliding_window


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
    iterable: List[int], window_size: int, expected_windows: Tuple[List[int]]
):
    assert list(sliding_window(iterable, window_size)) == expected_windows
