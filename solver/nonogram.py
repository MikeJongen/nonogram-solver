import json

class Nonogram:
    """Main nonogram class

    Used to hold the data of the nonogram.
    also has some basic creation and helper functions
    """
    printable_values = {-1: "  ",
                         0: "..",
                         1: "XX"}
    axis = {"x": 0,
            "y": 1}

    x = axis["x"]
    y = axis["y"]

    def __init__(self, size_x=0, size_y=0, file=None):
        if file == None:
            # Create empty Nonogram
            self.size = [0, 0]
            self.size[self.x] = size_x
            self.size[self.y] = size_y

            self.solution = [[-1 for y in range(self.get_size_y())]\
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
        return self.set_clues("x", *clues)

    def set_clues_y(self, *clues):
        return self.set_clues("y", *clues)

    def set_clues(self, input_axis, *clues):
        cur_axis = self.axis[input_axis]
        other_axis = not cur_axis

        if len(clues) != self.size[other_axis]:
            raise ValueError
        for index, clue in enumerate(clues):
            min_length_clue = sum(clue) + len(clue) - 1
            if(min_length_clue > self.size[cur_axis]):
                raise ValueError
            self.clues[cur_axis][index] = clue

    def is_complete(self):
        result = all(x != -1 for row in self.solution for x in row)
        return result

    def percent_complete(self):
        size = self.size[self.x] * self.size[self.y]
        empty_elements = 0
        for row in self.solution:
            for element in row:
                if element == -1:
                    empty_elements += 1
        filled_elements = size - empty_elements
        percent_complete = (filled_elements / size) * 100
        return percent_complete

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

    def _set_solution_row(self, input_axis, row_index, solution_row):
        if input_axis == self.y:
            self.solution[row_index] = solution_row
        elif input_axis == self.x:
            for index, value in enumerate(solution_row):
                self.solution[index][row_index] = value
        else:
            raise ValueError
