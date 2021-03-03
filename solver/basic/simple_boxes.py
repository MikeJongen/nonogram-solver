from solver.nonogram import Nonogram
from solver.nonogram import Row
from solver.error import *


class SimpleBoxesSolver(Nonogram):
    """
    Solver class to apply simple boxes algorithm.
    """

    def __init__(self, size_x=0, size_y=0, file=None):
        Nonogram.__init__(self, size_x, size_y, file)

        self.row_solver_y = []
        self.row_solver_x = []
        for index in range(self.size["y"]):
            self.row_solver_y.append(SimpleBoxesRowSolver(
                *self.get_clue_solution_pair("x", index)))
        for index in range(self.size["x"]):
            self.row_solver_x.append(SimpleBoxesRowSolver(
                *self.get_clue_solution_pair("y", index)))

    def solve(self):
        """
        Applies simple boxes algorithm to rows.

        Does not require to update rows before solving, as this algorithm
        does not use information from the solution.
        """
        for index, row_solver in enumerate(self.row_solver_y):
            changed = row_solver.solve_simple_boxes()
            if changed:
                self._set_solution_row("x", index, row_solver.values)
        for index, row_solver in enumerate(self.row_solver_x):
            changed = row_solver.solve_simple_boxes()
            if changed:
                self._set_solution_row("y", index, row_solver.values)


class SimpleBoxesRowSolver(Row):
    def solve_simple_boxes(self):
        """
        RowSolver for SimpleBoxesSolver class

        Applies simple boxes algorithm to row

        returnvalue : Bool
            A bool to indicate if the row has been changed. (true if changed)
        """
        if self.solved:
            return self.values

        movement_space = self.size - self.clue_size

        if len(self.clues) == 0:
            # simple box does not work with empty list
            # and max gives error on empty list
            return False

        if movement_space >= max(self.clues):
            # clues too small for simple boxes to work
            return False

        for index, clue in enumerate(self.clues):
            if movement_space < clue:
                self._simple_boxes_clue(index, clue)

        return True

    def _simple_boxes_clue(self, index, clue):
        """
        Apply simple box for clue at given index
        """

        # lowest row index where clue can be placed
        minimum = 0
        for other_clue in self.clues[:index]:
            minimum += other_clue
            minimum += 1  # space between clues

        # highest row index where clue can be placed
        maximum = self.size
        for other_clue in self.clues[index+1:]:
            maximum -= other_clue
            maximum -= 1  # space between clues

        # start and stop index of the spaces that need to be filled
        start_fill = maximum - clue
        stop_fill = minimum + clue

        self.values[start_fill:stop_fill] = [1] * (stop_fill - start_fill)
