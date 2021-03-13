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

    def get_all_solutions(self, input_axis, index):
        """Returns a list with all possible solutions for the row"""
        cur_clue = self.clues[input_axis][index]
        row_size = self.size[input_axis]

        solutions_list = []
        return self._list_of_solutions(solutions_list, [],
                                       cur_clue, row_size)

    def _list_of_solutions(self, total, start, clue, size):
        if len(clue) == 0:
            solution = []
            for i in range(size):
                solution.append(-1)
            total.append(solution)
            return total
        elif len(clue) == 1:
            no_solutions = size - clue[0] + 1
            for solution_no in range(no_solutions):
                solution = start[:]
                for i in range(solution_no):
                    solution.append(-1)
                for i in range(clue[0]):
                    solution.append(1)
                for i in range(size - clue[0] - solution_no):
                    solution.append(-1)
                total.append(solution)
            return total
        else:
            no_solutions = size - clue[0] + 1
            for solution_no in range(no_solutions):
                solution = start[:]
                for i in range(solution_no):
                    solution.append(-1)
                for i in range(clue[0]):
                    solution.append(1)
                solution.append(-1)
                new_size = size - clue[0] - solution_no - 1
                total = self._list_of_solutions(total, solution,
                                                clue[1:], new_size)
            return total

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
