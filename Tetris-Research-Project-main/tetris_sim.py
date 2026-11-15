# Tetris Simulation 

# this will be used for the neural network and A* to simulate 
# the next action and where a piece can fit

import numpy as np
from features import column_heights

ROWS, COLS = 20, 10


# (dx,dy) cell offsets of each piece's pivot 
# dx = right
# dy = down
# could be some mistakes in here need go back over this (I think its all good now)
OFFSETS = { 
    'Tu': [(0, -1), (-1, 0), (0, 0), (1, 0)],  'Tr': [(0, -1), (0, 0), (1, 0), (0, 1)],
    'Td': [(-1, 0), (0, 0), (1, 0), (0, 1)],   'Tl': [(0, -1), (-1, 0), (0, 0), (0, 1)],
    'Jl': [(0, -1), (0, 0), (-1, 1), (0, 1)],  'Ju': [(-1, -1), (-1, 0), (0, 0), (1, 0)],
    'Jr': [(0, -1), (1, -1), (0, 0), (0, 1)],  'Jd': [(-1, 0), (0, 0), (1, 0), (1, 1)],
    'Zh': [(-1, 0), (0, 0), (0, 1), (1, 1)],   'Zv': [(1, -1), (0, 0), (1, 0), (0, 1)],
    'O':  [(-1, 0), (0, 0), (-1, 1), (0, 1)],
    'Sh': [(0, 0), (1, 0), (-1, 1), (0, 1)],   'Sv': [(0, -1), (0, 0), (1, 0), (1, 1)],
    'Lr': [(0, -1), (0, 0), (0, 1), (1, 1)],   'Ld': [(-1, 0), (0, 0), (1, 0), (-1, 1)],
    'Ll': [(-1, -1), (0, -1), (0, 0), (0, 1)], 'Lu': [(1, -1), (-1, 0), (0, 0), (1, 0)],
    'Iv': [(0, -2), (0, -1), (0, 0), (0, 1)],  'Ih': [(-2, 0), (-1, 0), (0, 0), (1, 0)],
 }

# Dictionary of all tetramino orientations 
# should be all of the orientations also could use a second look. (I think its all good now)
PIECE_ORIENTATIONS = {
    'T': ['Tu', 'Tr', 'Td', 'Tl'],
    'J': ['Ju', 'Jl', 'Jr', 'Jd'],
    'Z': ['Zh', 'Zv'],
    'O': ['O'],
    'S': ['Sh', 'Sv'],
    'L': ['Lu','Lr', 'Ld', 'Ll' ],
    'I': ['Iv', 'Ih'],
}

# we want to check if a piece when offset can still fit in a column and row.
# we will return true or false
def fits(board, cells, x, y):
    rows, cols = board.shape
    for (dx,dy) in cells:
        c = x + dx
        r = y + dy
        if c >= cols or c < 0:
            return False
        if r >= rows:
            return False
        if r >= 0 and board[r,c] == 1:
            return False
    return True 

# Drops orientation straight down in column from the top
# returns (newboard, lines_cleared) or None if it can't be placed 
def simulate_drop(board, orient, x):
    cells = OFFSETS[orient]
    y = 0
    if not fits(board, cells, x, y):
        return None

    while fits(board, cells, x, y+1):
        y += 1

    new_board = board.copy()
    for (dx, dy) in cells:
        c = x + dx
        r = y + dy

        if r < 0:
            return None
        new_board[r,c] = 1

    rows, cols = new_board.shape
    kept = []

    for r in range(rows):
        if sum(new_board[r]) != cols:
            kept.append(new_board[r])

    lines = rows - len(kept)

    result = []

    for _ in range(lines):
        result.append(np.zeros(cols, dtype = int))

    for row in kept:
        result.append(row)

    return np.array(result), lines




# we want to return every possible placement of our current 'piece'
# reutnr a list of (orient, x, new_board, lines_cleared)
def get_placements(board, piece):
    placements = []
    for orient in PIECE_ORIENTATIONS[piece]:
        for x in range(COLS):
            result = simulate_drop(board,orient,x)
            if result is not None:
                new_board, lines = result
                placements.append((orient, x, new_board, lines))
    return placements


# Allows for reproducable tests 
PIECE_TYPES = "TJZOSLI"
class PieceSequence:
    def __init__(self, seed):
        self.rng = np.random.default_rng(seed)
        self.prev = None
        self.current = self._roll()
        self.next = self._roll()
    def _roll(self):
        p = int(self.rng.integers(0,8))
        if p == 7 or p == self.prev:
            p = int(self.rng.integers(0,7))
        self.prev = p
        return PIECE_TYPES[p]
    def advance(self):
        self.current = self.next
        self.next = self._roll()
# Tests

if __name__ == "__main__":
    # Fits Test
    empty = np.zeros((ROWS, COLS), dtype = int)
    jd = OFFSETS['Jd']
    print(fits(empty, jd, 5, 18))
    print(fits(empty, jd, 5, 19))
    print(fits(empty, jd, 0, 10))   
    print(fits(empty, jd, 9, 10))

    blocked = empty.copy()
    blocked[18, 5] = 1
    print(fits(blocked, jd, 5, 18))
    print(fits(empty, OFFSETS['Iv'], 3, 0))

    # simulate Drop Test

    result = simulate_drop(empty, 'Jd', 5)
    after_jd, lines = result
    print(after_jd[18:])
    print(lines)

    after_i, _ = simulate_drop(after_jd, 'Iv', 6)
    print(column_heights(after_i))
    print(simulate_drop(empty, 'Jd', 0))

    tall = empty.copy()
    tall[2:, 3] = 1
    print(simulate_drop(tall, 'Iv',3))

    one = empty.copy()
    one[19, :9] = 1
    board1, lines1 = simulate_drop(one, 'Iv', 9)
    print(lines1, column_heights(board1))

    four = empty.copy()
    four[16:, :9] = 1
    board4, lines4 = simulate_drop(four, 'Iv', 9)
    print(lines4, column_heights(board4))

    # placemet test
    for piece in ['J','O','I']:
        print(piece, len(get_placements(empty, piece)))

    orient, x, b, lines = get_placements(empty, 'O')[0]
    print(orient,x, lines)
    print(column_heights(b))


    # sequence test


    a = PieceSequence(7)
    b = PieceSequence(8)
    c = PieceSequence(8)
    seq_a, seq_b, seq_c = '', '', ''
    for _ in range(15):
        seq_a += a.current; a.advance()
        seq_b += b.current; b.advance()
        seq_c += c.current; c.advance()
    print(seq_a, seq_b, seq_c)

    s = PieceSequence(0)
    repeats = 0
    for _ in range(7000):
        old = s.current
        s.advance()
        if s.current == old:
            repeats += 1
    print(repeats / 7000)