import math
import random
from typing import List

from app.core.models import Player, Enemy


class Simulation:
    """Safe, self-contained sandbox simulation.

    Tracks a player and a set of moving enemies inside a rectangular area.
    No integration with external processes or games.
    """

    def __init__(self, play_width: int = 760, play_height: int = 660) -> None:
        self.area_width = max(200, int(play_width))
        self.area_height = max(200, int(play_height))
        self.running: bool = True

        # Aim
        self.auto_aim_enabled: bool = True
        self.aim_speed_rads_per_sec: float = 2.2
        self.hit_flash_timer: float = 0.0

        # Entities
        self.player: Player = Player(x=self.area_width / 2.0, y=self.area_height / 2.0)
        self.enemies: List[Enemy] = []
        self._spawn_enemies(9)

    # ----- Public configuration API -----
    def set_area_size(self, width: int, height: int) -> None:
        self.area_width = max(200, int(width))
        self.area_height = max(200, int(height))
        # Clamp player into new bounds
        self.player.x = _clamp(self.player.x, self.player.radius, self.area_width - self.player.radius)
        self.player.y = _clamp(self.player.y, self.player.radius, self.area_height - self.player.radius)

    def set_auto_aim_enabled(self, enabled: bool) -> None:
        self.auto_aim_enabled = bool(enabled)

    def set_aim_speed(self, rads_per_sec: float) -> None:
        self.aim_speed_rads_per_sec = max(0.0, float(rads_per_sec))

    def reset(self) -> None:
        self.player = Player(x=self.area_width / 2.0, y=self.area_height / 2.0)
        self.enemies.clear()
        self._spawn_enemies(9)
        self.hit_flash_timer = 0.0

    # ----- Update loop -----
    def update(self, dt: float) -> None:
        if dt <= 0:
            return

        # Move enemies and bounce at edges
        for e in self.enemies:
            e.x += e.vx * dt
            e.y += e.vy * dt
            if e.x < e.radius:
                e.x = e.radius
                e.vx = abs(e.vx)
            if e.x > self.area_width - e.radius:
                e.x = self.area_width - e.radius
                e.vx = -abs(e.vx)
            if e.y < e.radius:
                e.y = e.radius
                e.vy = abs(e.vy)
            if e.y > self.area_height - e.radius:
                e.y = self.area_height - e.radius
                e.vy = -abs(e.vy)

        # Auto-aim towards nearest enemy
        if self.auto_aim_enabled and self.enemies:
            px, py = self.player.x, self.player.y
            nearest = None
            nearest_d2 = float("inf")
            for e in self.enemies:
                dx = e.x - px
                dy = e.y - py
                d2 = dx * dx + dy * dy
                if d2 < nearest_d2:
                    nearest_d2 = d2
                    nearest = e
            if nearest is not None:
                target_angle = math.atan2(nearest.y - py, nearest.x - px)
                max_delta = self.aim_speed_rads_per_sec * dt
                self.player.aim_angle = _approach_angle(self.player.aim_angle, target_angle, max_delta)

                # Simple feedback when close to target at close range
                if nearest_d2 < 90.0 * 90.0 and abs(_angle_difference(self.player.aim_angle, target_angle)) < 0.09:
                    self.hit_flash_timer = 0.15

        # Decay flash timer
        if self.hit_flash_timer > 0.0:
            self.hit_flash_timer = max(0.0, self.hit_flash_timer - dt)

    # ----- Internals -----
    def _spawn_enemies(self, count: int) -> None:
        for _ in range(count):
            x = random.uniform(50, self.area_width - 50)
            y = random.uniform(50, self.area_height - 50)
            speed = random.uniform(60.0, 140.0)
            angle = random.uniform(0.0, 2.0 * math.pi)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            self.enemies.append(Enemy(x=x, y=y, vx=vx, vy=vy))


def _clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def _angle_difference(a: float, b: float) -> float:
    return (b - a + math.pi) % (2.0 * math.pi) - math.pi


def _approach_angle(current: float, target: float, max_delta: float) -> float:
    diff = _angle_difference(current, target)
    if abs(diff) <= max_delta:
        return target
    return current + max_delta * (1.0 if diff > 0.0 else -1.0)