from solver.nonogram import Nonogram, Row
from solver.basic.brute_force_2 import BruteForceSolver2, BruteForceRowSolver2


class OnlyBruteForceSolver(BruteForceSolver2, Nonogram):
    """
    Only uses brute force.
    """

    def init_row_solvers(self):
        Nonogram.init_row_solvers(self, OnlyBruteForceRowSolver)

    def solve(self):
        """
        Only uses brute force.
        """

        first_loop = True

        while not self.is_complete():
            if not first_loop:
                self.update_row_solvers()
            BruteForceSolver2.solve(self)
            first_loop = False


class OnlyBruteForceRowSolver(BruteForceRowSolver2, Row):
    pass
