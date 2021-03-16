import sys
import os
import unittest
test_path = os.path.join(os.path.dirname(__file__), '../')   # noqa
sys.path.insert(0, os.path.abspath(test_path))   # noqa

from solver.error import LengthError, ClueError, SetSolutionError  # noqa: E402
import solver.nonogram as nonogram  # noqa: E402


class TestNonogram(unittest.TestCase):
    def test_init(self):
        new_nonogram = nonogram.Nonogram(5, 5)
        self.assertIsNotNone(new_nonogram)

    def test_init_from_file(self):
        new_nonogram = \
            nonogram.Nonogram(file="test/puzzles/load.json")
        expected_size = {"x": 5, "y": 5}
        expected_solution = [[1,  1,  1,  1,  1],
                             [-1, -1, -1, -1, -1],
                             [1,  1,  1, -1,  1],
                             [1, -1,  1, -1,  1],
                             [-1, -1,  1, -1, -1]]
        expected_clues_x = [[1, 2], [1, 1], [1, 3], [1], [1, 2]]
        expected_clues_y = [[5], [], [3, 1], [1, 1, 1], [1]]
        expected_clues = dict()
        expected_clues["x"] = expected_clues_x
        expected_clues["y"] = expected_clues_y
        self.assertEqual(expected_size, new_nonogram.size)
        self.assertEqual(expected_solution, new_nonogram.solution)
        self.assertEqual(expected_clues, new_nonogram.clues)

    def test_isnotcomplete(self):
        new_nonogram = nonogram.Nonogram(5, 10)
        self.assertFalse(new_nonogram.is_complete())

    def test_percentcomplete(self):
        new_nonogram = nonogram.Nonogram(5, 10)
        example_row = [1, 1, 1, 1, 1]
        example_col = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.assertEqual(new_nonogram.percent_complete(), 0)
        new_nonogram._set_solution_row("x", 0, example_row)
        self.assertEqual(new_nonogram.percent_complete(), 10.0)
        new_nonogram._set_solution_row("x", 1, example_row)
        self.assertEqual(new_nonogram.percent_complete(), 20.0)
        new_nonogram._set_solution_row("y", 0, example_col)
        self.assertEqual(new_nonogram.percent_complete(), 36.0)
        new_nonogram._set_solution_row("y", 1, example_col)
        new_nonogram._set_solution_row("y", 2, example_col)
        new_nonogram._set_solution_row("y", 3, example_col)
        new_nonogram._set_solution_row("y", 4, example_col)
        self.assertEqual(new_nonogram.percent_complete(), 100.0)

    def test_iscorrect(self):
        new_nonogram = \
            nonogram.Nonogram(file="test/puzzles/load.json")
        self.assertTrue(new_nonogram.is_correct())
        new_nonogram.solution[0][0] = -1
        self.assertFalse(new_nonogram.is_correct())

    def test_legitimateinput(self):
        new_nonogram = nonogram.Nonogram(5, 10)
        clues_x = [[5], [4], [3], [2], [1],
                   [1], [3, 1], [1, 1, 1], [1, 2], [1]]
        clues_y = [[1, 1, 3], [3, 1], [5, 4], [2, 1, 1], [2, 2]]
        new_nonogram.set_clues_x(*clues_x)
        new_nonogram.set_clues_y(*clues_y)

    def test_wrongnumberofinputs(self):
        new_nonogram = nonogram.Nonogram(5, 10)
        clues_x = [[5], [4], [3], [2], [1],
                   [1], [3, 1], [1, 1, 1], [1, 2]]
        clues_y = [[1, 1, 3], [3, 1], [5, 4], [2, 1, 1], [2, 2], [5]]
        self.assertRaises(LengthError,
                          new_nonogram.set_clues_x, *clues_x)
        self.assertRaises(LengthError,
                          new_nonogram.set_clues_y, *clues_y)

    def test_wronginputvalue(self):
        new_nonogram = nonogram.Nonogram(5, 10)
        clues_x = [[6], [4], [3], [2], [1],
                   [1], [3, 1], [1, 1, 1], [1, 2], [1]]
        clues_y = [[1, 1, 3, 3], [3, 1], [5, 4], [2, 1, 1], [2, 2]]
        self.assertRaises(ClueError,
                          new_nonogram.set_clues_x, *clues_x)
        self.assertRaises(ClueError,
                          new_nonogram.set_clues_y, *clues_y)

    def test_save(self):
        new_nonogram = nonogram.Nonogram(5, 5)
        clues_x = [[1, 2], [1, 1], [1, 3], [1], [1, 2]]
        clues_y = [[5], [], [3, 1], [1, 1, 1], [1]]
        new_nonogram.set_clues_x(*clues_x)
        new_nonogram.set_clues_y(*clues_y)
        new_nonogram.solution = [[1,  1,  1,  1,  1],
                                 [-1, -1, -1, -1, -1],
                                 [1,  1,  1, -1,  1],
                                 [1, -1,  1, -1,  1],
                                 [-1, -1,  1, -1, -1]]
        new_nonogram.save("test/puzzles/temp.json")
        expected_savefile = "{\"clues\": "
        expected_savefile += "{\"x\": [[1, 2], [1, 1], [1, 3], [1], [1, 2]],"
        expected_savefile += " \"y\": [[5], [], [3, 1], [1, 1, 1], [1]]}, "
        expected_savefile += "\"solution\": "
        expected_savefile += "[[1, 1, 1, 1, 1],"
        expected_savefile += " [-1, -1, -1, -1, -1],"
        expected_savefile += " [1, 1, 1, -1, 1],"
        expected_savefile += " [1, -1, 1, -1, 1],"
        expected_savefile += " [-1, -1, 1, -1, -1]]}"
        f = open("test/puzzles/temp.json", "r")
        saved_text = f.read()
        f.close()
        self.assertEqual(expected_savefile, saved_text)
        os.remove("test/puzzles/temp.json")

    def test_save_only_clues(self):
        new_nonogram = nonogram.Nonogram(5, 5)
        clues_x = [[1, 2], [1, 1], [1, 3], [1], [1, 2]]
        clues_y = [[5], [], [3, 1], [1, 1, 1], [1]]
        new_nonogram.set_clues_x(*clues_x)
        new_nonogram.set_clues_y(*clues_y)
        new_nonogram.solution = [[1,  1,  1,  1,  1],
                                 [-1, -1, -1, -1, -1],
                                 [1,  1,  1, -1,  1],
                                 [1, -1,  1, -1,  1],
                                 [-1, -1,  1, -1, -1]]
        new_nonogram.save("test/puzzles/temp.json", only_clues=True)
        expected_savefile = "{\"clues\": "
        expected_savefile += "{\"x\": [[1, 2], [1, 1], [1, 3], [1], [1, 2]],"
        expected_savefile += " \"y\": [[5], [], [3, 1], [1, 1, 1], [1]]}}"
        f = open("test/puzzles/temp.json", "r")
        saved_text = f.read()
        f.close()
        self.assertEqual(expected_savefile, saved_text)
        os.remove("test/puzzles/temp.json")

    def test_load(self):
        new_nonogram = nonogram.Nonogram(5, 5)
        new_nonogram.load("test/puzzles/load.json")
        expected_size = {"x": 5, "y": 5}
        expected_solution = [[1,  1,  1,  1,  1],
                             [-1, -1, -1, -1, -1],
                             [1,  1,  1, -1,  1],
                             [1, -1,  1, -1,  1],
                             [-1, -1,  1, -1, -1]]
        expected_clues_x = [[1, 2], [1, 1], [1, 3], [1], [1, 2]]
        expected_clues_y = [[5], [], [3, 1], [1, 1, 1], [1]]
        expected_clues = dict()
        expected_clues["x"] = expected_clues_x
        expected_clues["y"] = expected_clues_y
        self.assertEqual(expected_size, new_nonogram.size)
        self.assertEqual(expected_solution, new_nonogram.solution)
        self.assertEqual(expected_clues, new_nonogram.clues)

    def test_load_clues(self):
        new_nonogram = nonogram.Nonogram(5, 5)
        new_nonogram.load("test/puzzles/clues_only.json")
        expected_size = {"x": 5, "y": 5}
        expected_solution = [[0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0]]
        expected_clues_x = [[1, 2], [1, 1], [1, 3], [1], [1, 2]]
        expected_clues_y = [[5], [], [3, 1], [1, 1, 1], [1]]
        expected_clues = dict()
        expected_clues["x"] = expected_clues_x
        expected_clues["y"] = expected_clues_y
        self.assertEqual(expected_size, new_nonogram.size)
        self.assertEqual(expected_solution, new_nonogram.solution)
        self.assertEqual(expected_clues, new_nonogram.clues)

    def test_load_clues_5_10(self):
        new_nonogram = nonogram.Nonogram(5, 5)
        new_nonogram.load("test/puzzles/clues_only_5_10.json")
        expected_size = {"x": 5, "y": 10}
        expected_solution = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        expected_clues_x = [[1, 2], [1, 1], [1, 3], [1],
                            [1, 2], [1, 2], [1, 1], [1, 3], [1], [1, 2]]
        expected_clues_y = [[10], [], [3, 4, 1], [1, 1, 2, 1, 1], [1, 1]]
        expected_clues = dict()
        expected_clues["x"] = expected_clues_x
        expected_clues["y"] = expected_clues_y
        self.assertEqual(expected_size, new_nonogram.size)
        self.assertEqual(expected_solution, new_nonogram.solution)
        self.assertEqual(expected_clues, new_nonogram.clues)

    def test_setsolutionrow(self):
        new_nonogram = \
            nonogram.Nonogram(file="test/puzzles/halfdone.json")
        test_column = [1, -1, 0, -1, 1]
        new_nonogram._set_solution_row("y", 2, test_column)
        new_column = new_nonogram._get_solution_row("y", 2)
        self.assertEqual(new_column, test_column)
        test_row = [-1, 1, 0, -1, 1]
        new_nonogram._set_solution_row("x", 0, test_row, 1)
        new_row = new_nonogram._get_solution_row("x", 0)
        self.assertEqual(new_row, test_row)

    def test_setsolutionvalue(self):
        new_nonogram = \
            nonogram.Nonogram(file="test/puzzles/halfdone.json")
        new_nonogram._set_solution_value(0, 0, 1)
        self.assertEqual(new_nonogram.solution[0][0], 1)
        new_nonogram._set_solution_value(0, 1, 0)
        self.assertEqual(new_nonogram.solution[0][1], 1)
        new_nonogram._set_solution_value(1, 2, 0)
        self.assertEqual(new_nonogram.solution[1][2], -1)
        new_nonogram._set_solution_value(1, 3, -1)
        self.assertEqual(new_nonogram.solution[1][3], -1)
        new_nonogram._set_solution_value(2, 0, 1)
        self.assertEqual(new_nonogram.solution[2][0], 1)
        new_nonogram._set_solution_value(2, 1, 0)
        self.assertEqual(new_nonogram.solution[2][1], 0)
        new_nonogram._set_solution_value(2, 2, -1)
        self.assertEqual(new_nonogram.solution[2][2], -1)

    def test_setsolutionvalueerror(self):
        new_nonogram = \
            nonogram.Nonogram(file="test/puzzles/halfdone.json")
        self.assertRaises(SetSolutionError,
                          new_nonogram._set_solution_value, 0, 2, -1)
        self.assertEqual(new_nonogram.solution[0][2], 1)
        self.assertRaises(SetSolutionError,
                          new_nonogram._set_solution_value, 1, 2, 1)
        self.assertEqual(new_nonogram.solution[1][2], -1)

    def test_setsolutionvalueforced(self):
        new_nonogram = \
            nonogram.Nonogram(file="test/puzzles/halfdone.json")
        new_nonogram._set_solution_value(0, 2, -1, 1)
        self.assertEqual(new_nonogram.solution[0][2], -1)
        new_nonogram._set_solution_value(1, 2, 1, 1)
        self.assertEqual(new_nonogram.solution[1][2], 1)

    def test_getsolutionrow(self):
        new_nonogram = \
            nonogram.Nonogram(file="test/puzzles/load.json")
        row = new_nonogram._get_solution_row("x", 1)
        expected_row = [1, -1, 1, -1, -1]
        self.assertEqual(expected_row, row)
        column = new_nonogram._get_solution_row("y", 3)
        expected_column = [1, -1, 1, -1, 1]
        self.assertEqual(expected_column, column)

    def test_getsolutionrowcopy(self):
        """
        Make sure _get_solution_row returns a copy, and adjusting this does not
        change the original solution.
        """
        new_nonogram = \
            nonogram.Nonogram(file="test/puzzles/trivial.json")
        expected_solution = [[0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0]]
        row1 = new_nonogram._get_solution_row("x", 1)
        row2 = new_nonogram._get_solution_row("y", 3)
        row1[0] = 1
        row1[3] = 1
        row2[1] = 1
        row2[4] = 1
        self.assertEqual(new_nonogram.solution, expected_solution)

    def test_get_clue_solution_pair(self):
        new_nonogram = \
            nonogram.Nonogram(file="test/puzzles/load.json")
        pair = new_nonogram.get_clue_solution_pair("x", 1)
        self.assertEqual(pair, ([1, 1], [1, -1, 1, -1, -1]))
        pair = new_nonogram.get_clue_solution_pair("y", 1)
        self.assertEqual(pair, ([], [-1, -1, -1, -1, -1]))

    def test_reset(self):
        new_nonogram = \
            nonogram.Nonogram(file="test/puzzles/load.json")
        new_nonogram.reset_solution()
        empty_solution = [[0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0]]
        self.assertEqual(new_nonogram.solution, empty_solution)

    def test_change_clues(self):
        puzzle = nonogram.Nonogram(5, 6)
        x_clues = [[1, 2], [1, 1], [1, 3], [1], [1, 2], []]
        y_clues = [[5], [], [3, 1], [1, 1, 1], [1]]
        puzzle.set_clues_x(*x_clues)
        puzzle.set_clues_y(*y_clues)
        for index, clue in enumerate(y_clues):
            self.assertEqual(puzzle.row_solver["y"][index].clues, clue)
        for index, clue in enumerate(x_clues):
            self.assertEqual(puzzle.row_solver["x"][index].clues, clue)

    def test_update_row_solvers(self):
        puzzle = nonogram.Nonogram(file="test/puzzles/full.json")
        puzzle._set_solution_row("x", 0, [1] * 5)
        puzzle._set_solution_row("x", 1, [1] * 5)
        puzzle._set_solution_row("x", 2, [1] * 5)
        puzzle._set_solution_row("x", 3, [1] * 5)
        puzzle._set_solution_row("x", 4, [1] * 5)
        for index in range(5):
            self.assertFalse(puzzle.row_solver["y"][index].is_complete())
        puzzle.update_row_solvers()
        for index in range(5):
            self.assertTrue(puzzle.row_solver["y"][index].is_complete())


if __name__ == '__main__':
    unittest.main()
