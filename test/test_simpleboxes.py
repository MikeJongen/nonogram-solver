import sys
import os
import unittest
test_path = os.path.join(os.path.dirname(__file__), '../')   # noqa
sys.path.insert(0, os.path.abspath(test_path))   # noqa

import solver.basic.simple_boxes as simple_boxes  # noqa: E402


class TestSimpleBoxes(unittest.TestCase):
    def test_solve_clues_too_small(self):
        empty = [0] * 15
        row = simple_boxes.SimpleBoxesRowSolver(
            [5, 4], empty)
        row.solve_simple_boxes()
        self.assertEqual(
            row.values, [0] * 15)

    def test_solve_clues_just_big_enough(self):
        empty = [0] * 15
        expected = [0] * 15
        expected[7] = 1
        row = simple_boxes.SimpleBoxesRowSolver(
            [2, 5, 2], empty)
        row.solve_simple_boxes()
        self.assertEqual(
            row.values, expected)

    def test_solve_clues_just_big_enough_asymetric(self):
        empty = [0] * 15
        expected = [0] * 15
        expected[6] = 1
        row = simple_boxes.SimpleBoxesRowSolver(
            [1, 5, 3], empty)
        row.solve_simple_boxes()
        self.assertEqual(
            row.values, expected)

    def test_solve_clues_lot_of_numbers(self):
        empty = [0] * 20
        expected = [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0]
        row = simple_boxes.SimpleBoxesRowSolver(
            [1, 2, 1, 5, 3, 2], empty)
        row.solve_simple_boxes()
        self.assertEqual(
            row.values, expected)

    def test_solve_clues_single_just_big_enough(self):
        empty = [0] * 15
        expected = [0] * 15
        expected[7] = 1
        row = simple_boxes.SimpleBoxesRowSolver(
            [8], empty)
        row.solve_simple_boxes()
        self.assertEqual(
            row.values, expected)

    def test_solve_clues_single(self):
        empty = [0] * 15
        expected = [0] * 15
        expected[4:11] = [1] * 7
        row = simple_boxes.SimpleBoxesRowSolver(
            [11], empty)
        row.solve_simple_boxes()
        self.assertEqual(
            row.values, empty)

    def test_solve_defined_row(self):
        empty = [0] * 10
        row = simple_boxes.SimpleBoxesRowSolver(
            [5, 4], empty)
        row.solve_simple_boxes()
        self.assertEqual(row.values, [1, 1, 1, 1, 1, 0, 1, 1, 1, 1])

    def test_solve_empty_row(self):
        empty = [0] * 10
        row = simple_boxes.SimpleBoxesRowSolver(
            [], empty)
        row.solve_simple_boxes()
        self.assertEqual(row.values, [0] * 10)

    def test_solver(self):
        new_nonogram = \
            simple_boxes.SimpleBoxesSolver(
                file="test/puzzles/simple_boxes.json")
        new_nonogram.solve()
        expected_solution = [[0, 1, 1, 1, 0],
                             [0, 1, 0, 0, 1],
                             [0, 0, 1, 1, 0],
                             [0, 0, 0, 1, 0],
                             [0, 0, 0, 0, 0]]
        self.assertEqual(new_nonogram.solution, expected_solution)


if __name__ == '__main__':
    unittest.main()
