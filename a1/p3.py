import heapq
import sys, parse, grader

def ucs_search(problem):
    #Your p3 code here
    start, goal, graph = problem['start_state'], problem['goal_state'], problem['graph']

    pq = [(0, start, [start])]
    visited = set()
    exploration = []
    final_path = []

    while pq:
        cost, node, path = heapq.heappop(pq)

        if node in visited:
            continue

        visited.add(node)

        if node == goal:
            final_path = path
            break

        exploration.append(node)

        for neighbor, edge_cost in graph[node]:
            if neighbor not in visited:
                new_cost = cost + float(edge_cost)
                new_path = path + [neighbor]
                heapq.heappush(pq, (new_cost, neighbor, new_path))

    solution_lines = [" ".join(exploration), " ".join(final_path)]
    solution = '\n'.join(solution_lines)
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 3
    grader.grade(problem_id, test_case_id, ucs_search, parse.read_graph_search_problem)