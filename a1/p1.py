import sys, grader, parse

from parse import read_graph_search_problem

def dfs_search(problem):
    #Your p1 code here
    start, goal, graph = problem['start_state'], problem['goal_state'], problem['graph']

    exploration = []
    path = []
    visited = set()

    def dfs(node):
        if node in visited:
            return False

        visited.add(node)
        path.append(node)

        if node == goal:
            return True

        exploration.append(node)
        for neighbor, value in reversed(graph[node]):
            if dfs(neighbor):
                return True

        path.pop()
        return False

    dfs(start)

    solution_lines = [" ".join(exploration), " ".join(path)]
    solution = '\n'.join(solution_lines)
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, dfs_search, parse.read_graph_search_problem)
