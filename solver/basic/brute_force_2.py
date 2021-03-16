from solver.nonogram import Nonogram, Row
from solver.basic.brute_force import BruteForceRowSolver


class BruteForceSolver2(Nonogram):
    """Brute force solver class

    Performance heavy algorithm, use as last option.
    Improved version of brute force. Uses more memory though.
    """

    def init_row_solvers(self):
        Nonogram.init_row_solvers(self, BruteForceRowSolver2)

    def solve(self):
        """
        Returns True if anything was changed to the solution.
        """
        return self.solve_single_iteration(BruteForceRowSolver2.solve_brute_force_save_intermediate)


class BruteForceRowSolver2(BruteForceRowSolver, Row):
    def reset(self):
        if hasattr(self, 'number_of_solutions'):
            del(self.number_of_solutions)
        if hasattr(self, 'all_solutions'):
            del(self.all_solutions)
        super().reset()

    def solve_brute_force_save_intermediate(self, maximum_solutions=100000):
        """
        RowSolver for BruteForceSaveIntermediateSolver class

        Tests every possible solution.

        maximum_solutions : int
            only solve if total number of solutions is lower than this.
        returnvalue : Bool
            A bool to indicate if the row has been changed. (True if changed)
        """
        if self.solved:
            return False

        if not hasattr(self, 'number_of_solutions'):
            self.number_of_solutions = self._get_number_of_solutions()
        if self.number_of_solutions > maximum_solutions:
            return False

        if not hasattr(self, 'all_solutions'):
            self.all_solutions = self._get_all_solutions()

        new_solution = None
        # only keep solutions that fit with the current solution
        self.all_solutions = [
            solution for solution in self.all_solutions if self._check_solution(solution)]
        # combine solutions
        for solution in self.all_solutions:
            if new_solution is None:
                new_solution = solution
                continue
            new_solution = self._get_matching_solution(
                new_solution, solution)

        if self.values == new_solution:
            return False
        if new_solution is not None:
            self.values = new_solution

        return True
