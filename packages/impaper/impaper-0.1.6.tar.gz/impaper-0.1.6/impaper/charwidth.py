"""计算字符宽度"""
from functools import lru_cache
from typing import Literal

__all__ = ("char_width", "string_width")


# GENERATED DATA
# generated from
# http://www.unicode.org/Public/4.0-Update/EastAsianWidth-4.0.0.txt

__WIDTHS = [
    (126, 1),
    (159, 0),
    (687, 1),
    (710, 0),
    (711, 1),
    (727, 0),
    (733, 1),
    (879, 0),
    (1154, 1),
    (1161, 0),
    (4347, 1),
    (4447, 2),
    (7467, 1),
    (7521, 0),
    (8369, 1),
    (8426, 0),
    (9000, 1),
    (9002, 2),
    (11021, 1),
    (12350, 2),
    (12351, 1),
    (12438, 2),
    (12442, 0),
    (19893, 2),
    (19967, 1),
    (55203, 2),
    (63743, 1),
    (64106, 2),
    (65039, 1),
    (65059, 0),
    (65131, 2),
    (65279, 1),
    (65376, 2),
    (65500, 1),
    (65510, 2),
    (120831, 1),
    (262141, 2),
    (1114109, 1),
]


def char_width(c: str) -> Literal[0, 1, 2]:
    """
    计算字符的宽度：
    + 零宽字符：0
    + 英文字母、标点等字符：1
    + 汉字等字符：2
    """
    o = ord(c)
    if o == 0xE or o == 0xF:
        return 0
    for num, wid in __WIDTHS:
        if o <= num:
            return wid
    return 1


@lru_cache(typed=True)
def string_width(s: str) -> int:
    """计算字符串的宽度"""
    return sum(char_width(c) for c in s)
