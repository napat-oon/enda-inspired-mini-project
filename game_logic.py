from dataclasses import dataclass
from enum import Enum, auto


class GameResult(Enum):
    PLAYING = auto()
    WON = auto()
    LOST = auto()
    DRAW = auto()


class Phase(Enum):
    IDLE = auto()
    ENEMY_WARNING = auto()
    ENEMY_ATTACK = auto()
    VULNERABLE = auto()


@dataclass(frozen=True)
class Target:
    x: int
    y: int
    width: int
    height: int

    def contains(self, cursor_x: int, cursor_y: int) -> bool:
        return (
            self.x <= cursor_x <= self.x + self.width
            and self.y <= cursor_y <= self.y + self.height
        )


@dataclass
class CombatGame:
    max_health: int = 3
    damage: int = 1
    block_target: Target = Target(80, 210, 180, 140)
    opening_target: Target = Target(540, 210, 180, 140)

    def __post_init__(self) -> None:
        self.restart()

    def restart(self) -> None:
        self.player_health = self.max_health
        self.enemy_health = self.max_health
        self.result = GameResult.PLAYING
        self.phase = Phase.IDLE
        self.blocking = False
        self.last_block_success = False
        self.last_attack_success = False

    @property
    def is_over(self) -> bool:
        return self.result is not GameResult.PLAYING

    def set_blocking(self, is_blocking: bool) -> None:
        if not self.is_over:
            self.blocking = is_blocking

    def begin_enemy_warning(self) -> bool:
        if self.is_over:
            return False
        self.phase = Phase.ENEMY_WARNING
        self.last_block_success = False
        return True

    def begin_enemy_attack(self) -> bool:
        if self.is_over or self.phase is not Phase.ENEMY_WARNING:
            return False
        self.phase = Phase.ENEMY_ATTACK
        return True

    def resolve_enemy_attack(self, cursor_x: int, cursor_y: int) -> bool:
        if self.is_over or self.phase is not Phase.ENEMY_ATTACK:
            return False

        self.last_block_success = self.blocking and self.block_target.contains(
            cursor_x, cursor_y
        )
        if not self.last_block_success:
            self.player_health = max(0, self.player_health - self.damage)

        self._update_result()
        return self.last_block_success

    def resolve_simultaneous_exchange(
        self,
        block_cursor_x: int,
        block_cursor_y: int,
        attack_cursor_x: int,
        attack_cursor_y: int,
    ) -> tuple[bool, bool]:
        if self.is_over or self.phase is not Phase.ENEMY_ATTACK:
            return False, False

        self.last_block_success = self.blocking and self.block_target.contains(
            block_cursor_x, block_cursor_y
        )
        if not self.last_block_success:
            self.player_health = max(0, self.player_health - self.damage)

        self.last_attack_success = (
            not self.blocking and self.opening_target.contains(attack_cursor_x, attack_cursor_y)
        )
        if self.last_attack_success:
            self.enemy_health = max(0, self.enemy_health - self.damage)

        self._update_result()
        return self.last_block_success, self.last_attack_success

    def begin_vulnerability(self) -> bool:
        if self.is_over:
            return False
        self.phase = Phase.VULNERABLE
        self.last_attack_success = False
        return True

    def attack(self, cursor_x: int, cursor_y: int) -> bool:
        if self.is_over or self.phase is not Phase.VULNERABLE or self.blocking:
            return False

        self.last_attack_success = self.opening_target.contains(cursor_x, cursor_y)
        if self.last_attack_success:
            self.enemy_health = max(0, self.enemy_health - self.damage)
            self._update_result()
        return self.last_attack_success

    def return_to_idle(self) -> bool:
        if self.is_over:
            return False
        self.phase = Phase.IDLE
        self.last_block_success = False
        self.last_attack_success = False
        return True

    def _update_result(self) -> None:
        if self.player_health == 0 and self.enemy_health == 0:
            self.result = GameResult.DRAW
        elif self.enemy_health == 0:
            self.result = GameResult.WON
        elif self.player_health == 0:
            self.result = GameResult.LOST
