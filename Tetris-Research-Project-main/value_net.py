import numpy as np
import torch
import torch.nn as nn
from features import board_features, num_features

FEATURE_SCALE = np.array([200.0, 200.0, 180.0, 20.0], dtype = np.float32)

def scaled_features(board):
    # scaled board features
    return board_features(board) / FEATURE_SCALE



class ValueNet(nn.Module):
    def __init__(self, n_inputs=num_features, hidden=64):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(n_inputs, hidden),
            nn.ReLU(),
            nn.Linear(hidden,hidden),
            nn.ReLU(),
            nn.Linear(hidden,1),
        )

    def forward(self, x):
        return self.layers(x).squeeze(-1)

def save_model(net, path):
        torch.save(net.state_dict(), path)

def load_model(path):
        net = ValueNet()
        net.load_state_dict(torch.load(path))
        net.eval()
        return net


def board_value(net, board):
     with torch.no_grad():
          x = torch.from_numpy(scaled_features(board))
          return net(x).item()

# Tests

if __name__ == "__main__":
    board = np.zeros((20, 10), dtype=int)
    board[19, 0:4] = 1
    board[18, 1] = 1
    board[17, 1] = 1
    board[16, 5] = 1

    f = scaled_features(board)
    print(f)

    net = ValueNet()
    print(net(torch.from_numpy(f)))

    batch = torch.from_numpy(np.stack([f, f, f]))
    print(net(batch).shape)

    print(sum(p.numel() for p in net.parameters()))

    save_model(net, "test_model.pt")
    loaded = load_model("test_model.pt")
    print(board_value(net, board))
    print(board_value(loaded, board))


# value_net.py - board value network (Stephen)
# Input:  20x10 0/1 board -> scaled_features -> 4 numbers between 0 and 1
# Output: one number, the predicted long-term value of the board
# For training: call net(batch) on a tensor of scaled features (keeps gradients)
# For using a trained net: board_value(net, board) returns a plain float
# Save/load: save_model(net, path) / load_model(path)