from solver.nonogram import Nonogram
from solver.nonogram import Row
from solver.error import *


class BlanksSolver(Nonogram):
    """
    Solver class to fill blanks of completed rows.

    Fills in the blanks of all rows which have all required filled cells.
    """

    def init_row_solvers(self):
        Nonogram.init_row_solvers(self, BlanksRowSolver)

    def solve(self):
        """only solves rows/columns which have one possible solution"""
        for index, row_solver in enumerate(self.row_solver["y"]):
            changed = row_solver.solve_blanks()
            if changed:
                self._set_solution_row("y", index, row_solver.values)
        for index, row_solver in enumerate(self.row_solver["x"]):
            changed = row_solver.solve_blanks()
            if changed:
                self._set_solution_row("x", index, row_solver.values)


class BlanksRowSolver(Row):
    def solve_blanks(self):
        """
        RowSolver for BlanksSolver class

        Fills in the blanks of all rows which have all required filled cells.

        returnvalue : Bool
            A bool to indicate if the row has been changed. (true if changed)
        """
        if self.solved:
            return self.values

        if self._reconstruct_clues() == self.clues:
            for index, value in enumerate(self.values):
                if value == 0:
                    self.values[index] = -1
            return True

        return False
