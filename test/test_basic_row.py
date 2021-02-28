from solver.error import *
import solver.basic as basic
import unittest
import sys
import os
test_path = os.path.join(os.path.dirname(__file__), '../')
sys.path.insert(0, os.path.abspath(test_path))


class TestBasicRow(unittest.TestCase):
    def test_solve_defined_row(self):
        row = basic.BasicRowSolver([5, 4], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        row.solve_defined_row()
        self.assertEqual(row.values, [1, 1, 1, 1, 1, -1, 1, 1, 1, 1])

    def test_solve_empty_row(self):
        row = basic.BasicRowSolver([], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        row.solve_defined_row()
        self.assertEqual(row.values, [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1])
