import sys
import os
import unittest

from nonogram_solver.compound.balanced import BalancedSolver


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
