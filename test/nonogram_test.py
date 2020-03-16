import sys
import os
test_path = os.path.join(os.path.dirname(__file__), '../')
sys.path.insert(0, os.path.abspath(test_path))

import unittest
import solver.nonogram as nonogram
from solver.error import *

class TestNonogram(unittest.TestCase):
    def test_init(self):
        new_nonogram = nonogram.Nonogram(5, 5)
        self.assertIsNotNone(new_nonogram)

    def test_init_from_file(self):
        new_nonogram = \
                nonogram.Nonogram(file="puzzles/test/nonogram_load.txt")
        expected_size = [5, 5]
        expected_solution = [[ 1,  1,  1,  1,  1], \
                             [-1, -1, -1, -1, -1], \
                             [ 1,  1,  1, -1,  1], \
                             [ 1, -1,  1, -1,  1], \
                             [-1, -1,  1, -1, -1]]
        expected_clues_x = [[1, 2], [1, 1], [1, 3], [1], [1, 2]]
        expected_clues_y = [[5], [], [3, 1], [1, 1, 1], [1]]
        expected_clues = [expected_clues_x, expected_clues_y]
        self.assertEqual(expected_size, new_nonogram.size)
        self.assertEqual(expected_solution, new_nonogram.solution)
        self.assertEqual(expected_clues, new_nonogram.clues)

    def test_size(self):
        new_nonogram = nonogram.Nonogram(5, 10)
        self.assertEqual(new_nonogram.get_size_x(),  5)
        self.assertEqual(new_nonogram.get_size_y(),  10)

    def test_isnotcomplete(self):
        new_nonogram = nonogram.Nonogram(5, 10)
        self.assertFalse(new_nonogram.is_complete())

    def test_percentcomplete(self):
        new_nonogram = nonogram.Nonogram(5, 10)
        example_row = [1, 1, 1, 1, 1]
        example_col = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.assertEqual(new_nonogram.percent_complete(), 0)
        new_nonogram._set_solution_row(new_nonogram.x, 0, example_row)
        self.assertEqual(new_nonogram.percent_complete(), 10.0)
        new_nonogram._set_solution_row(new_nonogram.x, 1, example_row)
        self.assertEqual(new_nonogram.percent_complete(), 20.0)
        new_nonogram._set_solution_row(new_nonogram.y, 0, example_col)
        self.assertEqual(new_nonogram.percent_complete(), 36.0)
        new_nonogram._set_solution_row(new_nonogram.y, 1, example_col)
        new_nonogram._set_solution_row(new_nonogram.y, 2, example_col)
        new_nonogram._set_solution_row(new_nonogram.y, 3, example_col)
        new_nonogram._set_solution_row(new_nonogram.y, 4, example_col)
        self.assertEqual(new_nonogram.percent_complete(), 100.0)

    def test_iscorrect(self):
        new_nonogram = \
                nonogram.Nonogram(file="puzzles/test/nonogram_load.txt")
        self.assertTrue(new_nonogram.is_correct())
        new_nonogram.solution[0][0] = -1
        self.assertFalse(new_nonogram.is_correct())

    def test_legitimateinput(self):
        new_nonogram = nonogram.Nonogram(5, 10)
        clues_x = [[5], [4], [3], [2], [1],\
                   [1] ,[3, 1], [1, 1, 1], [1, 2], [1]]
        clues_y = [[1, 1, 3], [3, 1], [5, 4], [2, 1, 1], [2, 2]]
        new_nonogram.set_clues_x(*clues_x)
        new_nonogram.set_clues_y(*clues_y)

    def test_wrongnumberofinputs(self):
        new_nonogram = nonogram.Nonogram(5, 10)
        clues_x = [[5], [4], [3], [2], [1],\
                   [1] ,[3, 1], [1, 1, 1], [1, 2]]
        clues_y = [[1, 1, 3], [3, 1], [5, 4], [2, 1, 1], [2, 2], [5]]
        self.assertRaises(LengthError, \
                          new_nonogram.set_clues_x, *clues_x)
        self.assertRaises(LengthError, \
                          new_nonogram.set_clues_y, *clues_y)

    def test_wronginputvalue(self):
        new_nonogram = nonogram.Nonogram(5, 10)
        clues_x = [[6], [4], [3], [2], [1],\
                   [1] ,[3, 1], [1, 1, 1], [1, 2], [1]]
        clues_y = [[1, 1, 3, 3], [3, 1], [5, 4], [2, 1, 1], [2, 2]]
        self.assertRaises(ClueError, \
                          new_nonogram.set_clues_x, *clues_x)
        self.assertRaises(ClueError, \
                          new_nonogram.set_clues_y, *clues_y)

    def test_save(self):
        new_nonogram = nonogram.Nonogram(5, 5)
        clues_x = [[1, 2], [1, 1], [1, 3], [1], [1, 2]]
        clues_y = [[5], [], [3, 1], [1, 1, 1], [1]]
        new_nonogram.set_clues_x(*clues_x)
        new_nonogram.set_clues_y(*clues_y)
        new_nonogram.solution = [[ 1,  1,  1,  1,  1], \
                                 [-1, -1, -1, -1, -1], \
                                 [ 1,  1,  1, -1,  1], \
                                 [ 1, -1,  1, -1,  1], \
                                 [-1, -1,  1, -1, -1]]
        new_nonogram.save("puzzles/test/temp.txt")
        expected_savefile = "[[5, 5], "
        expected_savefile += "[[1, 1, 1, 1, 1],"
        expected_savefile += " [-1, -1, -1, -1, -1],"
        expected_savefile += " [1, 1, 1, -1, 1],"
        expected_savefile += " [1, -1, 1, -1, 1],"
        expected_savefile += " [-1, -1, 1, -1, -1]], "
        expected_savefile += "[[[1, 2], [1, 1], [1, 3], [1], [1, 2]],"
        expected_savefile += " [[5], [], [3, 1], [1, 1, 1], [1]]]]"
        f = open("puzzles/test/temp.txt", "r")
        saved_text = f.read()
        f.close()
        self.assertEqual(expected_savefile, saved_text)
        os.remove("puzzles/test/temp.txt")

    def test_load(self):
        new_nonogram = nonogram.Nonogram(5, 5)
        new_nonogram.load("puzzles/test/nonogram_load.txt")
        expected_size = [5, 5]
        expected_solution = [[ 1,  1,  1,  1,  1], \
                             [-1, -1, -1, -1, -1], \
                             [ 1,  1,  1, -1,  1], \
                             [ 1, -1,  1, -1,  1], \
                             [-1, -1,  1, -1, -1]]
        expected_clues_x = [[1, 2], [1, 1], [1, 3], [1], [1, 2]]
        expected_clues_y = [[5], [], [3, 1], [1, 1, 1], [1]]
        expected_clues = [expected_clues_x, expected_clues_y]
        self.assertEqual(expected_size, new_nonogram.size)
        self.assertEqual(expected_solution, new_nonogram.solution)
        self.assertEqual(expected_clues, new_nonogram.clues)

    def test_getsolutionrow(self):
        new_nonogram = \
                nonogram.Nonogram(file="puzzles/test/nonogram_load.txt")
        row = new_nonogram._get_solution_row(new_nonogram.x, 1)
        expected_row = [1, -1, 1, -1, -1]
        self.assertEqual(expected_row, row)
        column = new_nonogram._get_solution_row(new_nonogram.y, 3)
        expected_column = [1, -1, 1, -1, 1]
        self.assertEqual(expected_column, column)

    def test_getcluesfromrow(self):
        new_nonogram = \
                nonogram.Nonogram(file="puzzles/test/nonogram_load.txt")
        row_clues = new_nonogram._get_clues_from_row(new_nonogram.x, 2)
        expected_row_clues = [1, 3]
        self.assertEqual(expected_row_clues, row_clues)
        col_clues = new_nonogram._get_clues_from_row(new_nonogram.y, 3)
        expected_col_clues = [1, 1, 1]
        self.assertEqual(expected_col_clues, col_clues)

if __name__ == '__main__':
    unittest.main()
