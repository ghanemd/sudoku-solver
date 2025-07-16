import sys

class Variable:
    def __init__(self, i, j):
        """
        Create a new variable containing the row number and the column number.
        """
        self.i = i
        self.j = j

    def __eq__(self, other):
        return self.i == other.i and self.j == other.j

    def __str__(self):
        return f"i = {self.i}, j = {self.j}"
    
    def __hash__(self):
        return hash((self.i, self.j))


class Sudoku:
    def __init__(self, structure_file):

        # Determine the structure of the sudoku
        self.structure = []
        try:
            with open(structure_file) as file:
                for line in file:
                    row = []
                    for num in line.strip():
                        if num == "0":
                            row.append(None)
                        else:
                            row.append(int(num))
                    self.structure.append(row)
        except FileNotFoundError:
            sys.exit("File not found")
        self.height = len(self.structure)
        self.width = len(self.structure[0])

        self.variables = set()
        for i in range(self.height):
            for j in range(self.width):
                self.variables.add(Variable(i, j))


    def neighbors(self, var):
        """
        Given a variable, return a set of its neighbors.
        """
        return set(
            v for v in self.variables
            if v != var and (v.i == var.i or v.j == var.j or (v.i // 3 == var.i // 3 and v.j // 3 == var.j // 3))
        )
