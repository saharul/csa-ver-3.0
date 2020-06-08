from unittest.mock import mock_open, patch
from max_id_file import get_max_id


def test_max_id_file():
    # pass the desired content as parameter
    m = mock_open(read_data="15")

    with patch("max_id_file.open", m):
        # it does not matter what file path you pass,
        # the file contents are mocked
        assert get_max_id("path/to/file") == int("15")
