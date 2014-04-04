import unittest
from enum import Enum

class Colors(Enum):
    White = 1
    Black = 2

class Board:
    def __init__(self, pieces = set(), enPassantTarget = [-1, -1]):
        self.pieces = pieces
        self.enPassantTarget = enPassantTarget

    def isInBoard(x, y):
        BOARDMAX = 7
        BOARDMIN = 0
        return x >= BOARDMIN and x <= BOARDMAX and y >= BOARDMIN and y <= BOARDMAX

    def isOccupied(self, x, y):
        return any(piece.x == x and piece.y == y for piece in self.pieces)

    def __pieceAt(self, x, y):
        for piece in self.pieces:
            if (piece.x == x and piece.y == y):
                return piece

    def __emptyOrCanTake(self, x, y, color):
        return Board.isInBoard(x, y) and not (self.isOccupied(x, y) and self.__pieceAt(x,y).color == color)

    def canTake(self, x, y, color):
        return self.isOccupied(x, y) and self.__pieceAt(x,y).color != color

    def movesInDirection(self, x, y, dx, dy, color):
        moves = set()
        x += dx
        y += dy
        while (Board.isInBoard(x,y)):
            if (self.isOccupied(x,y)):
                if self.__emptyOrCanTake(x, y, color):
                    moves.add((x, y))
                break
            moves.add((x,y))
            x += dx
            y += dy
        return moves

    def singleMoveInDirection(self, x, y, dx, dy, color):
        x = x + dx
        y = y + dy
        if self.__emptyOrCanTake(x, y, color):
            return set([(x, y)])
        return set()

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

class Knight(Piece):
    def validMoves(self, board):
        moves = set()

        for one in [-1, +1]:
            for two in [-2, +2]:
                moves.update(board.singleMoveInDirection(self.x, self.y, one, two, self.color))
                moves.update(board.singleMoveInDirection(self.x, self.y, two, one, self.color))

        return moves

class Pawn(Piece):
    def validMoves(self, board):
        startRank = {Colors.White:1, Colors.Black:6}.get(self.color)
        dy = {Colors.White:+1, Colors.Black:-1}.get(self.color)
        moves = set()
        if not board.isOccupied(self.x, self.y + dy):
            moves.add((self.x, self.y + dy))
            if self.y == startRank and not board.isOccupied(self.x, self.y + 2 * dy):
                moves.add((self.x, self.y + 2 * dy))
        for dx in [-1, +1]:
            if board.canTake(self.x + dx, self.y + dy, self.color) or board.enPassantTarget == (self.x + dx, self.y + dy):
                moves.add((self.x + dx, self.y + dy))
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

    def testKnightMovesFromCorner(self):
        knight = Knight(0, 0)
        moves = knight.validMoves(Board());
        expectedMoves = set([(2,1), (1,2)])
        self.assertEqual(expectedMoves, moves)

    def testKnightMoves(self):
        knight = Knight(3, 5)
        moves = knight.validMoves(Board());
        expectedMoves = set([(5,6), (4,7), (1,4), (2,3), (5,4), (4,3), (1,6), (2,7),])
        self.assertEqual(expectedMoves, moves)

    def testKnightMovesWithBlockingPiece(self):
        knight = Knight(0, 0)
        rook = Rook(1,2)
        moves = knight.validMoves(Board(set([knight, rook])));
        expectedMoves = set([(2,1)])
        self.assertEqual(expectedMoves, moves)

    def testKnightTakesRook(self):
        knight = Knight(0, 0, Colors.Black)
        rook = Rook(1,2, Colors.White)
        moves = knight.validMoves(Board(set([knight, rook])));
        expectedMoves = set([(2,1), (1,2)])
        self.assertEqual(expectedMoves, moves)

    def testWhitePawnMovesUp(self):
        pawn = Pawn(3, 3, Colors.White)
        moves = pawn.validMoves(Board())
        expectedMoves = set([(3, 4)])
        self.assertEqual(expectedMoves, moves)

    def testBlackPawnMovesDown(self):
        pawn = Pawn(3, 3, Colors.Black)
        moves = pawn.validMoves(Board())
        expectedMoves = set([(3, 2)])
        self.assertEqual(expectedMoves, moves)

    def testWhitePawnBlocked(self):
        pawn = Pawn(3, 3, Colors.White)
        rook = Rook(3, 4, Colors.Black)
        moves = pawn.validMoves(Board(set([pawn, rook])))
        expectedMoves = set()
        self.assertEqual(expectedMoves, moves)

    def testPawnChargeToRank4(self):
        pawn = Pawn(3, 1, Colors.White)
        moves = pawn.validMoves(Board())
        expectedMoves = set([(3, 2), (3, 3)])
        self.assertEqual(expectedMoves, moves)

    def testBlackPawnCharge(self):
        pawn = Pawn(3, 6, Colors.Black)
        moves = pawn.validMoves(Board())
        expectedMoves = set([(3, 5), (3, 4)])
        self.assertEqual(expectedMoves, moves)

    def testPawnCannotChargeToRank4IfBlocked(self):
        pawn = Pawn(3, 1, Colors.White)
        rook = Rook(3, 2, Colors.Black)
        moves = pawn.validMoves(Board(set([pawn, rook])))
        expectedMoves = set()
        self.assertEqual(expectedMoves, moves)

    def testPawnTakesRook(self):
        pawn = Pawn(3, 3, Colors.White)
        rook = Rook(4, 4, Colors.Black)
        moves = pawn.validMoves(Board(set([pawn, rook])))
        expectedMoves = set([(3, 4), (4, 4)])
        self.assertEqual(expectedMoves, moves)

    def testEnPassant(self):
        pawn = Pawn(3, 4, Colors.White)
        target = (4, 5)
        moves = pawn.validMoves(Board(set(), target))
        expectedMoves = set([(3, 5), (4, 5)])
        self.assertEqual(expectedMoves, moves)
        
        # TODO king, castling, check

if __name__ == '__main__':
    unittest.main()

