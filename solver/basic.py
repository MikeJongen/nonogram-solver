from solver.nonogram import Nonogram
from solver.nonogram import Row
from solver.error import *


class BasicSolver(Nonogram):
    """simple solver class

    First try at a solver class.
    """

    def solver1(self):
        """only solves rows/columns which have one possible solution"""
        for index in range(self.size[self.y]):
            try:
                self.solve_defined_row("x", index)
            except SolveError:
                pass
        for index in range(self.size[self.x]):
            try:
                self.solve_defined_row("y", index)
            except SolveError:
                pass

    def solve_defined_row(self, input_axis, index):
        """Solves a row/column that has only one possible solution"""
        cur_axis = self.axis[input_axis]
        cur_clue = self.clues[cur_axis][index]
        length_clue = sum(cur_clue) + len(cur_clue) - 1

        if cur_clue == []:
            # empty row
            row_solution = [-1 for i in range(self.size[cur_axis])]
        elif length_clue == self.size[cur_axis]:
            # clue fills entire row
            row_solution = []
            for block in cur_clue:
                row_solution.extend([1 for i in range(block)])
                row_solution.append(-1)
            del row_solution[-1]
        else:
            raise SolveError

        self._set_solution_row(cur_axis, index, row_solution)

    def fill_common_elements_row(self, input_axis, index):
        """Fills all elements which are common for all solutions"""
        cur_axis = self.axis[input_axis]
        all_solutions = self.get_all_solutions(input_axis, index)
        row_solution = all_solutions[0]

        for solution in all_solutions:
            row_solution = self._get_matching_solution(solution,
                                                       row_solution)
        self._set_solution_row(cur_axis, index, row_solution)

    def get_number_of_solutions_total(self, input_axis, index):
        """Returns the number of possible solutions for the row"""
        cur_axis = self.axis[input_axis]
        cur_clue = self.clues[cur_axis][index]
        length_clue = sum(cur_clue) + len(cur_clue) - 1
        empty_spaces = self.size[cur_axis] - length_clue
        no_clues = len(cur_clue)

        return self._number_of_solutions(empty_spaces, no_clues)

    def get_all_solutions(self, input_axis, index):
        """Returns a list with all possible solutions for the row"""
        cur_axis = self.axis[input_axis]
        cur_clue = self.clues[cur_axis][index]
        row_size = self.size[cur_axis]

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

    def _number_of_solutions(self, empty_spaces, no_clues):
        if no_clues == 1:
            return empty_spaces + 1
        elif no_clues == 0:
            return 1
        else:
            solutions = 0
            for i in range(empty_spaces + 1):
                solutions += self._number_of_solutions(i, no_clues - 1)
            return solutions

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


class BasicRowSolver(Row):
    def solve_defined_row(self):
        """
        Solves a row/column that has only one possible solution
        """
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
