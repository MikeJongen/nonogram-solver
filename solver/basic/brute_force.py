from solver.nonogram import Nonogram
from solver.nonogram import Row
from solver.error import *


class BruteForceSolver(Nonogram):
    """Brute force solver class

    Performance heavy algorithm, use as last option
    """

    def solve(self):
        # TODO: create
        pass

    def fill_common_elements_row(self, input_axis, index):
        """Fills all elements which are common for all solutions"""
        all_solutions = self.get_all_solutions(input_axis, index)
        row_solution = all_solutions[0]

        for solution in all_solutions:
            row_solution = self._get_matching_solution(solution,
                                                       row_solution)
        self._set_solution_row(input_axis, index, row_solution)

    def _get_matching_solution(self, row1, row2):
        if len(row1) != len(row2):
            raise LengthError
        solution = []
        for value1, value2 in zip(row1, row2):
            if value1 == value2:
                solution.append(value1)
            else:
                solution.append(0)
        return solution


class BruteForceRowSolver(Row):
    def solve_blanks(self):
        """
        RowSolver for BruteForceSolver class

        Tests every possible solution.

        returnvalue : Bool
            A bool to indicate if the row has been changed. (True if changed)
        """
        if self.solved:
            return self.values

        return False

    def _get_number_of_solutions(self):
        """
        Returns the number of possible solutions for the row.
        """

        movement_space = self.size - self.clue_size

        return self._number_of_solutions(movement_space, len(self.clues))

    def _number_of_solutions(self, movement_space, no_clues):
        if no_clues == 1:
            return movement_space + 1
        elif no_clues == 0:
            return 1
        else:
            solutions = 0
            for i in range(movement_space + 1):
                solutions += self._number_of_solutions(i, no_clues - 1)
            return solutions

    def _get_all_solutions(self):
        """
        Returns a list with all possible solutions for the row
        """

        solutions_list = []
        return self._list_of_solutions(solutions_list, [], self.clues, self.size)

    def _list_of_solutions(self, total, start, clue, size):
        if len(clue) == 0:
            # empty row. Return one solution with all empty cells
            total.append([-1] * size)
            return total
        elif len(clue) == 1:
            # one clue left. Check empty cell count, and move clue over these cells
            empty_cells = size - clue[0] + 1
            for empty_start_cells in range(empty_cells):
                solution = start[:]
                solution += [-1] * empty_start_cells
                solution += [1] * clue[0]
                solution += [-1] * (size - clue[0] - empty_start_cells)
                total.append(solution)
            return total
        else:
            # Multiple clues left. Check empty cell count, and move first clue over these cells
            # Then, recursively call this function to find the possible positions of the other clues
            empty_cells = size - clue[0] + 1
            for empty_start_cells in range(empty_cells):
                solution = start[:]
                solution += [-1] * empty_start_cells
                solution += [1] * clue[0]
                solution += [-1]
                new_size = size - clue[0] - empty_start_cells - 1
                total = self._list_of_solutions(total, solution,
                                                clue[1:], new_size)
            return total
