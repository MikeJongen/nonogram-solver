import sys
import os
test_path = os.path.join(os.path.dirname(__file__), '../')  # nopep8
sys.path.insert(0, os.path.abspath(test_path))  # nopep8

import solver.test_performance as performance
import solver.basic.basic as basic
import unittest


class TestPerformance(unittest.TestCase):
    def test_performance_test_init(self):
        test_file = "puzzles/test/basic_solver1.txt"
        test = performance.Performance_Test(basic.BasicSolver, test_file)
        pair = test.solver.get_clue_solution_pair("x", 0)
        self.assertEqual(pair, ([1, 2], [0, 0, 0, 0, 0]))
        pair = test.solver.get_clue_solution_pair("y", 3)
        self.assertEqual(pair, ([1, 1, 1], [0, 0, 0, 0, 0]))

    def test_performance_test_run(self):
        test_file = "puzzles/test/basic_solver1.txt"
        test = performance.Performance_Test(basic.BasicSolver, test_file)
        test.run()
        pair = test.solver.get_clue_solution_pair("x", 0)
        self.assertEqual(pair, ([1, 2], [1, -1, 1, 1, 0]))
        pair = test.solver.get_clue_solution_pair("y", 3)
        self.assertEqual(pair, ([1, 1, 1], [1, -1, 1, -1, 1]))

    def test_test_runner_timing_test(self):
        test = performance.Test_Runner(basic.BasicSolver)
        test.run_timing_test("puzzles/test/basic_solver1.txt")
        self.assertIn("puzzles/test/basic_solver1.txt", test.timing_results)

    def test_test_runner_correct_test(self):
        test = performance.Test_Runner(basic.BasicSolver)
        test.run_correctness_test("puzzles/test/basic_solver1.txt")
        self.assertIn("puzzles/test/basic_solver1.txt", test.correct_results)


if __name__ == '__main__':
    unittest.main()
