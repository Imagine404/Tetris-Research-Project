import unittest
from unittest.mock import patch

import numpy as np

from features import board_features
from rl_env import RewardConfig, TetrisRLEnv
from rl_smoke_test import run_episode
from tetris_sim import get_placements


class EnvironmentTests(unittest.TestCase):
    def test_observation_contains_shared_features_and_pieces(self):
        env = TetrisRLEnv()
        obs, info = env.reset(seed=7)
        self.assertEqual(obs["board"].shape, (20, 10))
        np.testing.assert_array_equal(obs["features"], board_features(obs["board"]))
        self.assertIn(obs["current_piece"], "TJZOSLI")
        self.assertIn(obs["next_piece"], "TJZOSLI")
        self.assertEqual(info["pieces_placed"], 0)
        obs["board"][:] = 1
        self.assertTrue(env.candidate_placements())
        self.assertEqual(env.step(env.available_actions()[0])[0]["board"].sum(), 4)

    def test_piece_limit_is_not_game_over(self):
        env = TetrisRLEnv(max_pieces=1)
        before, _ = env.reset(seed=0)
        obs, reward, terminated, truncated, info = env.step(env.available_actions()[0])
        self.assertFalse(terminated)
        self.assertTrue(truncated)
        self.assertAlmostEqual(reward, 0.1)
        self.assertEqual(info["pieces_placed"], 1)
        self.assertEqual(obs["current_piece"], before["next_piece"])
        self.assertEqual(env.available_actions(), [])
        with self.assertRaises(RuntimeError):
            env.step(("O", 5))

    def test_illegal_action_leaves_game_unchanged(self):
        env = TetrisRLEnv()
        env.reset(seed=0)
        actions = env.available_actions()
        with self.assertRaises(ValueError):
            env.step(("invalid", -1))
        self.assertEqual(actions, env.available_actions())
        _, _, _, _, info = env.step(actions[0])
        self.assertEqual(info["pieces_placed"], 1)

    def test_four_line_clear_through_environment(self):
        board = np.zeros((20, 10), dtype=int)
        board[16:, :9] = 1
        candidates = get_placements(board, "I")
        env = TetrisRLEnv()
        with patch("rl_env.get_placements", return_value=candidates):
            env.reset(seed=0)
        obs, reward, terminated, truncated, info = env.step(("Iv", 9))
        self.assertEqual(info["lines_cleared"], 4)
        self.assertEqual(info["total_lines"], 4)
        self.assertFalse(obs["board"].any())
        self.assertAlmostEqual(reward, 16.1)
        self.assertFalse(terminated or truncated)

    def test_game_over_penalty_and_reset(self):
        env = TetrisRLEnv()
        env.reset(seed=0)
        with patch("rl_env.get_placements", return_value=[]):
            _, reward, terminated, truncated, info = env.step(env.available_actions()[0])
        self.assertTrue(terminated)
        self.assertFalse(truncated)
        self.assertAlmostEqual(reward, -9.9)
        self.assertTrue(info["game_over"])
        with self.assertRaises(RuntimeError):
            env.step(("O", 5))
        _, info = env.reset(seed=0)
        self.assertEqual(info["episode_reward"], 0)
        self.assertTrue(env.available_actions())

    def test_reproducible_complete_episode(self):
        first = run_episode(3, max_pieces=1000, policy_seed=42)
        second = run_episode(3, max_pieces=1000, policy_seed=42)
        self.assertEqual(first, second)
        self.assertTrue(first["terminated"])
        self.assertLess(first["pieces_placed"], 1000)
        expected = first["pieces_placed"] * 0.1 - 10
        self.assertGreaterEqual(first["total_reward"], round(expected, 6))

    def test_candidate_boards_are_copies(self):
        env = TetrisRLEnv()
        env.reset(seed=0)
        candidate = env.candidate_placements()[0]
        candidate[2][:] = 1
        obs, _, _, _, _ = env.step((candidate[0], candidate[1]))
        self.assertEqual(obs["board"].sum(), 4)

    def test_reward_configuration(self):
        config = RewardConfig(placement=0, line_weight=2, game_over=-20)
        self.assertEqual(config.calculate(2, False), 8)
        self.assertEqual(config.calculate(0, True), -20)

    def test_reset_required_and_positive_limit(self):
        with self.assertRaises(ValueError):
            TetrisRLEnv(max_pieces=0)
        with self.assertRaises(RuntimeError):
            TetrisRLEnv().step(("O", 5))


if __name__ == "__main__":
    unittest.main()
