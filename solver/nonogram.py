import json
from solver.error import *


class Nonogram:
    """Main nonogram class

    Used to hold the data of the nonogram.
    also has some basic creation and helper functions
    """
    printable_values = {0: "  ",
                        -1: "..",
                        1: "XX"}

    def __init__(self, size_x=0, size_y=0, file=None):
        """
        Initializes using file or puzzle size
        """
        self.clues = dict()
        self.size = dict()

        if file == None:
            # Create empty Nonogram
            self.size["x"] = size_x
            self.size["y"] = size_y

            self.solution = [[0 for y in range(self.size["y"])]
                             for x in range(self.size["x"])]
            self.clues["x"] = [[] for x in range(self.size["y"])]
            self.clues["y"] = [[] for y in range(self.size["x"])]
        else:
            # Load from file
            self.load(file)

        self.init_row_solvers()

    def init_row_solvers(self, solver_class=None):
        if None == solver_class:
            # Use default
            solver_class = Row
        self.row_solver = dict()
        self.row_solver["x"] = []
        self.row_solver["y"] = []
        for index in range(self.size["y"]):
            self.row_solver["x"].append(solver_class(
                *self.get_clue_solution_pair("x", index)))
        for index in range(self.size["x"]):
            self.row_solver["y"].append(solver_class(
                *self.get_clue_solution_pair("y", index)))

    def set_clues_x(self, *clues):
        """
        Sets clues of for the rows

        *clues : list
            list of clues, where every clue is a list of ints
        """
        return self.set_clues("x", *clues)

    def set_clues_y(self, *clues):
        """
        Sets clues of for the columns

        *clues : list
            list of clues, where every clue is a list of ints
        """
        return self.set_clues("y", *clues)

    def set_clues(self, input_axis, *clues):
        """
        Sets clues

        input_axis : string
            "x" if clues are for rows
            "y" if clues are for columns
        *clues : list
            list of clues, where every clue is a list of ints
        """
        if len(clues) != self.size[self._other_axis(input_axis)]:
            raise LengthError
        for index, clue in enumerate(clues):
            min_length_clue = sum(clue) + len(clue) - 1
            if(min_length_clue > self.size[input_axis]):
                raise ClueError
            self.clues[input_axis][index] = clue
        self.init_row_solvers()

    def get_clue_solution_pair(self, axis, row_index):
        clues = self.clues[axis][row_index]
        values = self._get_solution_row(axis, row_index)
        return (clues, values)

    def update_row_solvers(self):
        for axis in self.row_solver:
            for index, row_solver in enumerate(self.row_solver[axis]):
                if row_solver.solved:
                    # don't waste time updating completed rows
                    continue
                row_solver.update_values(self._get_solution_row(axis, index))

    def is_complete(self) -> bool:
        """
        Checks if puzzle is completely filled in (no unknown values left)
        """
        result = all(x != 0 for row in self.solution for x in row)
        return result

    def percent_complete(self) -> float:
        """
        Returns percentage filled in cells / total cells
        """
        filled_elements = self.cells_known()
        percent_complete = (filled_elements / self.total_cells()) * 100
        return percent_complete

    def total_cells(self):
        return self.size["x"] * self.size["y"]

    def cells_known(self):
        """
        Returns total amoutn of cells where the value (filled/blank) is known.
        """
        empty_elements = 0
        for row in self.solution:
            for element in row:
                if element == 0:
                    empty_elements += 1
        return self.total_cells() - empty_elements

    def is_correct(self) -> bool:
        """
        Checks if puzzle solution fits the clues
        """
        correct = True
        for row_index in range(self.size["y"]):
            row = Row(*self.get_clue_solution_pair("x", row_index))
            if not row.is_correct():
                correct = False
        for col_index in range(self.size["x"]):
            row = Row(*self.get_clue_solution_pair("y", col_index))
            if not row.is_correct():
                correct = False
        return correct

    def reset_solution(self):
        self.solution = [[0 for y in range(self.size["y"])]
                         for x in range(self.size["x"])]
        if self.row_solver is not None:
            for solver in self.row_solver["y"]:
                solver.reset()
            for solver in self.row_solver["x"]:
                solver.reset()

    def print_solution(self):
        top_row = "+" + self.size["x"] * "--+"
        print(top_row)
        for y in range(self.size["y"]):
            row = "|"
            for x in range(self.size["x"]):
                row += f"{self.printable_values[self.solution[x][y]]}|"
            print(row)
            print(top_row)

    def print_clues(self):
        print("Horizontal clues:")
        for clue in self.clues["x"]:
            print(clue)
        print("Vertical clues:")
        for clue in self.clues["y"]:
            print(clue)

    def save(self, file, only_clues=False):
        file = open(file, 'w')
        if only_clues:
            data = {"clues": self.clues}
        else:
            data = {"clues": self.clues,
                    "solution": self.solution}
        json.dump(data, file)
        file.close()

    def load(self, file):
        file = open(file, 'r')
        data = json.load(file)
        self.clues = data["clues"]
        self.size["x"] = len(self.clues["x"])
        self.size["y"] = len(self.clues["y"])
        if "solution" in data:
            self.solution = data["solution"]
        else:
            self.solution = [[0 for y in range(self.size["y"])]
                             for x in range(self.size["x"])]
        file.close()

    def _other_axis(self, axis):
        if axis == "x":
            return "y"
        elif axis == "y":
            return "x"
        else:
            raise AxisError

    def _set_solution_row(self, axis, row_index, solution_row,
                          forced=False):
        """
        sets row/column to new value.

        solution_row : list
            list of int with new values.
        forced : bool
            if True, overwrite old values.
        """
        if axis == "y":
            for index, value in enumerate(solution_row):
                self._set_solution_value(row_index, index, value,
                                         forced)
        elif axis == "x":
            for index, value in enumerate(solution_row):
                self._set_solution_value(index, row_index, value,
                                         forced)
        else:
            raise AxisError

    def _set_solution_value(self, x, y, new, forced=False):
        """
        Sets the value of cell [x, y] to new.
        Only sets value if previous value was empty (unless forced == True).
        """
        value = self.solution[x][y]
        if forced:
            self.solution[x][y] = new
        else:
            if value == 0:
                self.solution[x][y] = new
            elif ((value, new) == (-1, 1)) or ((value, new) == (1, -1)):
                raise SetSolutionError

    def _get_solution_row(self, axis, row_index) -> list:
        """
        Get a copy of a row/column of the solution
        """
        if axis == "y":
            row = []
            for value in self.solution[row_index]:
                row.append(value)
            return row
        elif axis == "x":
            row = []
            for value in self.solution:
                row.append(value[row_index])
            return row
        else:
            raise AxisError


class Row:
    """
    Support class

    used for data/function for a single row/column
    """

    def __init__(self, clues, values):
        self.clues = clues
        self.values = values
        self.size = len(self.values)
        self.solved = False
        self.clue_size = sum(self.clues) + len(self.clues) - 1

    def _reconstruct_clues(self) -> list:
        """
        Get clue list, created from the current state of the row
        Interprets empty cells as blank
        """
        clues = []
        current_clue = 0
        for element in self.values:
            if element == 1:
                current_clue += 1
            elif current_clue != 0:
                clues.append(current_clue)
                current_clue = 0
        if current_clue != 0:
            clues.append(current_clue)
        return clues

    def is_complete(self) -> bool:
        """
        Checks if row is completely filled in (no unknown values left)
        """
        result = all(value != 0 for value in self.values)
        return result

    def is_correct(self) -> bool:
        """
        Checks if row solution fits the clues
        Non complete solution is interpreted as incorrect
        """
        if not self.is_complete():
            return False
        reconstructed_clue = self._reconstruct_clues()
        if reconstructed_clue != self.clues:
            return False
        return True

    def update_values(self, values):
        self.values = values
        if self.is_complete():
            self.solved = True

    def reset(self):
        self.values = [0] * self.size
        self.solved = False
