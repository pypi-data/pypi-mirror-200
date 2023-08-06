import exrex
import pytest

from impaper.charwidth import char_width, string_width


@pytest.mark.parametrize("char", list(exrex.generate("[a-zA-Z]")))
def test_ascii_alphabet(char):
    assert char_width(char) == 1


@pytest.mark.parametrize("char", list(exrex.generate("[你好世界]")))
def test_chinese_alphabet(char):
    assert char_width(char) == 2


@pytest.mark.parametrize(
    "s, exp",
    [
        ("abc", 3),
        ("abc你好", 7),
        ("你好世界", 8),
    ],
)
def test_string(s, exp):
    assert exp == string_width(s)
