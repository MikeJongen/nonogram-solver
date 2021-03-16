import sys
import os
import unittest
test_path = os.path.join(os.path.dirname(__file__), '../')   # noqa
sys.path.insert(0, os.path.abspath(test_path))   # noqa

import solver.basic.brute_force_2 as brute_force  # noqa: E402


class TestBasic(unittest.TestCase):
    def test_number_of_solutions(self):
        row = brute_force.BruteForceRowSolver2([2, 1], [0] * 5)
        no_solutions = row._get_number_of_solutions()
        self.assertEqual(no_solutions, 3)

    def test_number_of_solutions_large(self):
        row = brute_force.BruteForceRowSolver2([1, 1, 1], [0] * 10)
        no_solutions = row._get_number_of_solutions()
        self.assertEqual(no_solutions, 56)

    def test_number_of_solutions_large_2(self):
        row = brute_force.BruteForceRowSolver2([2, 1, 1], [0] * 10)
        no_solutions = row._get_number_of_solutions()
        self.assertEqual(no_solutions, 35)

    def test_number_of_solutions_one_clue(self):
        row = brute_force.BruteForceRowSolver2([2], [0] * 5)
        no_solutions = row._get_number_of_solutions()
        self.assertEqual(no_solutions, 4)

    def test_number_of_solutions_empty(self):
        row = brute_force.BruteForceRowSolver2([], [0] * 5)
        no_solutions = row._get_number_of_solutions()
        self.assertEqual(no_solutions, 1)

    def test_get_all_solutions(self):
        row = brute_force.BruteForceRowSolver2([2, 1], [0] * 5)
        expected_solutions = [
            [1, 1, -1, 1, -1],
            [1, 1, -1, -1, 1],
            [-1, 1, 1, -1, 1],
        ]
        solutions = row._get_all_solutions()
        self.assertEqual(solutions, expected_solutions)

    def test_get_all_solutions_one_clue(self):
        row = brute_force.BruteForceRowSolver2([3], [0] * 5)
        expected_solutions = [
            [1, 1, 1, -1, -1],
            [-1, 1, 1, 1, -1],
            [-1, -1, 1, 1, 1],
        ]
        solutions = row._get_all_solutions()
        self.assertEqual(solutions, expected_solutions)

    def test_get_all_solutions_two_clues(self):
        row = brute_force.BruteForceRowSolver2([3, 4], [0] * 10)
        solution = row._get_all_solutions()
        expected_solution = [[1,  1, 1, -1,  1,  1, 1, 1, -1, -1],
                             [1,  1, 1, -1, -1,  1, 1, 1,  1, -1],
                             [1,  1, 1, -1, -1, -1, 1, 1,  1,  1],
                             [-1,  1, 1,  1, -1,  1, 1, 1,  1, -1],
                             [-1,  1, 1,  1, -1, -1, 1, 1,  1,  1],
                             [-1, -1, 1,  1,  1, -1, 1, 1,  1,  1]]
        self.assertEqual(expected_solution, solution)

    def test_get_all_solutions_three_clues(self):
        row = brute_force.BruteForceRowSolver2([2, 2, 3], [0] * 10)
        solution = row._get_all_solutions()
        expected_solution = [[1, 1, -1,  1, 1, -1,  1, 1, 1, -1],
                             [1, 1, -1,  1, 1, -1, -1, 1, 1,  1],
                             [1, 1, -1, -1, 1,  1, -1, 1, 1,  1],
                             [-1, 1,  1, -1, 1,  1, -1, 1, 1,  1]]
        self.assertEqual(expected_solution, solution)

    def test_get_all_solutions_empty(self):
        row = brute_force.BruteForceRowSolver2([], [0] * 5)
        expected_solutions = [
            [-1, -1, -1, -1, -1],
        ]
        solutions = row._get_all_solutions()
        self.assertEqual(solutions, expected_solutions)

    def test_check_solutions(self):
        row = brute_force.BruteForceRowSolver2([2, 1], [1, 0, 0, 0, 0])
        valid = row._check_solution([1, 1, 0, 1, 0])
        self.assertTrue(valid)
        valid = row._check_solution([0, 1, 1, 0, 1])
        self.assertFalse(valid)

    def test_matching_solutions(self):
        row = brute_force.BruteForceRowSolver2([2, 1], [0] * 5)
        solution1 = [-1, 1, 1, -1, 1]
        solution2 = [1, 1, -1, -1, 1]
        expected_solution = [0, 1, 0, -1, 1]
        solution = row._get_matching_solution(solution1, solution2)
        self.assertEqual(expected_solution, solution)

    def test_row_brute_force_empty_values(self):
        row = brute_force.BruteForceRowSolver2([2, 1], [0] * 5)
        changed = row.solve_brute_force_save_intermediate()
        self.assertTrue(changed)
        self.assertEqual(row.values, [0, 1, 0, 0, 0])

    def test_row_brute_force(self):
        row = brute_force.BruteForceRowSolver2([2, 1], [1, 0, 0, 0, 0])
        changed = row.solve_brute_force_save_intermediate()
        self.assertTrue(changed)
        self.assertEqual(row.values, [1, 1, -1, 0, 0])

    def test_brute_force(self):
        puzzle = brute_force.BruteForceSolver2(file="test/puzzles/stairs.json")
        puzzle.solve()
        puzzle.update_row_solvers()
        puzzle.solve()
        puzzle.update_row_solvers()
        puzzle.solve()
        self.assertTrue(puzzle.is_complete())
        self.assertTrue(puzzle.is_correct())

    def test_reset(self):
        puzzle = brute_force.BruteForceSolver2(file="test/puzzles/stairs.json")
        puzzle.solve()
        puzzle.update_row_solvers()
        puzzle.solve()
        puzzle.update_row_solvers()
        puzzle.solve()
        for axis in puzzle.row_solver:
            for row_solver in puzzle.row_solver[axis]:
                self.assertTrue(hasattr(row_solver, 'number_of_solutions'))
                self.assertTrue(hasattr(row_solver, 'all_solutions'))
        puzzle.reset_solution()
        for axis in puzzle.row_solver:
            for row_solver in puzzle.row_solver[axis]:
                self.assertFalse(hasattr(row_solver, 'number_of_solutions'))
                self.assertFalse(hasattr(row_solver, 'all_solutions'))


if __name__ == '__main__':
    unittest.main()
