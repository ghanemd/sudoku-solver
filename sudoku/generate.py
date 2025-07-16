import sys
from sudoku import *

class SudokuCreator:
    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.domains = {
            var:set(range(1, 10))
            for var in self.sudoku.variables
        }


    def solve(self):
        """
        Enforce node consistency, arc consistency then solve the CSP using the backtracking algorithm.
        """
        self.enforce_node_consistency()
        self.ac3()
        self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the values defined by the structure of the sudoku.)
        """
        for var in self.domains:
            if self.sudoku.structure[var.i][var.j] != None:
                self.domains[var] = {self.sudoku.structure[var.i][var.j]}

    def revise(self, x, y):
        pass

    def ac3(self):
        pass

    def assignement_complete(self, assignement):
        pass

    def assignement_consistent(self, assignement):
        pass

    def select_unassigned_variable(self, assignment):
        pass

    def backtrack(self, assignment):
        pass


def main():
    
    # Check usage
    if len(sys.argv) != 2:
        sys.exit("Invalid usage")

    # Parse command-line arguments
    file_name = sys.argv[1]

    # Generate sudoku
    sudoku = Sudoku(file_name)
    creator = SudokuCreator(sudoku)
    assignement = creator.solve()

    # Print result
    if assignement is None:
        print("No solution.")
    else:
        pass


if __name__ == "__main__":
    main()
