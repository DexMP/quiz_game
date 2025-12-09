# core/theme_manager.py
class ThemeManager:
    def __init__(self):
        self.theme = {"color": "#2381E9", "font_family": "", "logo": None}

    def apply(self, theme):
        self.theme.update(theme)

    def get(self):
        return self.theme
