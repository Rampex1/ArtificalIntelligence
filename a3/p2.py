import sys, grader, parse


def POLICY_evaluation(problem):
    # ------------------- PARAMETERS ------------------------
    DISCOUNT = problem['discount']
    NOISE = problem['noise']
    LIVING_REWARD = problem['livingReward']
    ITERATIONS = problem['iterations']
    GRID = problem['grid']
    POLICY = problem['policy']

    R = len(GRID)
    C = len(GRID[0])
    V = [[0.0 for _ in range(C)] for _ in range(R)]

    # Movement deltas
    move_delta = {
        'N': (-1, 0),
        'E': (0, 1),
        'S': (1, 0),
        'W': (0, -1)
    }

    # Perpendicular actions
    perpendicular = {
        'N': ['E', 'W'],
        'E': ['S', 'N'],
        'S': ['W', 'E'],
        'W': ['N', 'S']
    }

    return_value = ''

    # ----------------------- START ALGORITHM -------------------
    return_value += f"V^pi_k=0\n"
    return_value += print_values(V, GRID)

    for k in range(1, ITERATIONS):
        V_new = [[0.0 for _ in range(C)] for _ in range(R)]

        for r in range(R):
            for c in range(C):
                cell = GRID[r][c]
                action = POLICY[r][c]

                # CASE 1: Skip walls
                if cell == '#':
                    V_new[r][c] = 0.0
                    continue

                # CASE 2: Terminal state
                if action == 'exit':
                    try:
                        V_new[r][c] = float(cell)
                    except:
                        V_new[r][c] = 0.0
                    continue

                # CASE 3: Non-terminal state
                expected_value = 0.0

                # Determine possible actions
                perp_actions = perpendicular[action]
                actions_probs = [
                    (action, 1 - 2 * NOISE),
                    (perp_actions[0], NOISE),
                    (perp_actions[1], NOISE)
                ]

                # Determine resulting state for each action
                for actual_action, prob in actions_probs:
                    delta = move_delta[actual_action]
                    new_r = r + delta[0]
                    new_c = c + delta[1]

                    # Check if move is valid, else stay in place
                    if (0 <= new_r < R and
                            0 <= new_c < C and
                            GRID[new_r][new_c] != '#'):
                        next_r, next_c = new_r, new_c
                    else:
                        next_r, next_c = r, c

                    # Add to expected value
                    reward = LIVING_REWARD
                    expected_value += prob * (reward + DISCOUNT * V[next_r][next_c])

                V_new[r][c] = expected_value

        # Update and print values
        V = V_new
        return_value += f"V^pi_k={k}\n"
        return_value += print_values(V, GRID)

    return return_value[:-1]


def print_values(V, GRID):
    """
    This helper function helps to print values in the expected output form
    """
    output = ''
    R = len(V)
    C = len(V[0])

    for r in range(R):
        for c in range(C):
            if GRID[r][c] == '#':
                output += '| ##### |'
            else:
                output += '|{:7.2f}|'.format(V[r][c])
        output += '\n'

    return output

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    #test_case_id = -7
    problem_id = 2
    grader.grade(problem_id, test_case_id, POLICY_evaluation, parse.read_grid_mdp_problem_p2)