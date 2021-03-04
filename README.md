# nonogram-solver
script to solve nonogram puzzles

## Requirements
This project was last tested with python 3.8.5. 
No external libraries are required.

## Tutorial
### Create nonogram.
A nonogram can be created manually or by loading a json file.
#### Manual creation
```
# Import library
from solver.nonogram_solver import NonogramSolver
# Create puzzle of size 5 by 5
puzzle = NonogramSolver(5, 5)
# Set clues for the (horizontal) rows
puzzle.set_clues_x([1, 2], [1, 1], [1, 3], [1], [1, 2])
# Set clues for the (vertical) columns
puzzle.set_clues_y([5], [], [3, 1], [1, 1, 1], [1])

# Save to file
puzzle.save("puzzles/new_puzzle.json")
```

#### Loading a file
```
# Import library
from solver.nonogram_solver import NonogramSolver
# Load puzzle from file
puzzle = NonogramSolver(file="puzzles/easy/pyramid.json")
```

### Solving a puzzle
After creating a nonogram, call its solve function:
```
puzzle.solve()
```

### Evaluating the results
```
# Check is the nonogram has been completed
puzzle.is_complete()
# Check how much of the nonogram is completed
puzzle.percent_complete()
# Check if the nonogram is correct (only works for completed nonograms)
puzzle.is_correct()

# Print the clues of the nonogram
puzzle.print_clues()
# Print the solution of the nonogram
puzzle.print_solution()
```

### Other functions
```
# Save the nonogram to a file
puzzle.save("puzzles/new_puzzle.json")

# Reset the solution
puzzle.reset_solution()
```

## Unit Tests
Run with
```
python3 -m unittest discover
```