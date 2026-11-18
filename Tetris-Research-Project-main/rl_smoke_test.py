import argparse
import csv
from pathlib import Path

import numpy as np

from rl_env import RewardConfig, TetrisRLEnv


def run_episode(seed, max_pieces=1000, policy_seed=0, reward_config=None):
    env = TetrisRLEnv(max_pieces=max_pieces, reward_config=reward_config)
    env.reset(seed=seed)
    rng = np.random.default_rng(policy_seed)
    terminated = truncated = False
    while not (terminated or truncated):
        actions = env.available_actions()
        action = actions[int(rng.integers(len(actions)))]
        _, _, terminated, truncated, info = env.step(action)
    return {
        "seed": seed,
        "policy_seed": policy_seed,
        "max_pieces": max_pieces,
        "pieces_placed": info["pieces_placed"],
        "lines_cleared": info["total_lines"],
        "total_reward": round(info["episode_reward"], 6),
        "terminated": terminated,
        "truncated": truncated,
    }


def positive_int(value):
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("must be positive")
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episodes", type=positive_int, default=5)
    parser.add_argument("--start-seed", type=int, default=0)
    parser.add_argument("--policy-seed", type=int, default=100)
    parser.add_argument("--max-pieces", type=positive_int, default=1000)
    parser.add_argument("--output", type=Path,
                        default=Path("results/rl_random_smoke.csv"))
    args = parser.parse_args()
    if args.start_seed < 0 or args.policy_seed < 0:
        parser.error("seeds must be non-negative")

    config = RewardConfig()
    results = []
    for episode in range(args.episodes):
        row = run_episode(args.start_seed + episode, args.max_pieces,
                          args.policy_seed + episode, config)
        row.update(placement_reward=config.placement,
                   line_weight=config.line_weight,
                   game_over_penalty=config.game_over)
        results.append(row)
        print(f"seed={row['seed']} pieces={row['pieces_placed']} "
              f"lines={row['lines_cleared']} reward={row['total_reward']:.2f} "
              f"end={'game_over' if row['terminated'] else 'piece_limit'}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)
    print(f"Saved {len(results)} random-policy episodes to {args.output}")


if __name__ == "__main__":
    main()
