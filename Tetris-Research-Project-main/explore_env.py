import gymnasium as gym
import gym_tetris
from nes_py.wrappers import JoypadSpace
from gym_tetris.actions import MOVEMENT

env = JoypadSpace(gym.make("TetrisA-v1"), MOVEMENT)
obs, info = env.reset(seed=1)
raw = env.unwrapped

print(info)
# this contains the piece and its oritnetaion at the top
# we cant actaully see it on the board as it falls until it is locked in place.
# we should store this so that we can then apply changes to it

# this isnt a problem cuz all we really need is curr piece next piece and landing area? space? idk something like that


# watch the live peice fall raw.ram[0x40] is column and raw.ram[0x41] is the row

board = (raw._board != 239).astype(int)
print(board)
# test loop
'''
for frame in range(60):
    obs, reward, terminated, truncated, info =env.step(9)
    board = (raw._board != 239).astype(int)
    #print(board, frame)
    print(frame, raw.ram[0x48], raw.ram[0x41], info['current_piece'])
'''


# if a piece is falling raw.ram-0x48] is 1 once it has landed it goes to 8 before the next piece starts
# i think during this time it does something in memeroy but less important for what we are doing rn
while raw.ram[0x48] == 1:
    obs, reward, terminated, truncated, info =env.step(9)
while raw.ram[0x48] > 1 and raw.ram[0x48] <= 8:
    obs, reward, terminated, truncated, info =env.step(0)

board = (raw._board != 239).astype(int)
print(board)
print(info['current_piece'])

