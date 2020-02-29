class Nonogram:
    """Main nonogram class

    Used to hold the data of the nonogram.
    also has some basic creation and helper functions
    """
    printable_values = {-1: "  ",
                         0: "..",
                         1: "XX"}

    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y

        self.solution = [[-1 for y in range(self.size_y)] \
                            for x in range(self.size_x) ]
        self.clues_x = [[] for x in range(self.size_x)]
        self.clues_y = [[] for y in range(self.size_y)]

    def set_clues_x(self, *clues):
        if len(clues) != self.size_x:
            raise ValueError
        for index, clue in enumerate(clues):
            min_length_clue = sum(clue) + len(clue) - 1
            if(min_length_clue > self.size_x):
                raise ValueError
            self.clues_x[index] = clue

    def set_clues_y(self, *clues):
        if len(clues) != self.size_y:
            raise ValueError
        for index, clue in enumerate(clues):
            min_length_clue = sum(clue) + len(clue) - 1
            if(min_length_clue > self.size_y):
                raise ValueError
            self.clues_y[index] = clue

    def print_solution(self):
        top_row = "+" + self.size_x * "--+"
        print(top_row)
        for y in range(self.size_y):
            row = "|"
            for x in range(self.size_x):
                row += f"{self.printable_values[self.solution[x][y]]}|"
            print(row)
            print(top_row)

    def print_clues(self):
        print("Horizontal clues:")
        for clue in self.clues_x:
            print(clue)
        print("Vertical clues:")
        for clue in self.clues_y:
            print(clue)
