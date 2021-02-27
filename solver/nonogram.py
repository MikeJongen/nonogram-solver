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
    axis = {"x": 0,
            "y": 1}

    x = axis["x"]
    y = axis["y"]

    def __init__(self, size_x=0, size_y=0, file=None):
        """
        Initializes using file or puzzle size
        """
        if file == None:
            # Create empty Nonogram
            self.size = [0, 0]
            self.size[self.x] = size_x
            self.size[self.y] = size_y

            self.solution = [[0 for y in range(self.get_size_y())]
                             for x in range(self.get_size_x())]
            self.clues = [0, 0]
            self.clues[self.x] = [[] for x in range(self.get_size_y())]
            self.clues[self.y] = [[] for y in range(self.get_size_x())]
        else:
            # Load from file
            self.load(file)

    def get_size_x(self):
        return self.size[self.x]

    def get_size_y(self):
        return self.size[self.y]

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
        cur_axis = self.axis[input_axis]
        other_axis = not cur_axis

        if len(clues) != self.size[other_axis]:
            raise LengthError
        for index, clue in enumerate(clues):
            min_length_clue = sum(clue) + len(clue) - 1
            if(min_length_clue > self.size[cur_axis]):
                raise ClueError
            self.clues[cur_axis][index] = clue

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
        size = self.size[self.x] * self.size[self.y]
        empty_elements = 0
        for row in self.solution:
            for element in row:
                if element == 0:
                    empty_elements += 1
        filled_elements = size - empty_elements
        percent_complete = (filled_elements / size) * 100
        return percent_complete

    def is_correct(self) -> bool:
        """
        Checks if puzzle solution fits the clues
        """
        correct = True
        for row_index in range(self.get_size_y()):
            derived_clue = self._get_clues_from_row(self.x, row_index)
            if derived_clue != self.clues[self.x][row_index]:
                correct = False
        for col_index in range(self.get_size_x()):
            derived_clue = self._get_clues_from_row(self.y, col_index)
            if derived_clue != self.clues[self.y][col_index]:
                correct = False
        return correct

    def print_solution(self):
        top_row = "+" + self.get_size_x() * "--+"
        print(top_row)
        for y in range(self.get_size_y()):
            row = "|"
            for x in range(self.get_size_x()):
                row += f"{self.printable_values[self.solution[x][y]]}|"
            print(row)
            print(top_row)

    def print_clues(self):
        print("Horizontal clues:")
        for clue in self.clues[self.x]:
            print(clue)
        print("Vertical clues:")
        for clue in self.clues[self.y]:
            print(clue)

    def save(self, filename):
        file = open(filename, 'w')
        data = self.size, self.solution, self.clues
        json.dump(data, file)
        file.close()

    def load(self, filename):
        file = open(filename, 'r')
        data = json.load(file)
        self.size, self.solution, self.clues = data
        file.close()

    def _set_solution_row(self, input_axis, row_index, solution_row,
                          forced=True):
        """
        sets row/column to new value.

        solution_row : list
            list of int with new values.
        forced : bool
            if True, overwrite old values.
        """
        if input_axis == self.y:
            for index, value in enumerate(solution_row):
                self._set_solution_value(row_index, index, value,
                                         forced)
        elif input_axis == self.x:
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

    def _get_solution_row(self, input_axis, row_index) -> list:
        """
        Get a copy of a row/column of the solution
        """
        if input_axis == self.y:
            row = []
            for value in self.solution[row_index]:
                row.append(value)
            return row
        elif input_axis == self.x:
            row = []
            for value in self.solution:
                row.append(value[row_index])
            return row
        else:
            raise AxisError

    def _get_clues_from_row(self, input_axis, row_index) -> list:
        """
        Get clue list, created from the current state of the solution
        """
        row = self._get_solution_row(input_axis, row_index)
        clues = []
        current_clue = 0
        for element in row:
            if element == 1:
                current_clue += 1
            elif current_clue != 0:
                clues.append(current_clue)
                current_clue = 0
        if current_clue != 0:
            clues.append(current_clue)
        return clues


class Row:
    """
    Support class

    used for data/function for a single row/column
    """

    def __init__(self, clues, values):
        self.clues = clues
        self.values = values

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
