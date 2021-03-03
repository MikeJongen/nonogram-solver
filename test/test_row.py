import sys
import os
test_path = os.path.join(os.path.dirname(__file__), '../')  # nopep8
sys.path.insert(0, os.path.abspath(test_path))  # nopep8

from solver.error import *
import solver.nonogram as nonogram
import unittest


class TestRow(unittest.TestCase):
    def test_init(self):
        row = nonogram.Row([5, 4], [1, 1, 1, 1, 1, -1, 1, 1, 1, 1])
        self.assertEqual(row.clues, [5, 4])
        self.assertEqual(row.values, [1, 1, 1, 1, 1, -1, 1, 1, 1, 1])
        self.assertEqual(row.size, 10)

    def test_reconstruct_clues(self):
        original_clues = [5, 4]
        row = nonogram.Row(original_clues, [1, 1, 1, 1, 1, -1, 1, 1, 1, 1])
        new_clues = row._reconstruct_clues()
        self.assertEqual(new_clues, original_clues)

    def test_is_complete(self):
        row = nonogram.Row([5, 4], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertFalse(row.is_complete())
        row.values = [1, 1, 1, 1, 0, -1, 1, 1, 1, 1]
        self.assertFalse(row.is_complete())
        row.values = [1, 1, 1, 1, 1, -1, 1, 1, 1, 1]
        self.assertTrue(row.is_complete())

    def test_is_correct(self):
        row = nonogram.Row([5, 4], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertFalse(row.is_correct())
        row.values = [1, 1, 1, 1, -1, -1, 1, 1, 1, 1]
        self.assertFalse(row.is_correct())
        row.values = [1, 1, 1, 1, 1, -1, 1, 1, 1, 1]
        self.assertTrue(row.is_correct())

    def test_reset(self):
        row = nonogram.Row([5, 4], [1, 1, 1, 1, 1, -1, 1, 1, 1, 1])
        row.solved = True
        self.assertEqual(row.solved, True)
        row.reset()
        self.assertEqual(row.values, [0] * 10)
        self.assertEqual(row.solved, False)


if __name__ == '__main__':
    unittest.main()
