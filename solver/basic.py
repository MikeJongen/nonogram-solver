from nonogram import Nonogram

class BasicSolver(Nonogram):
    """simple solver class

    First try at a solver class.
    """
    def solve_defined_row(self, input_axis, index):
        """Solves a row/column that has only one possible solution"""
        cur_axis = self.axis[input_axis]
        cur_clue = self.clues[cur_axis][index]
        length_clue = sum(cur_clue) + len(cur_clue) - 1

        if cur_clue == []:
            # empty row
            row_solution = [0 for i in range(self.size[cur_axis])]
        elif length_clue == self.size[cur_axis]:
            # clue fills entire row
            row_solution = []
            for block in cur_clue:
                row_solution.extend([1 for i in range(block)])
                row_solution.append(0)
            del row_solution[-1]
        else:
            raise ValueError

        self._set_solution_row(cur_axis, index, row_solution)

    def get_number_of_solutions_total(self, input_axis, index):
        """Returns the number of possible solutions for the row"""
        cur_axis = self.axis[input_axis]
        cur_clue = self.clues[cur_axis][index]
        length_clue = sum(cur_clue) + len(cur_clue) - 1
        empty_spaces = self.size[cur_axis] - length_clue
        no_clues = len(cur_clue)

        return self._number_of_solutions(empty_spaces, no_clues)

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
