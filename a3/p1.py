import sys, grader, parse
import random


def play_episode(problem):
    # Parameters
    seed = problem['seed']
    noise = problem['noise']
    living_reward = problem['livingReward']
    grid = problem['grid']
    policy = problem['policy']

    # Set random seed
    if seed != -1:
        random.seed(seed, version=1)

    # Find start state
    start_row, start_col = None, None
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == 'S':
                start_row, start_col = r, c
                break
        if start_row is not None:
            break

    # Initialize
    current_row, current_col = start_row, start_col
    cumulative_reward = 0.0
    experience = ''

    # Direction mappings for perpendicular actions
    perpendicular = {
        'N': ['E', 'W'],
        'E': ['S', 'N'],
        'S': ['W', 'E'],
        'W': ['N', 'S']
    }

    # Movement deltas
    move_delta = {
        'N': (-1, 0),
        'E': (0, 1),
        'S': (1, 0),
        'W': (0, -1)
    }

    # Print initial state
    experience += "Start state:\n"
    experience += print_grid(grid, current_row, current_col)
    experience += f"Cumulative reward sum: {cumulative_reward}\n"

    # Play episode
    while True:
        # Get intended action from policy
        intended_action = policy[current_row][current_col]

        # Check if terminal state
        if intended_action == 'exit':
            experience += "-------------------------------------------- \n"
            experience += f"Taking action: exit (intended: exit)\n"

            # Get reward from grid
            cell_value = grid[current_row][current_col]
            try:
                reward = float(cell_value)
            except:
                reward = 0.0

            cumulative_reward += reward
            experience += f"Reward received: {reward}\n"
            experience += "New state:\n"
            experience += print_grid(grid, start_row, start_col, hide_player=True)
            experience += f"Cumulative reward sum: {round(cumulative_reward, 10)}"
            break

        # Determine actual action with noise
        if noise == 0:
            actual_action = intended_action
        else:
            perp_actions = perpendicular[intended_action]
            actual_action = random.choices(
                population=[intended_action] + perp_actions,
                weights=[1 - 2 * noise, noise, noise]
            )[0]

        experience += "-------------------------------------------- \n"
        experience += f"Taking action: {actual_action} (intended: {intended_action})\n"

        # Try to move
        delta = move_delta[actual_action]
        new_row = current_row + delta[0]
        new_col = current_col + delta[1]

        # Check if move is valid (not out of bounds, not a wall)
        if (0 <= new_row < len(grid) and
                0 <= new_col < len(grid[new_row]) and
                grid[new_row][new_col] != '#'):
            current_row, current_col = new_row, new_col

        # Get reward (living reward for non-terminal states)
        reward = living_reward
        cumulative_reward += reward

        experience += f"Reward received: {reward}\n"
        experience += "New state:\n"
        experience += print_grid(grid, current_row, current_col)
        experience += f"Cumulative reward sum: {round(cumulative_reward, 10)}\n"

    return experience


def print_grid(grid, player_row, player_col, hide_player=False):
    output = ''
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if r == player_row and c == player_col and not hide_player:
                output += '    P'
            else:
                cell = grid[r][c]
                if cell == 'S':
                    output += '    S'
                elif cell == '#':
                    output += '    #'
                elif cell == '_':
                    output += '    _'
                else:
                    # It's a number (reward) - right align in 5 characters
                    output += f'{cell:>5}'
        output += '\n'
    return output


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    #test_case_id = 1
    problem_id = 1
    grader.grade(problem_id, test_case_id, play_episode, parse.read_grid_mdp_problem_p1)