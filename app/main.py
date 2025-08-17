from app.core.config import AppConfig
from app.ui.app import Application


def run() -> None:
    """Start the GUI application with default configuration."""
    config = AppConfig(
        app_title="Practice Panel",
        width=1100,
        height=720,
        appearance_mode="Dark",
        color_theme="blue",
        sidebar_width=320,
    )
    app = Application(config)
    app.mainloop()