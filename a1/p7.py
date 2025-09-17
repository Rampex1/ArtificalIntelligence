import sys, parse, grader
from copy import deepcopy


def better_board(problem):
    #Your p7 code here
    queens = problem
    n = 8

    def total_conflicts(modified_queens):
        """Calculate total conflicts between queens"""
        count = 0
        for i in range(len(modified_queens)):
            r1, c1 = modified_queens[i]
            for j in range(i + 1, len(modified_queens)):
                r2, c2 = modified_queens[j]
                if r1 == r2 or c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
                    count += 1
        return count

    def queens_to_board_string(queen_positions):
        """Convert list of queen positions to 8x8 board string"""
        board = [['.' for _ in range(n)] for _ in range(n)]
        for r, c in queen_positions:
            board[r][c] = 'q'

        result = []
        for row in board:
            result.append(' '.join(row))
        return '\n'.join(result)

    current_conflicts = total_conflicts(queens)
    best_conflicts = current_conflicts
    best_board = queens[:]

    # Try moving each queen to every position in its column
    for col in range(n):
        # Find the queen in this column
        current_queen_row = None
        for qr, qc in queens:
            if qc == col:
                current_queen_row = qr
                break

        if current_queen_row is None:
            continue

        for new_row in range(n):
            if new_row == current_queen_row:
                continue

            modified_queens = [(qr, qc) for (qr, qc) in queens if qc != col]
            modified_queens.append((new_row, col))

            conflicts = total_conflicts(modified_queens)

            if conflicts < best_conflicts:
                best_conflicts = conflicts
                best_board = modified_queens[:]

    return queens_to_board_string(best_board)

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 7
    grader.grade(problem_id, test_case_id, better_board, parse.read_8queens_search_problem)