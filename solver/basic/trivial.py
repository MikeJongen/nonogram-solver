from solver.nonogram import Nonogram
from solver.nonogram import Row
from solver.error import *


class TrivialSolver(Nonogram):
    """Solver class to solve trivial rows.

    Solves all rows which have a trivial solution. 
    This means that, using the row clues, only one solution is possible.
    For example, empty rows or completely filled rows.
    """

    def solve(self):
        """only solves rows/columns which have one possible solution"""
        for index in range(self.size[self.y]):
            try:
                row = TrivialRowSolver(
                    *self.get_clue_solution_pair("x", index))
                row_solution = row.solve_defined_row()
                self._set_solution_row(self.x, index, row_solution)
            except SolveError:
                pass
        for index in range(self.size[self.x]):
            try:
                row = TrivialRowSolver(
                    *self.get_clue_solution_pair("y", index))
                row_solution = row.solve_defined_row()
                self._set_solution_row(self.y, index, row_solution)
            except SolveError:
                pass


class TrivialRowSolver(Row):
    def solve_defined_row(self):
        """
        RowSolver for TrivialSolver class

        Solves a row/column that has only one possible solution
        """
        if self.is_complete():
            return self.values

        length_clue = sum(self.clues) + len(self.clues) - 1

        if self.clues == []:
            # empty row
            self.values = [-1 for i in range(self.size)]
        elif length_clue == self.size:
            # clue fills entire row
            self.values = []
            for block in self.clues:
                self.values.extend([1 for i in range(block)])
                self.values.append(-1)
            del self.values[-1]
        else:
            raise SolveError

        return self.values
