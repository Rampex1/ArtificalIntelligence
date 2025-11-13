import sys, grader, parse


def policy_evaluation(problem):
    # Extract problem parameters
    discount = problem['discount']
    noise = problem['noise']
    living_reward = problem['livingReward']
    iterations = problem['iterations']
    grid = problem['grid']
    policy = problem['policy']

    rows = len(grid)
    cols = len(grid[0])

    # Initialize values to 0
    V = [[0.0 for _ in range(cols)] for _ in range(rows)]

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

    # Print initial values (k=0)
    return_value += f"V^pi_k=0\n"
    return_value += print_values(V, grid)

    # Perform policy evaluation iterations
    for k in range(1, iterations + 1):
        V_new = [[0.0 for _ in range(cols)] for _ in range(rows)]

        for r in range(rows):
            for c in range(cols):
                cell = grid[r][c]
                action = policy[r][c]

                # Skip walls
                if cell == '#':
                    V_new[r][c] = 0.0
                    continue

                # Terminal states (exit action)
                if action == 'exit':
                    try:
                        V_new[r][c] = float(cell)
                    except:
                        V_new[r][c] = 0.0
                    continue

                # Non-terminal states - compute expected value
                expected_value = 0.0

                # Determine possible actions with probabilities
                if noise == 0:
                    actions_probs = [(action, 1.0)]
                else:
                    perp_actions = perpendicular[action]
                    actions_probs = [
                        (action, 1 - 2 * noise),
                        (perp_actions[0], noise),
                        (perp_actions[1], noise)
                    ]

                # For each possible action outcome
                for actual_action, prob in actions_probs:
                    # Determine resulting state
                    delta = move_delta[actual_action]
                    new_r = r + delta[0]
                    new_c = c + delta[1]

                    # Check if move is valid
                    if (0 <= new_r < rows and
                            0 <= new_c < cols and
                            grid[new_r][new_c] != '#'):
                        next_r, next_c = new_r, new_c
                    else:
                        # Hit wall or boundary - stay in place
                        next_r, next_c = r, c

                    # Add to expected value: P(s'|s,a) * [R(s,a,s') + γ*V(s')]
                    reward = living_reward
                    expected_value += prob * (reward + discount * V[next_r][next_c])

                V_new[r][c] = expected_value

        # Update V
        V = V_new

        # Print values for this iteration
        return_value += f"V^pi_k={k}\n"
        return_value += print_values(V, grid)

    return return_value


def print_values(V, grid):
    output = ''
    rows = len(V)
    cols = len(V[0])

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '#':
                output += '|#####|'
            else:
                output += '|{:7.2f}|'.format(V[r][c])
        output += '\n'

    return output

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    #test_case_id = -7
    problem_id = 2
    grader.grade(problem_id, test_case_id, policy_evaluation, parse.read_grid_mdp_problem_p2)