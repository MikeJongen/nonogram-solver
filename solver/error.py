class NonogramError(Exception):
    """Base class for exceptions in this module."""
    pass

class LengthError(NonogramError):
    """Exception raised for unexpected list lengths."""
    pass

class AxisError(NonogramError):
    """Exception raised for unexpected axis."""
    pass

class ClueError(NonogramError):
    """Exception raised for invalid clue."""
    pass

class SolveError(NonogramError):
    """Exception raised for when solve action cannot be executed."""
    pass

class SetSolutionError(NonogramError):
    """Exception raised for an invalid change of the solution."""
    pass
