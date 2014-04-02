import unittest
from enum import Enum

class Colors(Enum):
    White = 1
    Black = 2

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        letters = "abcdefgh"
        return letters[self.x] + str(self.y + 1)

class Board:
    def __init__(self, pieces = set()):
        self.pieces = pieces

    def isInBoard(x, y):
        BOARDMAX = 7
        BOARDMIN = 0
        return x >= BOARDMIN and x <= BOARDMAX and y >= BOARDMIN and y <= BOARDMAX

    def isOccupied(self, x, y):
        return any(piece.x == x and piece.y == y for piece in self.pieces)

    def pieceAt(self, x, y):
        for piece in self.pieces:
            if (piece.x == x and piece.y == y):
                return piece

    def movesInDirection(self, x, y, dx, dy, color):
        moves = set()
        x += dx
        y += dy
        while (Board.isInBoard(x,y)):
            if (self.isOccupied(x,y)):                
                if self.pieceAt(x, y).color != color:
                    moves.add((x, y))
                break
            moves.add((x,y))
            x += dx
            y += dy
        return moves

class Piece:
    def __init__(self, x, y, color = Colors.Black):
        self.x = x
        self.y = y
        self.color = color

class Bishop(Piece):
    def validMoves(self, board):
        moves = set()

        moves.update(board.movesInDirection(self.x, self.y, +1, +1, self.color))
        moves.update(board.movesInDirection(self.x, self.y, +1, -1, self.color))
        moves.update(board.movesInDirection(self.x, self.y, -1, +1, self.color))
        moves.update(board.movesInDirection(self.x, self.y, -1, -1, self.color))

        return moves

class Rook(Piece):
    def validMoves(self, board):
        moves = set()

        moves.update(board.movesInDirection(self.x, self.y, +1, 0, self.color))
        moves.update(board.movesInDirection(self.x, self.y, -1, 0, self.color))
        moves.update(board.movesInDirection(self.x, self.y, 0, +1, self.color))
        moves.update(board.movesInDirection(self.x, self.y, 0, -1, self.color))

        return moves

class Queen(Piece):
    def validMoves(self, board):
        moves = set()

        moves.update(Rook(self.x, self.y, board).validMoves(board))
        moves.update(Bishop(self.x, self.y, board).validMoves(board))

        return moves


class Tests(unittest.TestCase):
    
    def testPlaceBishopSomewhere(self):
        bishop = Bishop(3, 5)
        self.assertEqual(3, bishop.x)
        self.assertEqual(5, bishop.y)

    def testWhereCanABishopMove(self):
        bishop = Bishop(3, 5)
        calculatedMoves = bishop.validMoves(Board());
        expectedMoves = set([(2,4),(1,3),(0,2),(4,6),(5,7),(4,4),(5,3),(6,2),(7,1),(2,6),(1,7)])
        self.assertEqual(expectedMoves, calculatedMoves)

    def testWhereCanABishopInTheCornerMove(self):
        bishop = Bishop(0, 0)
        calculatedMoves = bishop.validMoves(Board());
        expectedMoves = set([(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)])
        self.assertEqual(expectedMoves, calculatedMoves)

    def testWhereCanARookInTheCornerMove(self):
        rook = Rook(0, 0)
        calculatedMoves = rook.validMoves(Board());
        expectedMoves = set([(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)])
        self.assertEqual(expectedMoves, calculatedMoves)

    def testRookMovesWithBishop(self):
        rook = Rook(3, 3)
        bishop = Bishop(5, 3)
        board = Board(set([rook, bishop]))
        moves = rook.validMoves(board);
        expectedMoves = set([(0, 3), (1, 3), (2, 3), (4, 3), (3, 0), (3, 1), (3, 2), (3, 4), (3, 5), (3, 6), (3, 7)])
        self.assertEqual(expectedMoves, moves)

    def testRookMovesWithOpposingBishop(self):
        rook = Rook(3, 3, Colors.Black)
        bishop = Bishop(5, 3, Colors.White)
        board = Board(set([rook, bishop]))
        moves = rook.validMoves(board);
        expectedMoves = set([(0, 3), (1, 3), (2, 3), (4, 3), (5, 3), (3, 0), (3, 1), (3, 2), (3, 4), (3, 5), (3, 6), (3, 7)])
        self.assertEqual(expectedMoves, moves)

    def testQueenMoves(self):
        queen = Queen(0, 0)
        moves = queen.validMoves(Board());
        expectedMoves = set([(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), 
                             (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                             (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)])
        self.assertEqual(expectedMoves, moves)

    def testPointToString(self):
        cell = Cell(2,3)
        self.assertEqual("c4", str(cell))

if __name__ == '__main__':
    unittest.main()

