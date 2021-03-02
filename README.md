# nonogram-solver
script to solve nonogram puzzles

# Nonogram
parent class which holds functions to initialize the puzzle and print
the solution.

## Create nonogram.
A nonogram can be created manually or by loading a json file.
### Manual creation
```
# import library
from solver.nonogram import Nonogram
# create puzzle of size 5 by 5
puzzle = Nonogram(5, 5)
# set clues for the (horizontal) rows
puzzle.set_clues_x([1, 2], [1, 1], [1, 3], [1], [1, 2])
# set clues for the (vertical) columns
puzzle.set_clues_y([5], [], [3, 1], [1, 1, 1], [1])

# save to file
puzzle.save("puzzles/new_puzzle.json")
```

### Loading a file
```
# import library
from solver.nonogram import Nonogram
# load puzzle from file
puzzle = Nonogram(file="puzzles/easy/pyramid.json")
```


# Unit Tests
Run with
```
python3 -m unittest discover
```