import sys
import os
test_path = os.path.join(os.path.dirname(__file__), '../solver')
sys.path.insert(0, os.path.abspath(test_path))

import unittest
import basic

class TestBasic(unittest.TestCase):
    def test_defined_row(self):
        new_nonogram = basic.BasicSolver(5, 10)
        clues_x = [[1, 3], [1, 1, 1], [1, 3], [1, 1, 1], [1, 2],\
                   [1, 1, 1] ,[1, 3], [1, 1], [1, 2], [1, 3]]
        clues_y = [[10], [], [4, 2, 2], [1, 1, 1, 1, 2], [8, 1]]
        new_nonogram.set_clues_x(*clues_x)
        new_nonogram.set_clues_y(*clues_y)
        new_nonogram.solve_defined_row('y', 0)
        new_nonogram.solve_defined_row('y', 1)
        new_nonogram.solve_defined_row('y', 2)
        new_nonogram.solve_defined_row('y', 3)
        new_nonogram.solve_defined_row('y', 4)
        expected_solution = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], \
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
                             [1, 1, 1, 1, 0, 1, 1, 0, 1, 1], \
                             [1, 0, 1, 0, 1, 0, 1, 0, 1, 1], \
                             [1, 1, 1, 1, 1, 1, 1, 1, 0, 1]]
        self.assertEqual(new_nonogram.solution, expected_solution)

    def test_number_of_solutions(self):
        new_nonogram = basic.BasicSolver(5, 10)
        clues_x = [[1, 3], [1, 1], [1, 2], [1, 1], [1, 1],\
                   [1, 1] ,[1, 2], [1], [1, 2], [1, 1]]
        clues_y = [[10], [], [4, 2, 1], [1, 1, 1, 1, 1], [1, 1]]
        new_nonogram.set_clues_x(*clues_x)
        new_nonogram.set_clues_y(*clues_y)
        solutions = []
        for i in range(5):
            number = new_nonogram.get_number_of_solutions_total('y', i)
            solutions.append(number)
        expected_solutions = [1, 1, 4, 6, 36]
        self.assertEqual(expected_solutions, solutions)

if __name__ == '__main__':
    unittest.main()
