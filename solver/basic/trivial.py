from solver.nonogram import Nonogram
from solver.nonogram import Row


class TrivialSolver(Nonogram):
    """Solver class to solve trivial rows.

    Solves all rows which have a trivial solution.
    This means that, using the row clues, only one solution is possible.
    For example, empty rows or completely filled rows.
    """

    def init_row_solvers(self):
        Nonogram.init_row_solvers(self, TrivialRowSolver)

    def solve(self):
        """only solves rows/columns which have one possible solution"""
        for index, row_solver in enumerate(self.row_solver["y"]):
            changed = row_solver.solve_defined_row()
            if changed:
                self._set_solution_row("y", index, row_solver.values)
        for index, row_solver in enumerate(self.row_solver["x"]):
            changed = row_solver.solve_defined_row()
            if changed:
                self._set_solution_row("x", index, row_solver.values)


class TrivialRowSolver(Row):
    def solve_defined_row(self):
        """
        RowSolver for TrivialSolver class.

        Solves a row/column that has only one possible solution.

        returnvalue : Bool
            A bool to indicate if the row has been changed. (true if changed)
        """
        if self.solved:
            return self.values

        if self.clues == []:
            # empty row
            self.values = [-1 for i in range(self.size)]
            self.solved = True
        elif self.clue_size == self.size:
            # clue fills entire row
            self.values = []
            for block in self.clues:
                self.values.extend([1 for i in range(block)])
                self.values.append(-1)
            del self.values[-1]
            self.solved = True

        return self.solved
