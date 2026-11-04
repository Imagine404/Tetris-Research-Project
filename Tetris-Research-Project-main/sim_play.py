# This is our simulation so we can play full games inside the sim

import time
import numpy as np
from tetris_sim import get_placements, PieceSequence, ROWS, COLS
from features import board_features

# Line Weights from Yiyuan Lee's (2013) Greedy Weights
LINES_WEIGHT = 0.76
# Yiyuan Lee's Weights for the same weights we are using execpt for Max height which we created
WEIGHTS = np.array([-0.51, -0.36, -0.18, 0.0])

def score(placement):
    orient, x, new_board, lines = placement
    total = LINES_WEIGHT * lines + WEIGHTS @ board_features(new_board)
    return total

def play_game(seed, max_pieces=10000, watch=False):
    
    board = np.zeros((ROWS, COLS), dtype = int)
    seq = PieceSequence(seed)
    pieces, total_lines = 0, 0

    while pieces < max_pieces:
        placements = get_placements(board, seq.current)
        if len(placements) == 0:
            break

        best = placements[0]
        for p in placements:
            if score(p) > score(best):
                best = p

        orient, x, board, lines = best
        total_lines += lines
        pieces += 1
        seq.advance()
        if watch:
            print("\033[H\033[J", end="")
            render(board)
            print(f"pieces: {pieces} lines: {total_lines} next: {seq.current}")
            time.sleep(0.05)

    return pieces, total_lines

# board render because I want to watch it 

def render(board):
    for r in range(ROWS):
        line = ''
        for c in range(COLS):
            line += "#" if board[r,c] == 1 else 'x'
        print("|" + line + "|")
    print("+" + "-" * COLS + "*")


if __name__ == "__main__":
    play_game(0, max_pieces=10000, watch=True)
    for seed in range(5):
        start = time.perf_counter()
        pieces, lines = play_game(seed)
        secs = time.perf_counter() - start
        print(f"seed {seed}: {pieces} pieces, {lines} lines, {pieces / secs:.0f} pieces/sec")


