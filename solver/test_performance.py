import sys
import os
test_path = os.path.join(os.path.dirname(__file__), '../')
sys.path.insert(0, os.path.abspath(test_path))

import timeit
import solver.basic

def run():
    puzzle.solver1()

def run_single_puzzle(puzzle):
    iterations = 10000
    time = timeit.timeit("run()", \
                         setup="from __main__ import run", \
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
