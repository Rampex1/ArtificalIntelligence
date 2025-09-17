import sys, parse, grader

def number_of_attacks(problem):
    #Your p6 code here
    queens = problem
    n = 8

    def total_conflicts(modified_queens):
        count = 0
        for i in range(len(modified_queens)):
            r1, c1 = modified_queens[i]
            for j in range(i+1, len(modified_queens)):
                r2, c2 = modified_queens[j]
                if r1 == r2 or c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
                    count += 1
        return count

    result = []
    for r in range(n):
        row_vals = []
        for c in range(n):
            modified = [(qr, qc) for (qr, qc) in queens if qc != c]
            modified.append((r, c))
            row_vals.append(f"{total_conflicts(modified):2d}")
        result.append(" ".join(row_vals))

    solution = "\n".join(result)
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 6
    grader.grade(problem_id, test_case_id, number_of_attacks, parse.read_8queens_search_problem)