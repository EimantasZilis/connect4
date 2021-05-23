import pytest
from unittest.mock import patch
from pathlib import Path

from pathlib import Path
from typing import List
from constants import status_codes
from connectz import main, ArgParser

BASE_TEST_DIR = Path(__file__).resolve().parent / "test_statuses"


def get_test_files(status: str) -> List[Path]:
    return [
        file
        for file in (BASE_TEST_DIR / status).iterdir()
        if file.is_file()
    ]


class TestStatuses:
    @patch("connectz.ArgParser")
    @pytest.mark.parametrize("status", list(map(str, range(1, 10))))
    def test_files(self, mock_arg_parser, status):
        for file in get_test_files(status):
            mock_arg_parser.get_file.return_value = file
            with pytest.raises(SystemExit) as sys_exit:
                main()
                assert sys_exit.exception.code == status