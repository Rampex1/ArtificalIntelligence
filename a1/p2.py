import sys, grader, parse
from collections import deque


def bfs_search(problem):
    #Your p2 code here
    start, goal, graph = problem['start_state'], problem['goal_state'], problem['graph']

    q = deque([(start, [start])])
    visited = set()
    exploration = []
    final_path = []

    while q:
        node, path = q.popleft()

        if node in visited:
            continue

        visited.add(node)

        if node == goal:
            final_path = path
            break

        exploration.append(node)

        for neighbor, _ in graph[node]:
            if neighbor not in visited:
                new_path = path + [neighbor]
                q.append((neighbor, new_path))

    solution_lines = [" ".join(exploration), " ".join(final_path)]
    solution = '\n'.join(solution_lines)
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 2
    grader.grade(problem_id, test_case_id, bfs_search, parse.read_graph_search_problem)