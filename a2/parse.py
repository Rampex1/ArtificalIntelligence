import os, sys
def read_layout_problem(file_path):
    #Your p1 code here
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Extract seed from first line
    seedLine = lines[0].strip()
    seed = int(seedLine.split(':')[1].strip())

    # Parse the layout grid
    layout = []
    for i in range(1, len(lines)):
        line = lines[i].rstrip('\n')
        layout.append(line)

    # Store problem data in a dictionary
    problem = {
        'seed': seed,
        'layout': layout,
        'height': len(layout),
        'width': len(layout[0]) if layout else 0
    }

    return problem

if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        problem = read_layout_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')