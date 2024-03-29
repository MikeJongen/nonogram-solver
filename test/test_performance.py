import sys
import os
import unittest

import nonogram_solver.performance as performance
import nonogram_solver.basic.trivial as trivial


class TestPerformance(unittest.TestCase):
    def test_performance_test_init(self):
        test_file = "test/puzzles/trivial.json"
        test = performance.PerformanceTest(trivial.TrivialSolver, test_file)
        pair = test.solver.get_clue_solution_pair("x", 0)
        self.assertEqual(pair, ([1, 2], [0, 0, 0, 0, 0]))
        pair = test.solver.get_clue_solution_pair("y", 3)
        self.assertEqual(pair, ([1, 1, 1], [0, 0, 0, 0, 0]))

    def test_performance_test_run(self):
        test_file = "test/puzzles/trivial.json"
        test = performance.PerformanceTest(trivial.TrivialSolver, test_file)
        test.run()
        pair = test.solver.get_clue_solution_pair("x", 0)
        self.assertEqual(pair, ([1, 2], [1, -1, 1, 1, 0]))
        pair = test.solver.get_clue_solution_pair("y", 3)
        self.assertEqual(pair, ([1, 1, 1], [1, -1, 1, -1, 1]))

    def test_test_runner_timing_test(self):
        test = performance.TestRunner(trivial.TrivialSolver)
        test.run_timing_test("test/puzzles/trivial.json")
        self.assertIn("test/puzzles/trivial.json",
                      test.timing_results)

    def test_test_runner_correct_test(self):
        test = performance.TestRunner(trivial.TrivialSolver)
        test.run_correctness_test("test/puzzles/trivial.json")
        self.assertIn("test/puzzles/trivial.json",
                      test.correct_results)


if __name__ == '__main__':
    unittest.main()
