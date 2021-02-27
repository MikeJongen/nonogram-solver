from solver.error import *
import solver.nonogram as nonogram
import unittest
import sys
import os
test_path = os.path.join(os.path.dirname(__file__), '../')
sys.path.insert(0, os.path.abspath(test_path))


class TestRow(unittest.TestCase):
    def test_init(self):
        row = nonogram.Row([5, 4], [1, 1, 1, 1, 1, -1, 1, 1, 1, 1])
        self.assertEqual(row.clues, [5, 4])
        self.assertEqual(row.values, [1, 1, 1, 1, 1, -1, 1, 1, 1, 1])

    def test_reconstruct_clues(self):
        original_clues = [5, 4]
        row = nonogram.Row(original_clues, [1, 1, 1, 1, 1, -1, 1, 1, 1, 1])
        new_clues = row._reconstruct_clues()
        self.assertEqual(new_clues, original_clues)
