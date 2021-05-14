import sys
import os
import unittest
test_path = os.path.join(os.path.dirname(__file__), '../')   # noqa
sys.path.insert(0, os.path.abspath(test_path))   # noqa

from nonogram_solver.compound.balanced import BalancedSolver  # noqa: E402


class TestBalancedSolver(unittest.TestCase):
    def test_solver(self):
        solver = BalancedSolver(file="test/puzzles/trivial.json")
        solver.solve()
        self.assertGreaterEqual(solver.percent_complete(), 88)

    def test_solver_update(self):
        solver = BalancedSolver(file="test/puzzles/edge.json")
        solver.solve()
        self.assertTrue(solver.is_complete())
        self.assertTrue(solver.is_correct())


if __name__ == '__main__':
    unittest.main()
