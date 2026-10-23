import random
from dataclasses import dataclass, field
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
    x: float
    y: float
    width: float
    height: float

    def contains(self, cursor_x: float, cursor_y: float) -> bool:
        return (
            self.x <= cursor_x <= self.x + self.width
            and self.y <= cursor_y <= self.y + self.height
        )


def scaled_target(target: Target, progress: float) -> Target:
    progress = max(0.0, min(1.0, progress))
    width = target.width * progress
    height = target.height * progress
    return Target(
        target.x + (target.width - width) / 2,
        target.y + (target.height - height) / 2,
        width,
        height,
    )


@dataclass
class CombatGame:
    max_health: int = 3
    damage: int = 1
    area_width: int = 800
    area_height: int = 520
    target_width: int = 180
    target_height: int = 140
    required_blocks: int = 5
    rng: random.Random = field(default_factory=random.Random, repr=False)
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
        self.successful_blocks = 0
        self.vulnerability_hit = False
        self.last_block_success = False
        self.last_attack_success = False
        self.randomize_targets()

    @property
    def is_over(self) -> bool:
        return self.result is not GameResult.PLAYING

    def set_blocking(self, is_blocking: bool) -> None:
        if not self.is_over:
            self.blocking = is_blocking

    def begin_enemy_warning(self) -> bool:
        if self.is_over:
            return False
        self.randomize_block_target()
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
        else:
            self.successful_blocks += 1

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
        if self.is_over or self.successful_blocks < self.required_blocks:
            return False
        self.randomize_opening_target()
        self.phase = Phase.VULNERABLE
        self.successful_blocks = 0
        self.vulnerability_hit = False
        self.last_attack_success = False
        return True

    def attack(self, cursor_x: int, cursor_y: int) -> bool:
        if (
            self.is_over
            or self.phase is not Phase.VULNERABLE
            or self.blocking
            or self.vulnerability_hit
        ):
            return False

        self.last_attack_success = self.opening_target.contains(cursor_x, cursor_y)
        if self.last_attack_success:
            self.enemy_health = max(0, self.enemy_health - self.damage)
            self.vulnerability_hit = True
            self._update_result()
        return self.last_attack_success

    def return_to_idle(self) -> bool:
        if self.is_over:
            return False
        self.phase = Phase.IDLE
        self.last_block_success = False
        self.last_attack_success = False
        return True

    def randomize_targets(self) -> None:
        self.randomize_block_target()
        self.randomize_opening_target()

    def randomize_block_target(self) -> None:
        self.block_target = self._random_target()

    def randomize_opening_target(self) -> None:
        self.opening_target = self._random_target()

    def _random_target(self) -> Target:
        max_x = self.area_width - self.target_width
        max_y = self.area_height - self.target_height
        return Target(
            self.rng.randint(0, max_x),
            self.rng.randint(0, max_y),
            self.target_width,
            self.target_height,
        )

    def _update_result(self) -> None:
        if self.player_health == 0 and self.enemy_health == 0:
            self.result = GameResult.DRAW
        elif self.enemy_health == 0:
            self.result = GameResult.WON
        elif self.player_health == 0:
            self.result = GameResult.LOST
