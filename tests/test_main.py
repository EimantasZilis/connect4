from pathlib import Path
from typing import List, Tuple
from unittest.mock import MagicMock, patch

import pytest

from game_solver.config import GameCode
from start_game import ArgParser, main, start_game

BASE_TEST_DIR = Path(__file__).resolve().parent / "sample_games"


@pytest.fixture
def get_files() -> List[Tuple[GameCode, Path]]:
    """Returns a list of tuples with game code and filepath pairs"""
    return [
        (GameCode[folder.name.upper()], file)
        for folder in BASE_TEST_DIR.iterdir()
        for file in folder.iterdir()
        if file.is_file()
    ]


@pytest.mark.parametrize("status,file", get_files())
def test_start_game(status: str, file: Path) -> None:
    assert start_game(file) == status


def test_start_game_file_doesnt_exist() -> None:
    missing_file = BASE_TEST_DIR / "I_don't_exist.txt"
    assert not missing_file.exists()
    assert start_game(missing_file) == GameCode(9)
    assert not missing_file.exists()


@patch("start_game.start_game")
@patch("start_game.show_summary")
@patch.object(ArgParser, "get_path")
@patch.object(ArgParser, "__init__", return_value=None)
def test_main(
    mock_init: MagicMock,
    mock_get_path: MagicMock,
    mock_show_summary: MagicMock,
    mock_start_game: MagicMock,
) -> None:
    status = GameCode.INCOMPLETE_GAME
    filename = Path("some_path")
    mock_get_path.return_value = filename
    mock_start_game.return_value = status

    main()

    mock_start_game.assert_called_once_with(filename)
    mock_show_summary.assert_called_once_with(status)
