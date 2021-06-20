from pathlib import Path
from unittest.mock import patch

import pytest

from main import ArgParser, main, start_game

BASE_TEST_DIR = Path(__file__).resolve().parent / "sample_files"


def get_files():
    test_files = [
        (folder.name, file)
        for folder in BASE_TEST_DIR.iterdir()
        for file in folder.iterdir()
        if file.is_file()
    ]
    return test_files


@pytest.mark.parametrize("status,file", get_files())
def test_start_game(status, file) -> None:
    assert start_game(file) == status


def test_start_game_file_doesnt_exist() -> None:
    missing_file = BASE_TEST_DIR / "I_don't_exist.txt"
    assert not missing_file.exists()
    assert start_game(missing_file) == "9"
    assert not missing_file.exists()


@patch("main.start_game")
@patch("main.show_summary")
@patch.object(ArgParser, "get_path")
@patch.object(ArgParser, "__init__", return_value=None)
def test_main(mock_init, mock_get_path, mock_show_summary, mock_start_game) -> None:
    status = "3"
    filename = Path("some_path")
    mock_get_path.return_value = filename
    mock_start_game.return_value = status

    main()

    mock_start_game.assert_called_once_with(filename)
    mock_show_summary.assert_called_once_with(status)
