import unittest

class Bishop:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Tests(unittest.TestCase):

    def testPlaceBishopSomewhere(self):
        bishop = Bishop(3, 5)
        self.assertEqual(3, bishop.x)
        self.assertEqual(5, bishop.y)


if __name__ == '__main__':
    unittest.main()

