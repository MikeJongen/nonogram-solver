import sys
import os
test_path = os.path.join(os.path.dirname(__file__), '../')  # nopep8
sys.path.insert(0, os.path.abspath(test_path))  # nopep8

from solver.error import *
# from solver.solver import NonogramSolver
import unittest


class TestNonogramSolver(unittest.TestCase):
    def test_dummy(self):
        pass


if __name__ == '__main__':
    unittest.main()
