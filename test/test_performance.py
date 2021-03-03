import sys
import os
test_path = os.path.join(os.path.dirname(__file__), '../')  # nopep8
sys.path.insert(0, os.path.abspath(test_path))  # nopep8

import solver.test_performance as performance
import solver.basic.trivial as trivial
import unittest


class TestPerformance(unittest.TestCase):
    def test_performance_test_init(self):
        test_file = "test/puzzles/nonogram_trivial.json"
        test = performance.Performance_Test(trivial.TrivialSolver, test_file)
        pair = test.solver.get_clue_solution_pair("x", 0)
        self.assertEqual(pair, ([1, 2], [0, 0, 0, 0, 0]))
        pair = test.solver.get_clue_solution_pair("y", 3)
        self.assertEqual(pair, ([1, 1, 1], [0, 0, 0, 0, 0]))

    def test_performance_test_run(self):
        test_file = "test/puzzles/nonogram_trivial.json"
        test = performance.Performance_Test(trivial.TrivialSolver, test_file)
        test.run()
        pair = test.solver.get_clue_solution_pair("x", 0)
        self.assertEqual(pair, ([1, 2], [1, -1, 1, 1, 0]))
        pair = test.solver.get_clue_solution_pair("y", 3)
        self.assertEqual(pair, ([1, 1, 1], [1, -1, 1, -1, 1]))

    def test_test_runner_timing_test(self):
        test = performance.Test_Runner(trivial.TrivialSolver)
        test.run_timing_test("test/puzzles/nonogram_trivial.json")
        self.assertIn("test/puzzles/nonogram_trivial.json",
                      test.timing_results)

    def test_test_runner_correct_test(self):
        test = performance.Test_Runner(trivial.TrivialSolver)
        test.run_correctness_test("test/puzzles/nonogram_trivial.json")
        self.assertIn("test/puzzles/nonogram_trivial.json",
                      test.correct_results)


if __name__ == '__main__':
    unittest.main()
