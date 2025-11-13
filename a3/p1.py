import sys, grader, parse
import random


def play_episode(problem):
    #----------------------- PARAMETERS ------------------------------
    SEED = problem['seed']
    NOISE = problem['noise']
    LIVING_REWARD = problem['livingReward']
    GRID = problem['grid']
    POLICY = problem['policy']

    R, C = len(GRID), len(GRID[0])
    random.seed(SEED, version=1)


    #----------------------- VARIABLES -------------------------------
    start_row, start_col = find_start_state(GRID, R, C)
    current_row, current_col = start_row, start_col
    cumulative_reward = 0.0
    experience = ''

    # Perpendicular actions
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

    # ---------------------- START ALGORITHM ---------------------------
    experience += "Start state:\n"
    experience += print_grid(GRID, current_row, current_col)
    experience += f"Cumulative reward sum: {cumulative_reward}\n"

    while True:
        intended_action = POLICY[current_row][current_col]

        # Terminal State
        if intended_action == 'exit':
            # Get reward
            cell_value = GRID[current_row][current_col]
            reward = float(cell_value)

            cumulative_reward += reward
            experience += "-------------------------------------------- \n"
            experience += "Taking action: exit (intended: exit)\n"
            experience += f"Reward received: {reward}\n"
            experience += "New state:\n"
            experience += print_grid(GRID, start_row, start_col, hide_player=True)
            experience += f"Cumulative reward sum: {round(cumulative_reward, 10)}"
            break

        # Determine move
        perp_actions = perpendicular[intended_action]
        actual_action = random.choices(
            population=[intended_action] + perp_actions,
            weights=[1 - 2 * NOISE, NOISE, NOISE]
        )[0]

        # Perform move
        delta = move_delta[actual_action]
        new_row = current_row + delta[0]
        new_col = current_col + delta[1]

        if 0 <= new_row < len(GRID) and 0 <= new_col < len(GRID[new_row]) and GRID[new_row][new_col] != '#':
            current_row, current_col = new_row, new_col

        # Get reward
        reward = LIVING_REWARD
        cumulative_reward += reward

        experience += "-------------------------------------------- \n"
        experience += f"Taking action: {actual_action} (intended: {intended_action})\n"
        experience += f"Reward received: {reward}\n"
        experience += "New state:\n"
        experience += print_grid(GRID, current_row, current_col)
        experience += f"Cumulative reward sum: {round(cumulative_reward, 10)}\n"

    return experience

def find_start_state(grid, row_count, col_count) -> (int, int):
    """
    This helper functions allows us to find the initial starting point of the player
    """
    start_row, start_col = None, None
    for r in range(row_count):
        for c in range(col_count):
            if grid[r][c] == 'S':
                start_row, start_col = r, c
                break

    return start_row, start_col


def print_grid(grid, player_row, player_col, hide_player=False) -> str:
    """
    This helper functions helps print a grid in the output.
    It goes over the rows and columns and parses according to the expected output format.
    """
    output = ''
    row, col = len(grid), len(grid[0])
    for r in range(row):
        for c in range(col):
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
                    output += f'{cell:>5}'
        output += '\n'
    return output


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    #test_case_id = 1
    problem_id = 1
    grader.grade(problem_id, test_case_id, play_episode, parse.read_grid_mdp_problem_p1)