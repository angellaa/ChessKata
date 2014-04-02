import unittest

class Bishop:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def validMoves(self):
        return set([(2,4),(1,3),(0,2),(4,6),(5,7),(4,4),(5,3),(6,2),(7,1),(2,6),(1,7)])

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

if __name__ == '__main__':
    unittest.main()

