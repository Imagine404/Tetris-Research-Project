from dataclasses import dataclass

import numpy as np

from features import board_features
from tetris_sim import COLS, ROWS, PieceSequence, get_placements


@dataclass(frozen=True)
class RewardConfig:
    placement: float = 0.1
    line_weight: float = 1.0
    game_over: float = -10.0

    def calculate(self, lines_cleared, terminated):
        return (
            self.placement
            + self.line_weight * lines_cleared ** 2
            + (self.game_over if terminated else 0.0)
        )


class TetrisRLEnv:

    def __init__(self, max_pieces=1000, reward_config=None):
        if not isinstance(max_pieces, int) or max_pieces <= 0:
            raise ValueError("max_pieces must be a positive integer")
        self.max_pieces = max_pieces
        self.reward_config = reward_config or RewardConfig()
        self._sequence = None
        self._candidates = []
        self._finished = True

    def reset(self, seed=0):
        self._seed = seed
        self._sequence = PieceSequence(seed)
        self._board = np.zeros((ROWS, COLS), dtype=int)
        self._pieces = 0
        self._lines = 0
        self._episode_reward = 0.0
        self._finished = False
        self._candidates = get_placements(self._board, self._sequence.current)
        return self._observation(), self._info()

    def available_actions(self):
        return [(orient, x) for orient, x, _, _ in self._candidates]

    def candidate_placements(self):
        return [(orient, x, board.copy(), lines)
                for orient, x, board, lines in self._candidates]

    def step(self, action):
        if self._finished:
            raise RuntimeError("Call reset() before starting or after ending a game")
        chosen = next((p for p in self._candidates if (p[0], p[1]) == action), None)
        if chosen is None:
            raise ValueError("Choose an action from available_actions()")

        _, _, board, lines = chosen
        self._board = board.copy()
        self._pieces += 1
        self._lines += lines
        self._sequence.advance()
        self._candidates = get_placements(self._board, self._sequence.current)
        terminated = not self._candidates
        truncated = self._pieces >= self.max_pieces and not terminated
        reward = self.reward_config.calculate(lines, terminated)
        self._episode_reward += reward
        self._finished = terminated or truncated
        if self._finished:
            self._candidates = []
        return (
            self._observation(), reward, terminated, truncated,
            self._info(lines, terminated, truncated),
        )

    def _observation(self):
        return {
            "board": self._board.copy(),
            "features": board_features(self._board),
            "current_piece": self._sequence.current,
            "next_piece": self._sequence.next,
        }

    def _info(self, lines_cleared=0, terminated=False, truncated=False):
        return {
            "seed": self._seed,
            "pieces_placed": self._pieces,
            "total_lines": self._lines,
            "lines_cleared": lines_cleared,
            "episode_reward": self._episode_reward,
            "game_over": terminated,
            "piece_limit_reached": truncated,
        }
