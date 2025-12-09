# core/theme_manager.py
class ThemeManager:
    def __init__(self):
        self.theme = {
            "color": "#2381E9",
            "font_family": "",
            "logo": None,
            "mode": "light",   # 'light' или 'dark'
        }

    def apply(self, theme):
        self.theme.update(theme)

    def get(self):
        return self.theme

    def toggle_mode(self):
        self.theme["mode"] = (
            "dark" if self.theme.get("mode") == "light" else "light"
        )
