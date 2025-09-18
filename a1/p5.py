import heapq
import sys, parse, grader

def astar_search(problem):
    #Your p5 code here
    start, goal, graph = problem['start_state'], problem['goal_state'], problem['graph']
    heuristic = problem['heuristic']

    start_h = heuristic[start]
    # One problem I had here is that when two f_cost are tied, the tiebreaker would be g_cost.
    # However, it seems that the tiebreaker should be the insertion order instead. That is why
    # I am using a counter here to track insertion order
    counter = 0
    pq = [(start_h, counter, 0, start, [start])]
    counter += 1
    visited = set()
    exploration = []
    final_path = []

    while pq:
        f_cost, insertion_order, g_cost, node, path = heapq.heappop(pq)

        if node in visited:
            continue

        visited.add(node)

        if node == goal:
            final_path = path
            break

        exploration.append(node)

        for neighbor, edge_cost in graph[node]:
            if neighbor not in visited:
                new_g_cost = g_cost + float(edge_cost)
                neighbor_h_cost = heuristic[neighbor]
                new_f_cost = new_g_cost + neighbor_h_cost
                new_path = path + [neighbor]
                heapq.heappush(pq, (new_f_cost, counter, new_g_cost, neighbor, new_path))
                counter += 1

    solution_lines = [" ".join(exploration), " ".join(final_path)]
    solution = '\n'.join(solution_lines)
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 5
    grader.grade(problem_id, test_case_id, astar_search, parse.read_graph_search_problem)