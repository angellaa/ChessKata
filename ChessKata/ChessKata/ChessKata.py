import unittest

class Board:
    def isInBoard(x, y):
        BOARDMAX = 7
        BOARDMIN = 0
        return x >= BOARDMIN and x <= BOARDMAX and y >= BOARDMIN and y <= BOARDMAX

class Bishop:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def validMoves(self):
        moves = set()

        moves.update(self.__MovesInDirection(self.x, self.y, +1, +1))
        moves.update(self.__MovesInDirection(self.x, self.y, +1, -1))
        moves.update(self.__MovesInDirection(self.x, self.y, -1, +1))
        moves.update(self.__MovesInDirection(self.x, self.y, -1, -1))

        return moves

    def __MovesInDirection(self, x, y, dx, dy):
        moves = set()
        x += dx
        y += dy
        while (Board.isInBoard(x,y)):
            moves.add((x,y))
            x += dx
            y += dy
        return moves

class Tests(unittest.TestCase):
    
    def testPlaceBishopSomewhere(self):
        bishop = Bishop(3, 5)
        self.assertEqual(3, bishop.x)
        self.assertEqual(5, bishop.y)

    def testWhereCanABishopMove(self):
        bishop = Bishop(3, 5)
        calculatedMoves = bishop.validMoves();
        expectedMoves = set([(2,4),(1,3),(0,2),(4,6),(5,7),(4,4),(5,3),(6,2),(7,1),(2,6),(1,7)])
        self.assertEqual(expectedMoves, calculatedMoves)

    def testWhereCanABishopInTheCornerMove(self):
        bishop = Bishop(0, 0)
        calculatedMoves = bishop.validMoves();
        expectedMoves = set([(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)])
        self.assertEqual(expectedMoves, calculatedMoves)

if __name__ == '__main__':
    unittest.main()

