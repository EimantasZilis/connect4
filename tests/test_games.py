import os
import pytest
from collections import defaultdict
from unittest.mock import patch
from pathlib import Path

from pathlib import Path
from typing import List
from connectz import main, ArgParser

BASE_TEST_DIR = Path(__file__).resolve().parent / "test_statuses"

def get_files():
    test_runs = [
        (folder.name, file)
        for folder in BASE_TEST_DIR.iterdir()
        for file in folder.iterdir()
        if file.is_file()
    ]
    return test_runs

class TestStatuses:
    
    @pytest.mark.parametrize("status,file", get_files())
    @patch.object(ArgParser, "__init__", return_value=None)
    @patch.object(ArgParser, "get_file")
    def test_file(self, mock_get_file, mock_init, status, file):
        mock_get_file.return_value = file
        with pytest.raises(SystemExit) as sys_exit:
            main()
        assert sys_exit.value.code == status

    @patch.object(ArgParser, "__init__", return_value=None)
    @patch.object(ArgParser, "get_file")
    def test_non_existent_file(self, mock_get_file, mock_init):
        missing_file = BASE_TEST_DIR / "I_don't_exist.txt"
        assert not missing_file.exists()

        mock_get_file.return_value = missing_file
        with pytest.raises(SystemExit) as sys_exit:
            main()
        assert sys_exit.value.code == "9"