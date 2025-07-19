import sys
from sudoku import *
from collections import deque
import copy
from PIL import Image, ImageDraw, ImageFont

class SudokuCreator:
    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.domains = {
            var:set(range(1, 10))
            for var in self.sudoku.variables
        }

    def save(self, assignment, filename):   
        """
        Save the sudoku assignment to an image file.
        """
        cell_size = 50
        cell_border = 2
        interior_size = cell_size - 2 * cell_border

        img = Image.new(
            "RGBA",
            (self.sudoku.width * cell_size,
             self.sudoku.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 35)
        draw = ImageDraw.Draw(img)

        for i in range(self.sudoku.height):
            for j in range(self.sudoku.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]

                if self.sudoku.structure[i][j] != None :
                    draw.rectangle(rect, fill="green")
                else:
                    draw.rectangle(rect, fill="white")

                txt = str(self.get_digit_from_assignement(assignment, i, j))
                _, _, w, h = draw.textbbox((0, 0), txt, font=font)
                draw.text(
                    (rect[0][0] + ((interior_size - w) / 2),
                     rect[0][1] + ((interior_size - h) / 2) - 10),
                    txt, fill="black", font=font
                )

        img.save(filename)

    def solve(self):
        """
        Enforce node consistency, arc consistency then solve the CSP using the backtracking algorithm.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

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
            x_domain_copy = copy.deepcopy(self.domains[x])
            for val in x_domain_copy:
                if not any(val != other for other in self.domains[y]):
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


    def assignment_complete(self, assignement):
        return len(self.domains) == len(assignement)

    def assignment_consistent(self, assignement):
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

    def order_domain_values(self, var, assignment):   # Least constraining value (LCV) heuristic
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        var_values = self.domains[var]   
        var_neighbors = self.sudoku.neighbors(var)
        conflicts = {val : 0 for val in var_values}
        for val in var_values:
            for neignbor in var_neighbors:
                if neignbor in assignment:
                    continue
                if val in self.domains[neignbor]:
                    conflicts[val] += 1
        
        # look for the key with smallest value 
        return sorted(conflicts , key = lambda value : conflicts[value])
        

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to integers (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for val in self.order_domain_values(var, assignment):
            assignment_copy = copy.deepcopy(assignment)
            assignment_copy[var] = val
            if self.assignment_consistent(assignment_copy):
                result = self.backtrack(assignment_copy)
                if result is not None:
                    return result
        return None
    
    def get_digit_from_assignement(self, assignement, i, j):
        for var in assignement:
            if var.i == i and var.j == j:
                return assignement[var]
        return None


def main():
    
    # Check usage
    if len(sys.argv) != 3:
        sys.exit("Invalid usage")

    # Parse command-line arguments
    file_name = sys.argv[1]
    output_file_name = sys.argv[2]

    # Generate sudoku
    sudoku = Sudoku(file_name)
    creator = SudokuCreator(sudoku)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.save(assignment, output_file_name)


if __name__ == "__main__":
    main()
