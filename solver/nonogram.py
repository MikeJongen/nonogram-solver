class Nonogram:
    """Main nonogram class

    Used to hold the data of the nonogram.
    also has some basic creation and helper functions
    """
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y

        self.solution = [[-1 for y in range(self.size_y)] \
                            for x in range(self.size_x) ]
        self.clue_x = [[] for x in range(self.size_x)]
        self.clue_y = [[] for y in range(self.size_y)]

    def print(self):
        top_row = "+" + self.size_x * "--+"
        print(top_row)
        for y in range(self.size_y):
            row = "|"
            for x in range(self.size_x):
                row += "  |"
            print(row)
            print(top_row)
