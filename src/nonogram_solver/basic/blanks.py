from nonogram_solver.nonogram import Nonogram
from nonogram_solver.nonogram import Row


class BlanksSolver(Nonogram):
    """
    Solver class to fill blanks of completed rows.

    Fills in the blanks of all rows which have all required filled cells.
    """

    def init_row_solvers(self):
        Nonogram.init_row_solvers(self, BlanksRowSolver)

    def solve(self):
        """
        Returns True if anything was changed to the solution.
        """
        return self.solve_single_iteration(BlanksRowSolver.solve_blanks)


class BlanksRowSolver(Row):
    def solve_blanks(self):
        """
        RowSolver for BlanksSolver class

        Fills in the blanks of all rows which have all required filled cells.

        returnvalue : Bool
            A bool to indicate if the row has been changed. (true if changed)
        """
        if self.solved:
            return False

        if self._reconstruct_clues() == self.clues:
            for index, value in enumerate(self.values):
                if value == 0:
                    self.values[index] = -1
            self.solved = True
            return True

        return False
