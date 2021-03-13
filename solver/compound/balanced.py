import sys
import os
test_path = os.path.join(os.path.dirname(__file__), '../')  # nopep8
sys.path.insert(0, os.path.abspath(test_path))  # nopep8

from solver.nonogram import Nonogram, Row
from solver.basic.simple_boxes import SimpleBoxesSolver, SimpleBoxesRowSolver
from solver.basic.trivial import TrivialSolver, TrivialRowSolver
from solver.basic.blanks import BlanksSolver, BlanksRowSolver


class BalancedSolver(BlanksSolver, TrivialSolver, SimpleBoxesSolver, Nonogram):
    """
    Solver class to combine all solver classes.
    """

    def init_row_solvers(self):
        Nonogram.init_row_solvers(self, BalancedRowSolver)

    def solve(self):
        """
        Applies several algorithms.
        """
        TrivialSolver.solve(self)
        SimpleBoxesSolver.solve(self)

        if self.is_complete():
            return

        self.update_row_solvers()
        BlanksSolver.solve(self)


class BalancedRowSolver(BlanksRowSolver, TrivialRowSolver, SimpleBoxesRowSolver, Row):
    pass
