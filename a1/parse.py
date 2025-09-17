import os, sys
from collections import defaultdict

def read_graph_search_problem(file_path):
    #Your p1 code here
    with open(file_path, 'r') as file:
        lines = file.readlines()

    start_state = lines[0].strip().split(': ')[1]
    goal_state = lines[1].strip().split(': ')[1]

    graph = defaultdict(list)
    for line in lines[2:]:
        if line.strip():
            parts = line.strip().split(' ')

            if len(parts) == 3:
                graph[parts[0]].append((parts[1], parts[2]))

    problem = {
        'start_state': start_state,
        'goal_state': goal_state,
        'graph': graph
    }

    return problem

def read_8queens_search_problem(file_path):
    #Your p6 code here
    problem = ''
    return problem

if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        if int(problem_id) <= 5:
            problem = read_graph_search_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        else:
            problem = read_8queens_search_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')