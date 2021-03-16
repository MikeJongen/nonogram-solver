from solver.nonogram import Nonogram
from solver.nonogram import Row


class SimpleBoxesSolver(Nonogram):
    """
    Solver class to apply simple boxes algorithm.
    """

    def init_row_solvers(self):
        Nonogram.init_row_solvers(self, SimpleBoxesRowSolver)

    def solve(self):
        """
        Applies simple boxes algorithm to rows.

        Does not require to update rows before solving, as this algorithm
        does not use information from the solution.
        """
        return self.solve_single_iteration(SimpleBoxesRowSolver.solve_simple_boxes)


class SimpleBoxesRowSolver(Row):
    def solve_simple_boxes(self):
        """
        RowSolver for SimpleBoxesSolver class

        Applies simple boxes algorithm to row

        returnvalue : Bool
            A bool to indicate if the row has been changed. (true if changed)
        """
        if self.solved:
            return False

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
