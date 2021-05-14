import sys
import os
import unittest
test_path = os.path.join(os.path.dirname(__file__), '../')   # noqa
sys.path.insert(0, os.path.abspath(test_path))   # noqa

import nonogram_solver.nonogram as nonogram  # noqa: E402


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

    def test_update_values(self):
        row = nonogram.Row([3, 4], [0] * 10)
        updated_values_1 = [1, 1, 1, 0, 0, 0, 1, 1, 1, 1]
        updated_values_2 = [1, 1, 1, -1, -1, -1, 1, 1, 1, 1]
        row.update_values(updated_values_1)
        self.assertEqual(row.values, updated_values_1)
        self.assertEqual(row.solved, False)
        row.update_values(updated_values_2)
        self.assertEqual(row.values, updated_values_2)
        self.assertEqual(row.solved, True)

    def test_reset(self):
        row = nonogram.Row([5, 4], [1, 1, 1, 1, 1, -1, 1, 1, 1, 1])
        row.solved = True
        self.assertEqual(row.solved, True)
        row.reset()
        self.assertEqual(row.values, [0] * 10)
        self.assertEqual(row.solved, False)


if __name__ == '__main__':
    unittest.main()
