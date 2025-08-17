from dataclasses import dataclass


@dataclass
class AppConfig:
    app_title: str = "Practice Panel"
    width: int = 1100
    height: int = 720
    appearance_mode: str = "Dark"  # Options: "System", "Light", "Dark"
    color_theme: str = "blue"       # Options: "blue", "dark-blue", "green"
    sidebar_width: int = 320