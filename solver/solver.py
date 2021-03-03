import sys
import os
test_path = os.path.join(os.path.dirname(__file__), '../')  # nopep8
sys.path.insert(0, os.path.abspath(test_path))  # nopep8

from solver import nonogram
from solver.basic import trivial
from solver.basic import simple_boxes


class NonogramSolver(nonogram, trivial, simple_boxes):
    pass
