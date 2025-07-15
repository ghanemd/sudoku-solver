class SudokuCreator:
    def __init__(self, sudoku):
        pass


    def solve(self):
        """
        Enforce node consistency, arc consistency then solve the CSP using the backtracking algorithm.
        """
        self.enforce_node_consistency()
        self.ac3()
        self.backtrack(dict())

    def enforce_node_consistency(self):
        pass

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
    pass


if __name__ == "__main__":
    main()
