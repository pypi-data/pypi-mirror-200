"""简单的文字排版引擎"""
from typing import TYPE_CHECKING, Union
from .charwidth import char_width, string_width
from .config import TypeSettingConfig

if TYPE_CHECKING:
    from .draw import TextDrawer


class TypeSetting:
    """简单的文本排版引擎，计算文本折行，可以修改此对象的一些属性：

    + `line_width`: 行宽度，控制折行位置，默认 48
    + `indentation`: 缩进符，控制折行后在新行首添加的符号，默认两个空格

    ```py
    ts = TypeSetting()
    ts.conf.line_width = 40
    ts.conf.indentation = ">>>"
    text = "1234567890" * 9
    lines = ts.wrap_text(text)
    assert lines == [
        "1234567890123456789012345678901234567890",
        ">>>1234567890123456789012345678901234567",
        ">>>8901234567890",
    ]
    ```
    """

    __conf: TypeSettingConfig
    __caller: "TextDrawer"

    @property
    def conf(self) -> TypeSettingConfig:
        if self.__caller:
            return self.__caller.conf.typesetting
        else:
            return self.__conf

    @conf.setter
    def _set_conf(self, conf: TypeSettingConfig):
        self.__conf = conf

    # 缩进符号的宽度
    @property
    def indent_size(self) -> int:
        return string_width(self.conf.indentation)

    def __init__(self, caller: "TextDrawer" = None) -> None:
        if caller:
            self.__caller = caller
        else:
            self.__caller = None
            self.__conf = TypeSettingConfig()
        pass

    def wrap_text(self, txt: str) -> list[str]:
        "根据折行规则给文本换行、折行，不保留换行符"
        # 字符序号 => 换行/折行（1, 2)
        newline = 1
        wrapline = 2
        signs = {}

        # 当前行宽度
        width = 0
        # 给文本打上换行、折行标记
        for i, c in enumerate(txt):
            if c == "\n":
                signs[i] = newline
                width = 0
                continue
            cw = char_width(c)
            if width + cw > self.conf.line_width:
                signs[i] = wrapline
                # 折行时有缩进
                width = self.indent_size + 1
                continue
            width += cw

        # 根据换行、折行标记将文本拆分
        lines = []
        cursor = 0
        need_wrap = False
        for seq, sign in signs.items():
            if sign == newline:
                if need_wrap:
                    lines.append(self.conf.indentation + txt[cursor:seq])
                    need_wrap = False
                else:
                    lines.append(txt[cursor:seq])
                cursor = seq + 1  # 忽略换行符
            elif sign == wrapline:
                if need_wrap:
                    lines.append(self.conf.indentation + txt[cursor:seq])
                else:
                    lines.append(txt[cursor:seq])
                cursor = seq
                need_wrap = True
        lastline = txt[cursor:]
        if lastline:
            if need_wrap:
                lines.append(self.conf.indentation + txt[cursor:])
                need_wrap = False
            else:
                lines.append(txt[cursor:])
        return lines
