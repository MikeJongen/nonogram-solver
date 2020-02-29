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

    def __init__(self, size_x, size_y):
        self.size = [0, 0]
        self.size[self.x] = size_x
        self.size[self.y] = size_y

        self.solution = [[-1 for y in range(self.size[self.y])]\
                             for x in range(self.size[self.x])]
        self.clues = [0, 0]
        self.clues[self.x] = [[] for x in range(self.size[self.x])]
        self.clues[self.y] = [[] for y in range(self.size[self.y])]

    def set_clues_x(self, *clues):
        return self.set_clues("x", *clues)

    def set_clues_y(self, *clues):
        return self.set_clues("y", *clues)

    def set_clues(self, input_axis, *clues):
        cur_axis = self.axis[input_axis]

        if len(clues) != self.size[cur_axis]:
            raise ValueError
        for index, clue in enumerate(clues):
            min_length_clue = sum(clue) + len(clue) - 1
            if(min_length_clue > self.size[cur_axis]):
                raise ValueError
            self.clues[cur_axis][index] = clue

    def print_solution(self):
        top_row = "+" + self.size[self.x] * "--+"
        print(top_row)
        for y in range(self.size[self.y]):
            row = "|"
            for x in range(self.size[self.x]):
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

    def _set_solution_row(self, input_axis, row_index, solution_row):
        if input_axis == self.x:
            self.solution[row_index] = solution_row
        elif input_axis == self.y:
            for index, value in enumerate(solution_row):
                self.solution[index][row_index] = value
        else:
            raise ValueError
