import sys
import os
test_path = os.path.join(os.path.dirname(__file__), '../')  # nopep8
sys.path.insert(0, os.path.abspath(test_path))  # nopep8

import solver.basic
import timeit


class Performance_Test:
    def __init__(self, solver_class, puzzle_file):
        self.solver = solver_class(file=puzzle_file)

    def run(self):
        self.solver.reset_solution()
        self.solver.solver1()

    def get_results(self):
        return {"done": self.solver.is_complete(),
                "done_pct": self.solver.percent_complete(),
                "correct": self.solver.is_correct()}


class Test_Runner:
    def __init__(self, solver_class):
        self.solver = solver_class
        self.timing_results = dict()
        self.correct_results = dict()

    def run_timing_test(self, puzzle):
        setup = ("from solver.test_performance import Performance_Test\n"
                 "import solver\n"
                 "test = Performance_Test("
                 + self.solver.__module__ + "." + self.solver.__name__ +
                 ", "
                 "\"" + puzzle + "\""
                 ")")
        iterations = 10000
        time = timeit.timeit("test.run()",
                             setup=setup,
                             number=iterations)
        self.timing_results[puzzle] = time / iterations * 1000

    def print_timing(self, puzzle):
        print("Time = {:8.5f} ms".format(self.timing_results[puzzle]))

    def run_correctness_test(self, puzzle):
        test = Performance_Test(self.solver, puzzle)
        test.run()
        self.correct_results[puzzle] = test.get_results()

    def print_correctness(self, puzzle):
        complete = self.correct_results[puzzle]["done"]
        print("Solved: {}".format(complete))
        if complete:
            print("Correct: {}".format(
                self.correct_results[puzzle]["correct"]))
        else:
            print("Percentage: {:5.2f}%".format(
                self.correct_results[puzzle]["done_pct"]))


def run():
    puzzle.reset_solution()
    puzzle.solver1()


def run_single_puzzle(puzzle):
    iterations = 10000
    time = timeit.timeit("run()",
                         setup="from __main__ import run",
                         number=iterations)
    complete = puzzle.is_complete()
    print("Solved: {}".format(bool(complete)))
    if complete == 0:
        print("Percentage: {:5.2f}%".format(puzzle.percent_complete()))
    else:
        correct = puzzle.is_correct()
        print("Correct: {}".format(correct))
    print("Time = {:8.5f} ms".format(time / iterations * 1000))


if __name__ == '__main__':
    # make puzzle global so timeit can access it
    global puzzle

    for filename in os.listdir("puzzles/easy"):
        puzzle_file = "puzzles/easy/" + filename
        puzzle = solver.basic.BasicSolver(file=puzzle_file)
        print("\nPuzzle: " + filename.strip(".txt"))
        run_single_puzzle(puzzle)
