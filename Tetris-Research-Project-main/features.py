# Features

# Feature Ideas 
# Aggregate Height - the sum of all column heights - Why? taller stakcns mean closer to loss
# Holes - empty cells that are filled above - Why? these areas cannot be accessed
# Bumpiness - sum of difference in heights between neighbors - why? a bumpy playing field leaves less opportunity for clean solutions
# Max Height - Tallest Column Why? this ends the game.


import numpy as np


# number of features
num_features = 4

# function that returns the height of each column on the board
def column_heights(board):
    rows, cols = board.shape
    heights = []
    for c in range(cols):
        height = 0
        for r in range(rows):
            if board[r,c] == 1:
                height = (rows - r)
                break
        heights.append(height)
    return heights




# features that adds together the height of all of the columns
# the higher this value the closer to the end of the game in some cases
def aggregate_height(heights):
    total = 0
    for i in range(len(heights)):
        total += heights[i]
        agg_height = total
    return agg_height


# feature to detect holes in columns on the game board 
def holes(board):
    count = 0 
    rows, cols = board.shape
    for c in range(cols):
        seen_block = False
        for r in range(rows):
            position = board[r,c]
            if position == 1:
                seen_block = True
            elif seen_block:
                    count += 1
    return count

#  sum of difference in heights between neighbors
def bumpiness(heights):
    bump = 0
    for i in range(len(heights) - 1):
        difference = abs(heights[i] - heights[i +1])
        bump += difference
    return bump

# feature that returns the tallest column
def max_height(heights):
    tallest = heights[0]
    for h in heights:
        if h > tallest:
            tallest = h
    return tallest

# function that returns all of our features as a array.
def board_features(board):
    heights = column_heights(board)
    agg_height = aggregate_height(heights)
    m_height = max_height(heights)
    bump = bumpiness(heights)
    h = holes(board)
    return np.array([agg_height, h, bump, m_height], dtype=np.float32)





if __name__ == "__main__":

    # Test board 
    
    board = np.zeros((20,10), dtype=int)
    board[19, 0:4] = 1
    board[18, 1] = 1
    board[17, 1] = 1
    board[16, 5] = 1
    heights = column_heights(board)
    #print(column_heights(board))
    #print(aggregate_height(heights))
    #print(max_height(heights))
    #print(bumpiness(heights))
    #print(holes(board))
    print(board_features(board))

