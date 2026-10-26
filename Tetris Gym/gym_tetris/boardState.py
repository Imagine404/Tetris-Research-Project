# Used for our A* approach to be the state value of each graph node
class BoardState ():
    def __init__ (self, board, currentPiece, nextPiece,pieceX, pieceY, pieceRotation):
        self.board = board
        self.currentPiece = currentPiece
        self.nextPiece = nextPiece

        self.pieceX = pieceX
        self.pieceY = pieceY
        self.pieceRotation = pieceRotation

    # Unique identifier for the current game state
    def getKey(self):
        return (
            self.board.tobytes(), # 0s and ones for the board state
            self.currentPiece,
            self.nextPiece,
            self.pieceX,
            self.pieceY,
            self.pieceRotation
        )

