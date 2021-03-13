import sys
import os
import unittest
test_path = os.path.join(os.path.dirname(__file__), '../')   # noqa
sys.path.insert(0, os.path.abspath(test_path))   # noqa

import solver.basic.trivial as trivial  # noqa: E402


class TestTrivial(unittest.TestCase):
    def test_solve_defined_row(self):
        row = trivial.TrivialRowSolver([5, 4], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        row.solve_defined_row()
        self.assertEqual(row.values, [1, 1, 1, 1, 1, -1, 1, 1, 1, 1])

    def test_solve_empty_row(self):
        row = trivial.TrivialRowSolver([], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        row.solve_defined_row()
        self.assertEqual(row.values, [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1])

    def test_solver1(self):
        new_nonogram = \
            trivial.TrivialSolver(file="test/puzzles/trivial.json")
        new_nonogram.solve()
        expected_solution = [[1,  1,  1,  1,  1],
                             [-1, -1, -1, -1, -1],
                             [1,  1,  1, -1,  1],
                             [1, -1,  1, -1,  1],
                             [0,  1,  0,  0,  1]]
        self.assertEqual(new_nonogram.solution, expected_solution)


if __name__ == '__main__':
    unittest.main()
