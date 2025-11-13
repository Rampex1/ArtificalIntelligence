def read_grid_mdp_problem_p1(file_path):
    #Your p1 code here

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    problem = {}
    i = 0

    while i < len(lines):
        line = lines[i]

        if line.startswith('seed:'):
            problem['seed'] = int(line.split(':')[1].strip())
        elif line.startswith('noise:'):
            problem['noise'] = float(line.split(':')[1].strip())
        elif line.startswith('livingReward:'):
            problem['livingReward'] = float(line.split(':')[1].strip())
        elif line == 'grid:':
            grid = []
            i += 1
            while i < len(lines) and lines[i] != 'policy:':
                row = lines[i].split()
                grid.append(row)
                i += 1
            problem['grid'] = grid
            continue
        elif line == 'policy:':
            policy = []
            i += 1
            while i < len(lines):
                row = lines[i].split()
                policy.append(row)
                i += 1
            problem['policy'] = policy
            break

        i += 1

    return problem


def read_grid_mdp_problem_p2(file_path):
    #Your p2 code here

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    problem = {}
    i = 0

    while i < len(lines):
        line = lines[i]

        if line.startswith('discount:'):
            problem['discount'] = float(line.split(':')[1].strip())
        elif line.startswith('noise:'):
            problem['noise'] = float(line.split(':')[1].strip())
        elif line.startswith('livingReward:'):
            problem['livingReward'] = float(line.split(':')[1].strip())
        elif line.startswith('iterations:'):
            problem['iterations'] = int(line.split(':')[1].strip())
        elif line == 'grid:':
            grid = []
            i += 1
            while i < len(lines) and lines[i] != 'policy:':
                row = lines[i].split()
                grid.append(row)
                i += 1
            problem['grid'] = grid
            continue
        elif line == 'policy:':
            policy = []
            i += 1
            while i < len(lines):
                row = lines[i].split()
                policy.append(row)
                i += 1
            problem['policy'] = policy
            break

        i += 1

    return problem

def read_grid_mdp_problem_p3(file_path):
    #Your p3 code here

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    problem = {}
    i = 0

    while i < len(lines):
        line = lines[i]

        if line.startswith('discount:'):
            problem['discount'] = float(line.split(':')[1].strip())
        elif line.startswith('noise:'):
            problem['noise'] = float(line.split(':')[1].strip())
        elif line.startswith('livingReward:'):
            problem['livingReward'] = float(line.split(':')[1].strip())
        elif line.startswith('iterations:'):
            problem['iterations'] = int(line.split(':')[1].strip())
        elif line == 'grid:':
            grid = []
            i += 1
            while i < len(lines):
                row = lines[i].split()
                grid.append(row)
                i += 1
            problem['grid'] = grid
            break

        i += 1

    return problem