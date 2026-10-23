import random
import unittest

from game_logic import CombatGame, GameResult, Phase, Target, scaled_target


class CombatGameTests(unittest.TestCase):
    def start_attack(self, game: CombatGame) -> None:
        self.assertTrue(game.begin_enemy_warning())
        self.assertTrue(game.begin_enemy_attack())

    def successful_block(self, game: CombatGame) -> None:
        self.start_attack(game)
        game.set_blocking(True)
        target = game.block_target
        self.assertTrue(game.resolve_enemy_attack(target.x, target.y))
        game.set_blocking(False)
        self.assertTrue(game.return_to_idle())

    def outside_target(self, target: Target) -> tuple[float, float]:
        if target.x + target.width + 1 <= 800:
            return target.x + target.width + 1, target.y
        return target.x - 1, target.y

    def unlock_vulnerability(self, game: CombatGame) -> None:
        for _ in range(game.required_blocks):
            self.successful_block(game)
        self.assertTrue(game.begin_vulnerability())

    def test_successful_block_preserves_player_health(self) -> None:
        game = CombatGame()
        self.start_attack(game)
        game.set_blocking(True)
        target = game.block_target

        blocked = game.resolve_enemy_attack(target.x, target.y)

        self.assertTrue(blocked)
        self.assertEqual(game.player_health, 3)
        self.assertEqual(game.successful_blocks, 1)
        self.assertEqual(game.result, GameResult.PLAYING)

    def test_failed_block_damages_player(self) -> None:
        game = CombatGame()
        self.start_attack(game)
        game.set_blocking(True)
        cursor_x, cursor_y = self.outside_target(game.block_target)

        blocked = game.resolve_enemy_attack(cursor_x, cursor_y)

        self.assertFalse(blocked)
        self.assertEqual(game.player_health, 2)
        self.assertEqual(game.successful_blocks, 0)

    def test_vulnerability_requires_five_successful_blocks(self) -> None:
        game = CombatGame()

        for _ in range(4):
            self.successful_block(game)
        self.assertFalse(game.begin_vulnerability())
        self.successful_block(game)

        self.assertTrue(game.begin_vulnerability())
        self.assertEqual(game.successful_blocks, 0)

    def test_vulnerability_hit_limit_resets_for_next_opening(self) -> None:
        game = CombatGame()
        self.unlock_vulnerability(game)
        target = game.opening_target

        self.assertTrue(game.attack(target.x, target.y))
        self.assertFalse(game.attack(target.x, target.y))

        game.return_to_idle()
        self.unlock_vulnerability(game)
        self.assertTrue(game.attack(game.opening_target.x, game.opening_target.y))

    def test_missed_attack_can_be_retried_once(self) -> None:
        game = CombatGame()
        self.unlock_vulnerability(game)
        target = game.opening_target

        self.assertFalse(game.attack(target.x - 1, target.y - 1))
        self.assertTrue(game.attack(target.x, target.y))
        self.assertFalse(game.attack(target.x, target.y))
        self.assertEqual(game.enemy_health, 2)

    def test_successful_attack_damages_enemy(self) -> None:
        game = CombatGame()
        self.unlock_vulnerability(game)

        target = game.opening_target
        attacked = game.attack(target.x, target.y)

        self.assertTrue(attacked)
        self.assertEqual(game.enemy_health, 2)

    def test_attack_outside_opening_and_while_blocking_fails(self) -> None:
        game = CombatGame()
        self.unlock_vulnerability(game)
        target = game.opening_target
        game.set_blocking(True)

        self.assertFalse(game.attack(target.x, target.y))
        self.assertEqual(game.enemy_health, 3)

        game.set_blocking(False)
        self.assertFalse(game.attack(100, 250))
        self.assertEqual(game.enemy_health, 3)

    def test_terminal_results(self) -> None:
        winning_game = CombatGame(max_health=1)
        self.unlock_vulnerability(winning_game)
        winning_game.attack(winning_game.opening_target.x, winning_game.opening_target.y)
        self.assertEqual(winning_game.result, GameResult.WON)

        losing_game = CombatGame(max_health=1)
        self.start_attack(losing_game)
        cursor_x, cursor_y = self.outside_target(losing_game.block_target)
        losing_game.resolve_enemy_attack(cursor_x, cursor_y)
        self.assertEqual(losing_game.result, GameResult.LOST)

    def test_simultaneous_exchange_is_a_draw(self) -> None:
        game = CombatGame(max_health=1)
        self.start_attack(game)
        opening_target = game.opening_target

        blocked_cursor = self.outside_target(game.block_target)
        blocked, attacked = game.resolve_simultaneous_exchange(
            blocked_cursor[0], blocked_cursor[1], opening_target.x, opening_target.y
        )

        self.assertFalse(blocked)
        self.assertTrue(attacked)
        self.assertEqual(game.player_health, 0)
        self.assertEqual(game.enemy_health, 0)
        self.assertEqual(game.result, GameResult.DRAW)

    def test_game_over_prevents_later_health_changes(self) -> None:
        game = CombatGame(max_health=1)
        self.unlock_vulnerability(game)
        game.attack(game.opening_target.x, game.opening_target.y)
        self.assertEqual(game.result, GameResult.WON)

        self.assertFalse(game.begin_enemy_warning())
        self.assertFalse(game.begin_vulnerability())
        self.assertFalse(game.attack(game.opening_target.x, game.opening_target.y))
        self.assertEqual((game.player_health, game.enemy_health), (1, 0))

    def test_restart_restores_initial_state(self) -> None:
        game = CombatGame()
        self.start_attack(game)
        game.resolve_enemy_attack(500, 250)
        game.restart()

        self.assertEqual(game.player_health, 3)
        self.assertEqual(game.enemy_health, 3)
        self.assertEqual(game.result, GameResult.PLAYING)
        self.assertEqual(game.phase, Phase.IDLE)
        self.assertFalse(game.blocking)

    def test_random_targets_stay_inside_game_area(self) -> None:
        game = CombatGame(rng=random.Random(7))

        for _ in range(10):
            game.randomize_targets()
            for target in (game.block_target, game.opening_target):
                self.assertGreaterEqual(target.x, 0)
                self.assertGreaterEqual(target.y, 0)
                self.assertLessEqual(target.x + target.width, game.area_width)
                self.assertLessEqual(target.y + target.height, game.area_height)

    def test_seeded_randomization_changes_prompt_positions(self) -> None:
        game = CombatGame(rng=random.Random(7))
        first = game.block_target
        game.randomize_block_target()
        second = game.block_target

        self.assertNotEqual(first, second)

    def test_scaled_target_grows_from_center(self) -> None:
        target = Target(100, 100, 200, 100)

        self.assertEqual(scaled_target(target, 0), Target(200, 150, 0, 0))
        self.assertEqual(scaled_target(target, 0.5), Target(150, 125, 100, 50))
        self.assertEqual(scaled_target(target, 1), target)


if __name__ == "__main__":
    unittest.main()
