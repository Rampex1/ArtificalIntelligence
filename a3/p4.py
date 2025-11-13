"""
Problem 4: Q-Value TD Learning

The goal is to apply temporal difference learning of Q values to the test case 2 of problem 3
and see if I can get an optimal policy.

INSTRUCTIONS:
- Discount, noise, living reward extracted from problem
- Start from initial Q values = 0
- Use epsilon greedy (with decay) or exploration functions to force exploration
- Implement an appropriate learning rate decay to reach an optimal policy
- Stop iteration when the solution is found
- Run learning algorithm multiple times and output how often optimal policy can be found

RESULTS:
Running the algorithm 10 times on test case 2 of problem 3:
- Successfully finds optimal policy: 10/10 times
- Range of episodes to convergence: 1120 - 2200

HOW TO RUN CODE:
python p4.py
"""

import random
import sys
sys.path.append('.')

def q_learning(problem):
    # ------------------------ PARAMETERS -------------------------

    # These parameters were tuned manually to optimize algorithm success rate
    MAX_EPISODES = 3000
    MAX_STEPS_PER_EPISODE = 100
    INITIAL_EPSILON = 1.0
    EPSILON_DECAY = 0.995
    MIN_EPSILON = 0.01
    INITIAL_ALPHA = 0.5
    ALPHA_DECAY = 0.9995
    MIN_ALPHA = 0.01
    CONVERGENCE_THRESHOLD = 50

    # -------------------- PROBLEM PARAMETERS -----------------------
    discount = problem['discount']
    noise = problem['noise']
    living_reward = problem['livingReward']
    grid = problem['grid']

    R = len(grid)
    C = len(grid[0])

    # Initialize Q-values
    Q = {}
    for r in range(R):
        for c in range(C):
            if grid[r][c] != '#':
                for action in ['N', 'E', 'S', 'W']:
                    Q[(r, c, action)] = 0.0

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

    all_actions = ['N', 'E', 'S', 'W']
    epsilon = INITIAL_EPSILON
    alpha = INITIAL_ALPHA
    previous_policy = None
    stable_count = 0

    # ---------------------- START ALGORITHM -------------------------------
    for episode in range(MAX_EPISODES):
        # Random start state
        valid_starts = []
        for r in range(R):
            for c in range(C):
                if grid[r][c] in ['S', '_']:
                    valid_starts.append((r, c))
        current_row, current_col = random.choice(valid_starts)

        # Run episode
        for step in range(MAX_STEPS_PER_EPISODE):
            cell = grid[current_row][current_col]
            # Check terminal state
            try:
                float(cell)
                is_terminal = True
            except:
                is_terminal = False
            if is_terminal: break

            # Choose action using epsilon-greedy
            if random.random() < epsilon:
                action = random.choice(all_actions)
            else:
                max_q = float('-inf')
                best_action = all_actions[0]
                for a in all_actions:
                    q_val = Q.get((current_row, current_col, a), 0.0)
                    if q_val > max_q:
                        max_q = q_val
                        best_action = a
                action = best_action

            # Simulate action
            perp_actions = perpendicular[action]
            actual_action = random.choices(
                population=[action] + perp_actions,
                weights=[1 - 2 * noise, noise, noise]
            )[0]

            # Execute action
            delta = move_delta[actual_action]
            new_row = current_row + delta[0]
            new_col = current_col + delta[1]

            # Check if move is valid else stay
            if (0 <= new_row < R and
                    0 <= new_col < C and
                    grid[new_row][new_col] != '#'):
                next_row, next_col = new_row, new_col
            else:
                next_row, next_col = current_row, current_col

            # Get reward
            next_cell = grid[next_row][next_col]
            try:
                reward = float(next_cell)
            except:
                reward = living_reward

            # Get max Q-value for next state
            try:
                float(next_cell)
                max_q_next = 0.0
            except:
                max_q_next = float('-inf')
                for a in all_actions:
                    q_val = Q.get((next_row, next_col, a), 0.0)
                    if q_val > max_q_next:
                        max_q_next = q_val
                if max_q_next == float('-inf'):
                    max_q_next = 0.0

            # Q-Learning update
            old_q = Q.get((current_row, current_col, action), 0.0)
            sample = reward + discount * max_q_next
            Q[(current_row, current_col, action)] = (1 - alpha) * old_q + alpha * sample

            # Move to next state
            current_row, current_col = next_row, next_col

        # Decay epsilon and alpha
        epsilon = max(MIN_EPSILON, epsilon * EPSILON_DECAY)
        alpha = max(MIN_ALPHA, alpha * ALPHA_DECAY)

        # Check for convergence every 10 episodes
        if episode % 10 == 0:
            current_policy = extract_policy(Q, grid, all_actions)

            if previous_policy == current_policy:
                stable_count += 1
            else:
                stable_count = 0

            if stable_count >= CONVERGENCE_THRESHOLD:
                print(f"Converged at episode {episode}")
                break

            previous_policy = current_policy

    return Q


def extract_policy(Q, grid, all_actions):
    """Extract policy from Q-values"""
    R = len(grid)
    C = len(grid[0])
    policy = []

    for r in range(R):
        row_policy = []
        for c in range(C):
            cell = grid[r][c]

            if cell == '#':
                row_policy.append('#')
            else:
                try:
                    float(cell)
                    row_policy.append('x')
                except:
                    max_q = float('-inf')
                    best_action = 'N'
                    for a in all_actions:
                        q_val = Q.get((r, c, a), 0.0)
                        if q_val > max_q:
                            max_q = q_val
                            best_action = a
                    row_policy.append(best_action)

        policy.append(row_policy)

    return policy


def print_policy(policy):
    """Print policy in expected format"""
    for row in policy:
        for action in row:
            print(f"| {action} |", end="")
        print()


def policies_match(policy1, policy2):
    """Check if two policies are identical"""
    if len(policy1) != len(policy2):
        return False
    for i in range(len(policy1)):
        if len(policy1[i]) != len(policy2[i]):
            return False
        for j in range(len(policy1[i])):
            if policy1[i][j] != policy2[i][j]:
                return False
    return True

def read_grid_mdp_problem_p3(file_path):
    """
    This code was copied from P3
    """

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


if __name__ == "__main__":
    # Problem 3, Test 2
    problem = read_grid_mdp_problem_p3('test_cases/p3/2.prob')

    # Known optimal policy from A3 instructions
    optimal_policy = [
        ['E', 'E', 'E', 'x'],
        ['N', '#', 'W', 'x'],
        ['N', 'W', 'W', 'S']
    ]

    print("Running Q-Learning algorithm 10 times...\n")

    num_runs = 10
    successes = 0

    for run in range(num_runs):
        print(f"Run {run + 1}/10:")

        # Run Q-Learning
        Q = q_learning(problem)
        learned_policy = extract_policy(Q, problem['grid'], ['N', 'E', 'S', 'W'])

        # Check for match
        if policies_match(learned_policy, optimal_policy):
            print("Found optimal policy")
            successes += 1
        else:
            print("Found Suboptimal policy")
            print_policy(learned_policy)

        print()

    print(f"\nRESULT: {successes}/{num_runs} successful runs")
    print(f"Success rate: {successes / num_runs * 100:.1f}%")

    print("\nOptimal policy:")
    print_policy(optimal_policy)
