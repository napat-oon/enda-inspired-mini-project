import tkinter as tk
import time

from game_logic import CombatGame, GameResult, Phase, Target, scaled_target


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 520
WARNING_DURATION = 900
ATTACK_DURATION = 500
OPENING_DURATION = 900
ANIMATION_INTERVAL = 16


class CombatApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Point-and-Click Combat")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(
            root,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            background="#121923",
            highlightthickness=0,
        )
        self.canvas.pack()
        self.game = CombatGame()
        self.cursor_x = 0
        self.cursor_y = 0
        self.restart_button: tk.Button | None = None
        self.round_token = 0
        self.animation_token = 0
        self.animation_progress = 0.0
        self.animation_target: Target | None = None
        self.animation_color = "#f4f1de"
        self.animation_started_at = 0.0
        self.animation_duration = 0

        self.canvas.bind("<Motion>", self.on_motion)
        self.canvas.bind("<Button-1>", self.on_attack)
        self.canvas.bind("<ButtonPress-3>", self.on_block_start)
        self.canvas.bind("<ButtonRelease-3>", self.on_block_end)
        self.draw()
        self.schedule_round()

    def on_motion(self, event: tk.Event) -> None:
        self.cursor_x = event.x
        self.cursor_y = event.y

    def on_attack(self, _event: tk.Event) -> None:
        if self.game.attack(self.cursor_x, self.cursor_y):
            self.draw()
        elif self.game.phase is Phase.VULNERABLE:
            self.draw("Attack missed")

    def on_block_start(self, _event: tk.Event) -> None:
        self.game.set_blocking(True)
        self.draw()

    def on_block_end(self, _event: tk.Event) -> None:
        self.game.set_blocking(False)
        self.draw()

    def schedule_round(self) -> None:
        if self.game.is_over:
            return
        token = self.round_token
        self.root.after(700, lambda: self.start_warning(token))

    def start_warning(self, token: int) -> None:
        if token != self.round_token:
            return
        if not self.game.begin_enemy_warning():
            return
        self.start_animation(self.game.block_target, WARNING_DURATION, "#55c2a1")
        self.draw()
        self.root.after(WARNING_DURATION, lambda: self.start_attack(token))

    def start_attack(self, token: int) -> None:
        if token != self.round_token:
            return
        if not self.game.begin_enemy_attack():
            return
        self.animation_progress = 1.0
        self.draw()
        self.root.after(ATTACK_DURATION, lambda: self.resolve_attack(token))

    def resolve_attack(self, token: int) -> None:
        if token != self.round_token:
            return
        self.game.resolve_enemy_attack(self.cursor_x, self.cursor_y)
        self.draw()
        if self.game.is_over:
            self.animation_token += 1
            return
        self.root.after(1000, lambda: self.start_opening(token))

    def start_opening(self, token: int) -> None:
        if token != self.round_token:
            return
        if not self.game.begin_vulnerability():
            self.game.return_to_idle()
            self.draw()
            self.schedule_round()
            return
        self.start_animation(self.game.opening_target, OPENING_DURATION, "#e87968")
        self.draw()
        self.root.after(OPENING_DURATION, lambda: self.end_opening(token))

    def end_opening(self, token: int) -> None:
        if token != self.round_token:
            return
        if not self.game.return_to_idle():
            return
        self.animation_token += 1
        self.animation_target = None
        self.draw()
        self.schedule_round()

    def restart(self) -> None:
        self.round_token += 1
        self.animation_token += 1
        self.game.restart()
        if self.restart_button is not None:
            self.restart_button.destroy()
            self.restart_button = None
        self.draw()
        self.schedule_round()

    def draw(self, feedback: str = "") -> None:
        self.canvas.delete("all")
        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            28,
            text="POINT-AND-CLICK COMBAT",
            fill="#f4f1de",
            font=("Georgia", 22, "bold"),
        )
        self.draw_health(40, 65, "PLAYER", self.game.player_health, "#55c2a1")
        self.draw_health(560, 65, "ENEMY", self.game.enemy_health, "#e87968")
        self.draw_areas()
        self.draw_phase(feedback)

        if self.game.is_over:
            result_text = {
                GameResult.WON: "YOU WIN",
                GameResult.LOST: "YOU LOSE",
                GameResult.DRAW: "DRAW",
            }[self.game.result]
            self.canvas.create_text(
                WINDOW_WIDTH // 2,
                430,
                text=result_text,
                fill="#f4f1de",
                font=("Georgia", 28, "bold"),
            )
            self.restart_button = tk.Button(
                self.root,
                text="Restart",
                command=self.restart,
                font=("Segoe UI", 11, "bold"),
                relief=tk.FLAT,
                padx=18,
                pady=6,
            )
            self.canvas.create_window(WINDOW_WIDTH // 2, 480, window=self.restart_button)

    def draw_health(self, x: int, y: int, label: str, health: int, color: str) -> None:
        self.canvas.create_text(x, y, anchor="w", text=label, fill="#d8dee9", font=("Segoe UI", 11, "bold"))
        for index in range(self.game.max_health):
            fill = color if index < health else "#313b4a"
            self.canvas.create_rectangle(x + index * 34, y + 22, x + index * 34 + 24, y + 38, fill=fill, outline="")

    def draw_areas(self) -> None:
        if self.game.phase in (Phase.ENEMY_WARNING, Phase.ENEMY_ATTACK):
            target = self.game.block_target
            visible_target = target if self.game.phase is Phase.ENEMY_ATTACK else scaled_target(target, self.animation_progress)
            self.draw_target(visible_target, "#55c2a1", "BLOCK\nTARGET")
        elif self.game.phase is Phase.VULNERABLE:
            target = self.game.opening_target
            visible_target = scaled_target(target, self.animation_progress)
            self.draw_target(visible_target, "#e87968", "ATTACK\nOPENING")

    def draw_target(self, target: Target, color: str, label: str) -> None:
        self.canvas.create_rectangle(
            target.x,
            target.y,
            target.x + target.width,
            target.y + target.height,
            fill="",
            outline=color,
            width=3,
        )
        if target.width > 30 and target.height > 30:
            self.canvas.create_text(
                target.x + target.width / 2,
                target.y + target.height / 2,
                text=label,
                fill=color,
                font=("Segoe UI", 13, "bold"),
            )

    def start_animation(self, target: Target, duration: int, color: str) -> None:
        self.animation_token += 1
        token = self.animation_token
        self.animation_target = target
        self.animation_color = color
        self.animation_progress = 0.0
        self.animation_started_at = time.monotonic()
        self.animation_duration = duration
        self.animate_frame(token)

    def animate_frame(self, token: int) -> None:
        if token != self.animation_token or self.game.is_over or self.animation_target is None:
            return
        elapsed = (time.monotonic() - self.animation_started_at) * 1000
        self.animation_progress = min(1.0, elapsed / self.animation_duration)
        self.draw()
        if self.animation_progress < 1.0:
            self.root.after(ANIMATION_INTERVAL, lambda: self.animate_frame(token))

    def draw_phase(self, feedback: str) -> None:
        phase_text = {
            Phase.IDLE: "Watch for the enemy's next move.",
            Phase.ENEMY_WARNING: "Incoming attack: move to the block target and hold right mouse.",
            Phase.ENEMY_ATTACK: "Block now.",
            Phase.VULNERABLE: "Opening! Move to the attack target and left-click.",
        }[self.game.phase]
        if self.game.blocking and not self.game.is_over:
            phase_text = "Blocking"
        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            365,
            text=feedback or phase_text,
            fill="#f4f1de",
            font=("Segoe UI", 13),
            width=700,
        )


if __name__ == "__main__":
    root = tk.Tk()
    CombatApp(root)
    root.mainloop()
