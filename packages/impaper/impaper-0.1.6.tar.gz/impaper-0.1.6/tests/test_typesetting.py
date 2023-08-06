from impaper.typesetting import TypeSetting


def test_typesetting():
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
