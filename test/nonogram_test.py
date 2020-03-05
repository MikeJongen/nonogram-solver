import sys
import os
test_path = os.path.join(os.path.dirname(__file__), '../solver')
sys.path.insert(0, os.path.abspath(test_path))

import unittest
import nonogram

class TestNonogram(unittest.TestCase):
    def test_init(self):
        new_nonogram = nonogram.Nonogram(5, 5)
        self.assertIsNotNone(new_nonogram)

    def test_size(self):
        new_nonogram = nonogram.Nonogram(5, 10)
        self.assertEqual(new_nonogram.get_size_x(),  5)
        self.assertEqual(new_nonogram.get_size_y(),  10)

    def test_isnotcomplete(self):
        new_nonogram = nonogram.Nonogram(5, 10)
        self.assertFalse(new_nonogram.is_complete())

    def test_legitimateinput(self):
        new_nonogram = nonogram.Nonogram(5, 10)
        clues_x = [[5], [4], [3], [2], [1],\
                   [1] ,[3, 1], [1, 1, 1], [1, 2], [1]]
        clues_y = [[1, 1, 3], [3, 1], [5, 4], [2, 1, 1], [2, 2]]
        new_nonogram.set_clues_x(*clues_x)
        new_nonogram.set_clues_y(*clues_y)

    def test_wrongnumberofinputs(self):
        new_nonogram = nonogram.Nonogram(5, 10)
        clues_x = [[5], [4], [3], [2], [1],\
                   [1] ,[3, 1], [1, 1, 1], [1, 2]]
        clues_y = [[1, 1, 3], [3, 1], [5, 4], [2, 1, 1], [2, 2], [5]]
        self.assertRaises(ValueError, \
                          new_nonogram.set_clues_x, *clues_x)
        self.assertRaises(ValueError, \
                          new_nonogram.set_clues_y, *clues_y)

    def test_wronginputvalue(self):
        new_nonogram = nonogram.Nonogram(5, 10)
        clues_x = [[6], [4], [3], [2], [1],\
                   [1] ,[3, 1], [1, 1, 1], [1, 2], [1]]
        clues_y = [[1, 1, 3, 3], [3, 1], [5, 4], [2, 1, 1], [2, 2]]
        self.assertRaises(ValueError, \
                          new_nonogram.set_clues_x, *clues_x)
        self.assertRaises(ValueError, \
                          new_nonogram.set_clues_y, *clues_y)

if __name__ == '__main__':
    unittest.main()
