import sys
import os
test_path = os.path.join(os.path.dirname(__file__), '../')  # nopep8
sys.path.insert(0, os.path.abspath(test_path))  # nopep8

from solver.error import *
import solver.basic.basic as basic
import unittest


class TestBasicRow(unittest.TestCase):
    def test_solve_defined_row(self):
        row = basic.BasicRowSolver([5, 4], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        row.solve_defined_row()
        self.assertEqual(row.values, [1, 1, 1, 1, 1, -1, 1, 1, 1, 1])

    def test_solve_empty_row(self):
        row = basic.BasicRowSolver([], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        row.solve_defined_row()
        self.assertEqual(row.values, [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1])


if __name__ == '__main__':
    unittest.main()
