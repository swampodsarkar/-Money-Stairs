import tkinter as tk

try:
    import customtkinter as ctk
except ImportError as e:
    raise SystemExit(
        "Missing dependency: customtkinter. Install with: pip install customtkinter"
    ) from e


class PlayfieldView(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, corner_radius=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.on_size_changed = None  # type: ignore

        # Canvas for drawing
        self.canvas = tk.Canvas(self, bg="#0f1115", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<Configure>", self._on_resize)

    # ----- Drawing -----
    def draw(self, simulation) -> None:  # keep loosely coupled to avoid import cycles
        c = self.canvas
        width = c.winfo_width()
        height = c.winfo_height()

        c.delete("all")

        # Background
        c.create_rectangle(0, 0, width, height, fill="#0f1115", outline="")

        # Border
        c.create_rectangle(6, 6, width - 6, height - 6, outline="#2a2f3a", width=2)

        # Enemies
        for e in getattr(simulation, "enemies", []):
            r = getattr(e, "radius", 10.0)
            c.create_oval(e.x - r, e.y - r, e.x + r, e.y + r, fill="#e74c3c", outline="")

        # Player
        player = getattr(simulation, "player", None)
        if player is not None:
            pr = getattr(player, "radius", 12.0)
            px = getattr(player, "x", width / 2)
            py = getattr(player, "y", height / 2)
            aim_angle = getattr(player, "aim_angle", 0.0)

            # Aim line
            ax = px + 72 * __import__("math").cos(aim_angle)
            ay = py + 72 * __import__("math").sin(aim_angle)
            c.create_line(px, py, ax, ay, fill="#55d0ff", width=3)

            c.create_oval(px - pr, py - pr, px + pr, py + pr, fill="#18b7ff", outline="#9be8ff")

        # HUD
        c.create_text(14, 12, text="Sandbox • No game interaction", anchor="w", fill="#7c8597", font=("Segoe UI", 10))

        # Flash feedback
        timer = float(getattr(simulation, "hit_flash_timer", 0.0))
        if timer > 0.0:
            c.create_rectangle(0, 0, width, height, fill="#ffffff", outline="", stipple="gray25")
            c.create_text(width // 2, 36, text="Headshot!", fill="#ffe06b", font=("Segoe UI", 20, "bold"))

    # ----- Events -----
    def _on_resize(self, event) -> None:
        if callable(self.on_size_changed):
            self.on_size_changed(int(event.width), int(event.height))