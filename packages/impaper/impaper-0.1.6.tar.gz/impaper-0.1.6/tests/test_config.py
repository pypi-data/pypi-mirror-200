from impaper.config import Font, Layout, Config


def test_font():
    font = Font()
    assert font.path == "package:///res/sarasa-mono-sc-regular.ttf"


def test_layout():
    layout = Layout()
    assert all(x == 6 for x in layout.margin)


def test_config():
    config = Config()
    assert config.font.path == "package:///res/sarasa-mono-sc-regular.ttf"
    assert config.layout.spacing == 2
