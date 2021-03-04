# nonogram-solver
script to solve nonogram puzzles

## Requirements
This project was last tested with python 3.8.5. 
No external libraries are required.

## Tutorial
Note: This project includes several solver classes. For this tutorial, we use 
the compound.balanced solver, as this is the most generic solver. The other solvers
are more specialized or limited, but still use the same methods as shown
in this tutorial. 

### Create nonogram.
A nonogram can be created manually or by loading a json file.
#### Manual creation
```
# Import library
from solver.compound.balanced import BalancedSolver
# Create puzzle of size 5 by 5
puzzle = BalancedSolver(5, 5)
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
from solver.compound.balanced import BalancedSolver
# Load puzzle from file
puzzle = BalancedSolver(file="puzzles/easy/pyramid.json")
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

Note: legend for the solution print:  
XX is a filled cell  
.. is a blank cell  
   is a unknown cell  

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