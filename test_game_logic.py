import unittest

from game_logic import CombatGame, GameResult, Phase


class CombatGameTests(unittest.TestCase):
    def start_attack(self, game: CombatGame) -> None:
        self.assertTrue(game.begin_enemy_warning())
        self.assertTrue(game.begin_enemy_attack())

    def test_successful_block_preserves_player_health(self) -> None:
        game = CombatGame()
        self.start_attack(game)
        game.set_blocking(True)

        blocked = game.resolve_enemy_attack(100, 250)

        self.assertTrue(blocked)
        self.assertEqual(game.player_health, 3)
        self.assertEqual(game.result, GameResult.PLAYING)

    def test_failed_block_damages_player(self) -> None:
        game = CombatGame()
        self.start_attack(game)
        game.set_blocking(True)

        blocked = game.resolve_enemy_attack(500, 250)

        self.assertFalse(blocked)
        self.assertEqual(game.player_health, 2)

    def test_successful_attack_damages_enemy(self) -> None:
        game = CombatGame()
        self.assertTrue(game.begin_vulnerability())

        attacked = game.attack(600, 250)

        self.assertTrue(attacked)
        self.assertEqual(game.enemy_health, 2)

    def test_attack_outside_opening_and_while_blocking_fails(self) -> None:
        game = CombatGame()
        self.assertTrue(game.begin_vulnerability())
        game.set_blocking(True)

        self.assertFalse(game.attack(600, 250))
        self.assertEqual(game.enemy_health, 3)

        game.set_blocking(False)
        self.assertFalse(game.attack(100, 250))
        self.assertEqual(game.enemy_health, 3)

    def test_terminal_results(self) -> None:
        winning_game = CombatGame(max_health=1)
        self.assertTrue(winning_game.begin_vulnerability())
        winning_game.attack(600, 250)
        self.assertEqual(winning_game.result, GameResult.WON)

        losing_game = CombatGame(max_health=1)
        self.start_attack(losing_game)
        losing_game.resolve_enemy_attack(500, 250)
        self.assertEqual(losing_game.result, GameResult.LOST)

    def test_simultaneous_exchange_is_a_draw(self) -> None:
        game = CombatGame(max_health=1)
        self.start_attack(game)

        blocked, attacked = game.resolve_simultaneous_exchange(500, 250, 600, 250)

        self.assertFalse(blocked)
        self.assertTrue(attacked)
        self.assertEqual(game.player_health, 0)
        self.assertEqual(game.enemy_health, 0)
        self.assertEqual(game.result, GameResult.DRAW)

    def test_game_over_prevents_later_health_changes(self) -> None:
        game = CombatGame(max_health=1)
        self.assertTrue(game.begin_vulnerability())
        game.attack(600, 250)
        self.assertEqual(game.result, GameResult.WON)

        self.assertFalse(game.begin_enemy_warning())
        self.assertFalse(game.begin_vulnerability())
        self.assertFalse(game.attack(600, 250))
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


if __name__ == "__main__":
    unittest.main()
