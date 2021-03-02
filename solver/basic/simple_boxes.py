from solver.nonogram import Nonogram
from solver.nonogram import Row
from solver.error import *


class SimpleBoxesSolver(Nonogram):
    """
    Solver class to apply simple boxes algorithm.
    """

    def solve(self):
        """only solves rows/columns which have one possible solution"""
        for index in range(self.size["y"]):
            row = SimpleBoxesRowSolver(
                *self.get_clue_solution_pair("x", index))
            changed = row.solve_simple_boxes()
            if changed:
                self._set_solution_row("x", index, row.values)
        for index in range(self.size["x"]):
            row = SimpleBoxesRowSolver(
                *self.get_clue_solution_pair("y", index))
            changed = row.solve_simple_boxes()
            if changed:
                self._set_solution_row("y", index, row.values)


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
