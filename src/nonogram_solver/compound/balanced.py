from nonogram_solver.nonogram import Nonogram, Row
from nonogram_solver.basic.simple_boxes import SimpleBoxesSolver, SimpleBoxesRowSolver
from nonogram_solver.basic.trivial import TrivialSolver, TrivialRowSolver
from nonogram_solver.basic.blanks import BlanksSolver, BlanksRowSolver
from nonogram_solver.basic.brute_force_2 import BruteForceSolver2, BruteForceRowSolver2


class BalancedSolver(BruteForceSolver2, BlanksSolver, TrivialSolver, SimpleBoxesSolver, Nonogram):
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

        solution_changed = True
        while not self.is_complete() and solution_changed:
            solution_changed = False
            self.update_row_solvers()
            solution_changed |= BlanksSolver.solve(self)
            self.update_row_solvers()
            solution_changed |= BruteForceSolver2.solve(self)


class BalancedRowSolver(BruteForceRowSolver2, BlanksRowSolver, TrivialRowSolver, SimpleBoxesRowSolver, Row):
    pass
