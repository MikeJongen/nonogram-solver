import sys
import os
test_path = os.path.join(os.path.dirname(__file__), '../')  # nopep8
sys.path.insert(0, os.path.abspath(test_path))  # nopep8

from solver.error import *
import solver.basic as basic
import unittest


class TestBasic(unittest.TestCase):
    def test_solver1(self):
        new_nonogram = \
            basic.BasicSolver(file="puzzles/test/basic_solver1.txt")
        new_nonogram.solver1()
        expected_solution = [[1,  1,  1,  1,  1],
                             [-1, -1, -1, -1, -1],
                             [1,  1,  1, -1,  1],
                             [1, -1,  1, -1,  1],
                             [0,  1,  0,  0,  1]]
        self.assertEqual(new_nonogram.solution, expected_solution)

    def test_fillcommonelementsrow(self):
        new_nonogram = basic.BasicSolver(10, 5)
        clues_y = [[4], [2, 2], [5], [5], [2, 1],
                   [5], [1, 1], [1, 1], [2, 1], [2, 1]]
        clues_x = [[8], [6, 2], [1, 2, 2, 1], [6], [4, 1, 3]]
        new_nonogram.set_clues_x(*clues_x)
        new_nonogram.set_clues_y(*clues_y)
        new_nonogram.fill_common_elements_row('x', 0)
        new_nonogram.fill_common_elements_row('x', 1)
        new_nonogram.fill_common_elements_row('x', 2)
        new_nonogram.fill_common_elements_row('x', 3)
        new_nonogram.fill_common_elements_row('x', 4)
        expected_solution = [[0,  0,  0,  0,  1],
                             [0,  1,  0,  0,  1],
                             [1,  1,  0,  0,  1],
                             [1,  1,  1,  0,  1],
                             [1,  1,  0,  1, -1],
                             [1,  1,  0,  1,  1],
                             [1,  0,  1,  0, -1],
                             [1,  0,  0,  0,  1],
                             [0,  1,  0,  0,  1],
                             [0,  0,  0,  0,  1]]
        self.assertEqual(new_nonogram.solution, expected_solution)

    def test_number_of_solutions(self):
        new_nonogram = basic.BasicSolver(5, 10)
        clues_x = [[1, 3], [1, 1], [1, 2], [1, 1], [1, 1],
                   [1, 1], [1, 2], [1], [1, 2], [1, 1]]
        clues_y = [[10], [], [4, 2, 1], [1, 1, 1, 1, 1], [1, 1]]
        new_nonogram.set_clues_x(*clues_x)
        new_nonogram.set_clues_y(*clues_y)
        solutions = []
        for i in range(5):
            number = new_nonogram.get_number_of_solutions_total('y', i)
            solutions.append(number)
        expected_solutions = [1, 1, 4, 6, 36]
        self.assertEqual(expected_solutions, solutions)

    def test_matching_solution_input_failed(self):
        new_nonogram = basic.BasicSolver(5, 5)
        row1 = [1, 2, 3]
        row2 = [1, 2, 3, 4]
        self.assertRaises(LengthError,
                          new_nonogram._get_matching_solution,
                          row1, row2)
        self.assertRaises(LengthError,
                          new_nonogram._get_matching_solution,
                          row2, row1)

    def test_matching_solution_full_rows(self):
        new_nonogram = basic.BasicSolver(5, 5)
        row1 = [1, -1, 1, -1, 1]
        row2 = [1, 1, -1, -1, 1]
        expected_solution = [1, 0, 0, -1, 1]
        solution = new_nonogram._get_matching_solution(row1, row2)
        self.assertEqual(expected_solution, solution)

    def test_list_of_solutions_empty(self):
        new_nonogram = basic.BasicSolver(5, 5)
        solution = new_nonogram._list_of_solutions([], [], [], 5)
        expected_solution = [[-1, -1, -1, -1, -1]]
        self.assertEqual(expected_solution, solution)

    def test_list_of_solutions_full(self):
        new_nonogram = basic.BasicSolver(5, 5)
        solution = new_nonogram._list_of_solutions([], [], [5], 5)
        expected_solution = [[1, 1, 1, 1, 1]]
        self.assertEqual(expected_solution, solution)

    def test_list_of_solutions_one(self):
        new_nonogram = basic.BasicSolver(5, 5)
        solution = new_nonogram._list_of_solutions([], [], [3], 5)
        expected_solution = [[1,  1, 1, -1, -1],
                             [-1,  1, 1,  1, -1],
                             [-1, -1, 1,  1,  1]]
        self.assertEqual(expected_solution, solution)

    def test_list_of_solutions_two1(self):
        new_nonogram = basic.BasicSolver(5, 5)
        solution = new_nonogram._list_of_solutions([], [], [2, 1], 5)
        expected_solution = [[1, 1, -1,  1, -1],
                             [1, 1, -1, -1,  1],
                             [-1, 1,  1, -1,  1]]
        self.assertEqual(expected_solution, solution)

    def test_list_of_solutions_two2(self):
        new_nonogram = basic.BasicSolver(10, 5)
        solution = new_nonogram._list_of_solutions([], [], [3, 4], 10)
        expected_solution = [[1,  1, 1, -1,  1,  1, 1, 1, -1, -1],
                             [1,  1, 1, -1, -1,  1, 1, 1,  1, -1],
                             [1,  1, 1, -1, -1, -1, 1, 1,  1,  1],
                             [-1,  1, 1,  1, -1,  1, 1, 1,  1, -1],
                             [-1,  1, 1,  1, -1, -1, 1, 1,  1,  1],
                             [-1, -1, 1,  1,  1, -1, 1, 1,  1,  1]]
        self.assertEqual(expected_solution, solution)

    def test_list_of_solutions_three(self):
        new_nonogram = basic.BasicSolver(10, 5)
        solution = new_nonogram._list_of_solutions([], [],
                                                   [2, 2, 3], 10)
        expected_solution = [[1, 1, -1,  1, 1, -1,  1, 1, 1, -1],
                             [1, 1, -1,  1, 1, -1, -1, 1, 1,  1],
                             [1, 1, -1, -1, 1,  1, -1, 1, 1,  1],
                             [-1, 1,  1, -1, 1,  1, -1, 1, 1,  1]]
        self.assertEqual(expected_solution, solution)

    def test_all_solutions(self):
        new_nonogram = basic.BasicSolver(5, 10)
        clues_x = [[1, 3], [1, 1], [1, 2], [1, 1], [1, 1],
                   [1, 1], [1, 2], [1], [1, 2], [1, 1]]
        clues_y = [[10], [], [4, 2, 1], [1, 1, 1, 1, 1], [1, 1]]
        new_nonogram.set_clues_x(*clues_x)
        new_nonogram.set_clues_y(*clues_y)
        solutions = new_nonogram.get_all_solutions('y', 2)
        expected_solutions = [[1, 1, 1, 1, -1,  1, 1, -1,  1, -1],
                              [1, 1, 1, 1, -1,  1, 1, -1, -1,  1],
                              [1, 1, 1, 1, -1, -1, 1,  1, -1,  1],
                              [-1, 1, 1, 1,  1, -1, 1,  1, -1,  1]]
        self.assertEqual(expected_solutions, solutions)


if __name__ == '__main__':
    unittest.main()