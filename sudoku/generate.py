import sys
from sudoku import *
from collections import deque
import copy

class SudokuCreator:
    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.domains = {
            var:set(range(1, 10))
            for var in self.sudoku.variables
        }

    def save(self, assignment, filename):    # Implement with Pillow library
        pass

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
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revision = False
        if x in self.sudoku.neighbors(y):
            for val in self.domains[x]:
                if any(v != val for v in self.domains[y]):
                    self.domains[x].remove(val)
                    revision = True
        return revision


    def ac3(self):
        """
        Update `self.domains` such that each variable is arc consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        arcs_list = []
        for x in self.domains:
            for y in self.sudoku.neighbors(x):
                arcs_list.append((x,y))
        arcs_queue = deque(arcs_list)
        while arcs_queue:
            x, y = arcs_queue.popleft()
            if self.revise(x,y):
                if len(self.domains[x]) == 0:
                    return False
                else:
                    for z in self.sudoku.neighbors(x):
                        if z != y:
                            arcs_queue.append((z,x))
        return True


    def assignement_complete(self, assignement):
        return len(self.domains) == len(assignement)

    def assignement_consistent(self, assignement):
        """
        Return True if `assignment` is consistent; return False otherwise.
        """
        for x in assignement:
            for y in assignement:
                if x != y and self.sudoku.are_neighbors(x, y) and assignement[x] == assignement[y]:
                    return False
        return True

    def select_unassigned_variable(self, assignment):   # Missing implementation with heuristics
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_variables = [var for var in self.domains if var not in assignment]
        return min(unassigned_variables,
                   key=lambda var : (len(self.domains[var]), -len(self.sudoku.neighbors(var))) )

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to integers (values).

        If no assignment is possible, return None.
        """
        if self.assignement_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for val in self.domains[var]:
            assignment_copy = copy.deepcopy(assignment)
            assignment_copy[var] = val
            if self.assignement_consistent(assignment_copy):
                result = self.backtrack(assignment_copy)
                if result is not None:
                    return result
        return None


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
