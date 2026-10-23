import tkinter as tk

from game_logic import CombatGame, GameResult, Phase


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 520


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
        self.root.after(700, self.start_warning)

    def start_warning(self) -> None:
        if not self.game.begin_enemy_warning():
            return
        self.draw()
        self.root.after(900, self.start_attack)

    def start_attack(self) -> None:
        if not self.game.begin_enemy_attack():
            return
        self.draw()
        self.root.after(500, self.resolve_attack)

    def resolve_attack(self) -> None:
        self.game.resolve_enemy_attack(self.cursor_x, self.cursor_y)
        self.draw()
        if self.game.is_over:
            return
        self.root.after(1000, self.start_opening)

    def start_opening(self) -> None:
        if not self.game.begin_vulnerability():
            return
        self.draw()
        self.root.after(900, self.end_opening)

    def end_opening(self) -> None:
        if not self.game.return_to_idle():
            return
        self.draw()
        self.schedule_round()

    def restart(self) -> None:
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
        block = self.game.block_target
        opening = self.game.opening_target
        block_color = "#24463f" if self.game.phase is Phase.ENEMY_ATTACK else "#1e2c38"
        opening_color = "#5b3b28" if self.game.phase is Phase.VULNERABLE else "#1e2c38"
        self.canvas.create_rectangle(
            block.x, block.y, block.x + block.width, block.y + block.height,
            fill=block_color, outline="#55c2a1", width=2,
        )
        self.canvas.create_text(block.x + block.width // 2, block.y + block.height // 2, text="BLOCK\nTARGET", fill="#b9eadb", font=("Segoe UI", 13, "bold"))
        self.canvas.create_rectangle(
            opening.x, opening.y, opening.x + opening.width, opening.y + opening.height,
            fill=opening_color, outline="#e87968", width=2,
        )
        self.canvas.create_text(opening.x + opening.width // 2, opening.y + opening.height // 2, text="ATTACK\nOPENING", fill="#ffd0c7", font=("Segoe UI", 13, "bold"))

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
