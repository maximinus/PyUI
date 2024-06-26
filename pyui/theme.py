from pyui.base import get_asset, TextStyle

DEFAULT_THEME = 'themes/basic_theme.json'


class Theme:
    def __init__(self, path=None):
        # stores current theme
        self.icon = {}
        self.text = {}
        self.color = {}
        self.nine_patch = {}
        if path is not None:
            self.from_json(path)

    def load_default(self):
        self.from_json(DEFAULT_THEME)

    def to_json(self):
        pass

    def from_json(self, theme_path):
        json_data = get_asset(theme_path)
        self.color = json_data['colors']
        self.text = {}
        for key, value in json_data['text'].items():
            self.text[key] = TextStyle.from_json_data(value)
        self.icon = {}
        for key, value in json_data['icons'].items():
            self.icon[key] = get_asset(f'icons/{value}.png')
        self.nine_patch = {}
        for key, value in json_data['nine_patch'].items():
            self.nine_patch[key] = get_asset(f'nine_patch/{value}.png')


THEME = Theme()
