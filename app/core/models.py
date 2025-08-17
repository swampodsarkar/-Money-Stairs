from dataclasses import dataclass


@dataclass
class Player:
    x: float
    y: float
    radius: float = 12.0
    speed: float = 280.0
    aim_angle: float = 0.0


@dataclass
class Enemy:
    x: float
    y: float
    vx: float
    vy: float
    radius: float = 10.0