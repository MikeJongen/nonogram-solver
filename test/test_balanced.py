import sys
import os
test_path = os.path.join(os.path.dirname(__file__), '../')  # nopep8
sys.path.insert(0, os.path.abspath(test_path))  # nopep8

from solver.error import *
from solver.compound.balanced import BalancedSolver
import unittest


class TestBalancedSolver(unittest.TestCase):
    def test_solver(self):
        solver = BalancedSolver(file="test/puzzles/nonogram_trivial.json")
        solver.solve()
        self.assertGreaterEqual(solver.percent_complete(), 88)


if __name__ == '__main__':
    unittest.main()
