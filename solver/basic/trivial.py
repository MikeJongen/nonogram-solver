from solver.nonogram import Nonogram
from solver.nonogram import Row
from solver.error import *


class TrivialSolver(Nonogram):
    """Solver class to solve trivial rows.

    Solves all rows which have a trivial solution. 
    This means that, using the row clues, only one solution is possible.
    For example, empty rows or completely filled rows.
    """

    def __init__(self, size_x=0, size_y=0, file=None):
        Nonogram.__init__(self, size_x, size_y, file)

        self.row_solver_y = []
        self.row_solver_x = []
        for index in range(self.size["y"]):
            self.row_solver_y.append(TrivialRowSolver(
                *self.get_clue_solution_pair("x", index)))
        for index in range(self.size["x"]):
            self.row_solver_x.append(TrivialRowSolver(
                *self.get_clue_solution_pair("y", index)))

    def solve(self):
        """only solves rows/columns which have one possible solution"""
        for index, row_solver in enumerate(self.row_solver_y):
            changed = row_solver.solve_defined_row()
            if changed:
                self._set_solution_row("x", index, row_solver.values)
        for index, row_solver in enumerate(self.row_solver_x):
            changed = row_solver.solve_defined_row()
            if changed:
                self._set_solution_row("y", index, row_solver.values)


class TrivialRowSolver(Row):
    def solve_defined_row(self):
        """
        RowSolver for TrivialSolver class

        Solves a row/column that has only one possible solution

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
