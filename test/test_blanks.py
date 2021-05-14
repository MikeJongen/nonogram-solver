import sys
import os
import unittest
test_path = os.path.join(os.path.dirname(__file__), '../')   # noqa
sys.path.insert(0, os.path.abspath(test_path))   # noqa

from nonogram_solver.basic.blanks import BlanksSolver, BlanksRowSolver  # noqa: E402


class TestBalancedSolver(unittest.TestCase):
    def test_blanksrow(self):
        clues = [1, 1]
        values = [0] * 15
        values[4] = 1
        values[9] = 1
        expected = [-1] * 15
        expected[4] = 1
        expected[9] = 1
        row = BlanksRowSolver(clues, values)
        row.solve_blanks()
        self.assertEqual(row.values, expected)

    def test_solver(self):
        solver = BlanksSolver(file="test/puzzles/blanks.json")
        solver.solve()
        self.assertTrue(solver.is_complete())
        self.assertTrue(solver.is_correct())


if __name__ == '__main__':
    unittest.main()
