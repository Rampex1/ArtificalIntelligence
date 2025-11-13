import sys, grader, parse


def value_iteration(problem):
    # ---------------------- PARAMETERS ----------------------
    DISCOUNT = problem['discount']
    NOISE = problem['noise']
    LIVING_REWARD = problem['livingReward']
    ITERATIONS = problem['iterations']
    GRID = problem['grid']

    R = len(GRID)
    C = len(GRID[0])
    V = [[0.0 for _ in range(C)] for _ in range(R)]
    all_actions = ['N', 'E', 'S', 'W']

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

    # -------------------- START ALGORITHM ----------------------------
    return_value += f"V_k=0\n"
    return_value += print_values(V, GRID)

    for k in range(1, ITERATIONS):
        V_new = [[0.0 for _ in range(C)] for _ in range(R)]
        policy = [['' for _ in range(C)] for _ in range(R)]

        for r in range(R):
            for c in range(C):
                cell = GRID[r][c]

                # CASE 1: Skip walls
                if cell == '#':
                    V_new[r][c] = 0.0
                    policy[r][c] = '#'
                    continue

                # CASE 2: Terminal state
                try:
                    terminal_reward = float(cell)
                    is_terminal = True
                except:
                    is_terminal = False

                if is_terminal:
                    V_new[r][c] = terminal_reward
                    policy[r][c] = 'x'
                    continue

                # CASE 3: Non-terminal state
                max_value = float('-inf')
                best_action = 'N'

                for action in all_actions:
                    expected_value = 0.0

                    # Determine possible action
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

                        # Check if move is valid else stay in place
                        if (0 <= new_r < R and
                                0 <= new_c < C and
                                GRID[new_r][new_c] != '#'):
                            next_r, next_c = new_r, new_c
                        else:
                            next_r, next_c = r, c

                        # Add to expected value
                        reward = LIVING_REWARD
                        expected_value += prob * (reward + DISCOUNT * V[next_r][next_c])

                    # Update best action
                    if expected_value > max_value:
                        max_value = expected_value
                        best_action = action

                V_new[r][c] = max_value
                policy[r][c] = best_action

        # Update V and print iteration
        V = V_new
        return_value += f"V_k={k}\n"
        return_value += print_values(V, GRID)
        return_value += f"pi_k={k}\n"
        return_value += print_policy(policy)

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


def print_policy(policy):
    """
    This helper function helps to print policy in the expected output form
    """
    output = ''
    R = len(policy)
    C = len(policy[0])

    for r in range(R):
        for c in range(C):
            action = policy[r][c]
            output += '| {} |'.format(action)
        output += '\n'

    return output

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    #test_case_id = -4
    problem_id = 3
    grader.grade(problem_id, test_case_id, value_iteration, parse.read_grid_mdp_problem_p3)