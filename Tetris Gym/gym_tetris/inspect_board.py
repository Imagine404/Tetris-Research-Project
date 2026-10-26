
import gymnasium as gym
import gym_tetris
import numpy as np
import cv2
from gym_tetris.actions import SIMPLE_MOVEMENT
from nes_py.wrappers import JoypadSpace
from graphs import ImplicitGraphNode as graphNode
import copy


# Each tuple represents (x, y) relative to the piece's origin
# X increases right, Y increases down
# Each list contains the possible rotations of that piece
PIECE_SHAPES = {
    "I": [
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        [(0, 0), (0, 1), (0, 2), (0, 3)]
    ],

    "O": [
        [(0, 0), (1, 0),
         (0, 1), (1, 1)]
    ],

    "T": [
        [(0, 0), (1, 0), (2, 0), (1, 1)],
        [(1, 0), (0, 1), (1, 1), (1, 2)],
        [(1, 0), (0, 1), (1, 1), (2, 1)],
        [(0, 0), (0, 1), (1, 1), (0, 2)]
    ],

    "S": [
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(0, 0), (0, 1), (1, 1), (1, 2)]
    ],

    "Z": [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(1, 0), (0, 1), (1, 1), (0, 2)]
    ],

    "J": [
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(0, 0), (1, 0), (0, 1), (0, 2)],
        [(0, 0), (1, 0), (2, 0), (2, 1)],
        [(1, 0), (1, 1), (0, 2), (1, 2)]
    ],

    "L": [
        [(2, 0), (0, 1), (1, 1), (2, 1)],
        [(0, 0), (0, 1), (0, 2), (1, 2)],
        [(0, 0), (1, 0), (2, 0), (0, 1)],
        [(0, 0), (1, 0), (1, 1), (1, 2)]
    ]
}


# Creates and starts the Tetris game
def createGame():
    env = gym.make("TetrisA-v0", render_mode="rgb_array")
    env = JoypadSpace(env, SIMPLE_MOVEMENT)

    observation, info = env.reset()
    return env, info


# Reads the NES Tetris board from RAM
def readBoard(env):
    ram = env.unwrapped.ram
    board = np.array(ram[0x0400:0x04C8]).reshape(20, 10)

    # Convert raw tiles into occupied/empty cells
    binaryBoard = (board != 0xEF).astype(int)

    return binaryBoard


# Prints the current game state
def printGameState(step, board, info):
    print(f"\nSTEP {step}")
    print(board)
    print("Current piece:", info.get("current_piece"))
    print("Next piece:", info.get("next_piece"))
    print("Score:", info.get("score"))

# Checks if the current piece position is valid
def isValidPosition(state):
    pieceType = state.currentPiece[0]
    shapes = PIECE_SHAPES[pieceType]

    shape = shapes[state.pieceRotation % len(shapes)]

    for dx, dy in shape:
        x = state.pieceX + dx
        y = state.pieceY + dy

        # Check horizontal boundaries
        if x < 0 or x >= 10:
            return False

        # Check bottom boundary
        if y >= 20:
            return False

        # Check collision with settled blocks
        if y >= 0 and state.board[y, x] == 1:
            return False

    return True

# Discovers all possible states from one Tetris action
def discoverTetrisNeighbors(node, existingNeighbors):
    currentState = node.stateValue
    newNeighbors = []

    # Each action represents one possible movement
    actions = ["LEFT", "RIGHT", "DOWN", "ROTATE_CW", "ROTATE_CCW"]

    for action in actions:
        # Make a copy so we don't modify the original state
        newState = copy.deepcopy(currentState)

        # Apply the action to the copied state
        if action == "LEFT":
            newState.pieceX -= 1

        elif action == "RIGHT":
            newState.pieceX += 1

        elif action == "DOWN":
            newState.pieceY += 1

        elif action == "ROTATE_CW":
            newState.pieceRotation = (newState.pieceRotation + 1) % 4

        elif action == "ROTATE_CCW":
            newState.pieceRotation = (newState.pieceRotation - 1) % 4

        # Check if the new piece position is valid
        if not isValidPosition(newState):
            continue

        # Create the new graph node
        newNode = graphNode(key=newState.getKey(),stateValue=newState,discoveryFunction=discoverTetrisNeighbors)

        # Each movement costs 1
        newNeighbors.append([newNode, 1])

    return newNeighbors


# Displays the game and checks if Q was pressed
def displayGame(env):
    frame = env.render()

    if frame is not None:
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = cv2.resize(frame, None, fx=2, fy=2)
        cv2.imshow("NES Tetris", frame)

    # Returns True if Q is pressed
    return cv2.waitKey(16) & 0xFF == ord("q")


# Chooses the next action
def chooseAction(board, info):
    action = 0  # Do nothing for now

    return action


# Runs the game
def runGame():
    env, info = createGame()
    step = 0

    try:
        while True:
            board = readBoard(env)

            printGameState(step, board, info)

            if displayGame(env):
                break

            action = chooseAction(board, info)
            observation, reward, terminated, truncated, info = env.step(action)

            step += 1

            if terminated or truncated:
                print("\nGAME OVER")
                observation, info = env.reset()
                step = 0

    except KeyboardInterrupt:
        print("Stopped.")

    finally:
        cv2.destroyAllWindows()
        env.close()


if __name__ == "__main__":
    runGame()
