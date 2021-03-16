from solver.nonogram import Nonogram, Row
from solver.basic.simple_boxes import SimpleBoxesSolver, SimpleBoxesRowSolver
from solver.basic.trivial import TrivialSolver, TrivialRowSolver
from solver.basic.blanks import BlanksSolver, BlanksRowSolver
from solver.basic.brute_force import BruteForceSolver, BruteForceRowSolver


class BalancedSolver(BruteForceSolver, BlanksSolver, TrivialSolver, SimpleBoxesSolver, Nonogram):
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
            solution_changed |= BruteForceSolver.solve(self)


class BalancedRowSolver(BruteForceRowSolver, BlanksRowSolver, TrivialRowSolver, SimpleBoxesRowSolver, Row):
    pass
