from impaper.draw import SimpleTextDrawer
from impaper.config import Config
from impaper.typesetting import TypeSettingConfig

def test_dynamic_config():
    x = SimpleTextDrawer()
    assert id(x.conf.typesetting) == id(x.ts.conf)
    assert x.ts.conf.line_width == 48
    x.conf = Config(typesetting=TypeSettingConfig(line_width=100))
    assert id(x.conf.typesetting) == id(x.ts.conf)
    assert x.ts.conf.line_width == 100
