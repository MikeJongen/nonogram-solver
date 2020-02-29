from solver.nonogram import Nonogram

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
