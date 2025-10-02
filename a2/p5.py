import sys, parse
import time, os, copy
import random  # Keep random for the Ghost's tie-breaking (if needed)

# --- Score Constants (Reused from p4/p3) ---
EAT_FOOD_SCORE = 10
PACMAN_EATEN_SCORE = -500
PACMAN_WIN_SCORE = 500
PACMAN_MOVING_SCORE = -1

# --- Global Ghost Order ---
# This is crucial for the minimax turn order
GHOST_ORDER = ['W', 'X', 'Y', 'Z']


def min_max_multiple_ghosts(problem, k):
    # Your p5 code here

    # 1. INITIALIZE GAME STATE (Reused from p4)
    pacmanPos = None
    ghostPositions = {}
    foodPositions = set()

    currentLayout = [list(row) for row in problem['layout']]
    for r in range(len(currentLayout)):
        for c in range(len(currentLayout[r])):
            cell = currentLayout[r][c]
            if cell == 'P':
                pacmanPos = (r, c)
            elif cell in GHOST_ORDER:
                ghostPositions[cell] = (r, c)
            elif cell == '.':
                foodPositions.add((r, c))

    # Sort the ghosts currently in the game
    ghostOrder = sorted([g for g in GHOST_ORDER if g in ghostPositions.keys()])
    num_ghosts = len(ghostOrder)

    # Initial state representation for search and logging
    initial_state = {
        'layout': currentLayout,
        'pacmanPos': pacmanPos,
        'ghostPositions': ghostPositions,
        'foodPositions': foodPositions,
        'score': 0,
        'turn': 0  # 0 for Pacman, 1 to num_ghosts for the ghosts
    }

    solution = f"seed: {problem.get('seed', 'N/A')}\n0\n"
    solution += '\n'.join(''.join(row) for row in initial_state['layout']) + '\n'

    score = 0
    moveCount = 0
    currentState = initial_state

    # 2. GAME LOOP
    while True:
        moveCount += 1

        # ---------------- PACMAN TURN ----------------

        # Minimax determines the best move for Pacman
        bestMove, bestScore = minimax_search(
            currentState,
            k,
            0,  # Initial depth
            num_ghosts,
            ghostOrder
        )

        pacmanMoves = getValidMoves(currentState['layout'], currentState['pacmanPos'], currentState['ghostPositions'])

        if not pacmanMoves:
            score += PACMAN_EATEN_SCORE
            solution += f"{moveCount}: Pacman has no moves (trapped)\n"
            solution += '\n'.join(''.join(row) for row in currentState['layout']) + '\n'
            solution += f"score: {score}\nWIN: Ghost"
            return solution, 'Ghost'

        # Since Pacman is the maximizer, we take the move from the minimax result
        pacmanMove = bestMove

        # Apply the best move
        newState = apply_pacman_move(currentState, pacmanMove)

        # Update score and state for logging
        score = newState['score']
        pacmanPos = newState['pacmanPos']
        currentState = newState

        # Check Pacman's immediate outcome
        if pacmanPos in currentState['ghostPositions'].values():
            # Collision detected on Pacman's move
            score += PACMAN_EATEN_SCORE
            solution += f"{moveCount}: P moving {pacmanMove}\n"
            solution += '\n'.join(''.join(row) for row in currentState['layout']) + '\n'
            solution += f"score: {score}\nWIN: Ghost"
            return solution, 'Ghost'

        solution += f"{moveCount}: P moving {pacmanMove}\n"
        solution += '\n'.join(''.join(row) for row in currentState['layout']) + '\n'
        solution += f"score: {score}\n"

        # Check Pacman Win condition
        if not currentState['foodPositions']:
            score += PACMAN_WIN_SCORE
            solution += f"WIN: Pacman"
            return solution, 'Pacman'

        # ---------------- GHOSTS TURN ----------------
        for ghostChar in ghostOrder:
            moveCount += 1

            ghostPos = currentState['ghostPositions'][ghostChar]

            # Ghosts move randomly (since minimax only applied to Pacman's turn in this simplified setup)
            # A full adversarial search would require minimax for ghosts too, but the problem structure
            # suggests only Pacman is the rational agent given the constraints.

            ghostMoves = getValidMoves(currentState['layout'], ghostPos, currentState['ghostPositions'], ghostChar)

            if not ghostMoves:
                # Ghost is trapped, just log the state and continue
                solution += f"{moveCount}: {ghostChar} moving \n"
                solution += '\n'.join(''.join(row) for row in currentState['layout']) + '\n'
                solution += f"score: {score}\n"
                continue

            # Random selection for ghost moves (tie-breaking or simple ghost model)
            ghostMove = random.choice(ghostMoves)

            # Apply the ghost move
            newState = apply_ghost_move(currentState, ghostChar, ghostMove)
            currentState = newState

            # Update score and state for logging
            score = newState['score']
            ghostPos = newState['ghostPositions'][ghostChar]

            # Ghost catches Pacman
            if ghostPos == currentState['pacmanPos']:
                score += PACMAN_EATEN_SCORE
                solution += f"{moveCount}: {ghostChar} moving {ghostMove}\n"
                # The layout is already updated inside apply_ghost_move
                solution += '\n'.join(''.join(row) for row in currentState['layout']) + '\n'
                solution += f"score: {score}\nWIN: Ghost"
                return solution, 'Ghost'

            solution += f"{moveCount}: {ghostChar} moving {ghostMove}\n"
            solution += '\n'.join(''.join(row) for row in currentState['layout']) + '\n'
            solution += f"score: {score}\n"


# 3. MINIMAX SEARCH IMPLEMENTATION

def minimax_search(state, k, depth, num_ghosts, ghostOrder):
    """
    Initiates the minimax search from Pacman's turn (agentIndex=0).
    Returns (bestMove, bestScore).
    """

    # Minimax is structured by full rounds: Pacman (Max) -> Ghost 1 (Min) -> ... -> Ghost N (Min)
    # The current agentIndex maps to (0: Pacman, 1: Ghost 1, ..., num_ghosts: Ghost N)

    # We call value_function to start the recursive search
    move = None
    best_score = float('-inf')

    pacmanMoves = getValidMoves(state['layout'], state['pacmanPos'], state['ghostPositions'])

    if not pacmanMoves:
        return None, evaluate_state(state, is_terminal=True, winner='Ghost')

    for current_move in pacmanMoves:
        # Get the state after Pacman's move
        next_state = apply_pacman_move(state, current_move)

        # Start the minimization phase (Ghost 1's turn, agentIndex=1)
        score = value_function(next_state, k, depth + 1, 1, num_ghosts, ghostOrder)

        if score > best_score:
            best_score = score
            move = current_move

    return move, best_score


def value_function(state, k, depth, agentIndex, num_ghosts, ghostOrder):
    """
    Recursively calculates the minimax value for the current agent.
    agentIndex: 0 (Pacman), 1 to num_ghosts (Ghosts).
    """

    # Check for terminal state (win/loss/depth limit)
    winner = check_terminal(state)
    if winner or depth > k * (num_ghosts + 1):
        return evaluate_state(state, is_terminal=bool(winner), winner=winner)

    # Agent is Pacman (Maximizer)
    if agentIndex == 0:
        return max_value(state, k, depth, num_ghosts, ghostOrder)

    # Agent is a Ghost (Minimizer)
    else:
        return min_value(state, k, depth, agentIndex, num_ghosts, ghostOrder)


def max_value(state, k, depth, num_ghosts, ghostOrder):
    """Pacman's turn (agentIndex=0) - Chooses the move that maximizes score."""
    v = float('-inf')

    pacmanMoves = getValidMoves(state['layout'], state['pacmanPos'], state['ghostPositions'])
    if not pacmanMoves:
        return evaluate_state(state, is_terminal=True, winner='Ghost')

    for move in pacmanMoves:
        next_state = apply_pacman_move(state, move)
        # Next turn is the first ghost (agentIndex=1)
        v = max(v, value_function(next_state, k, depth + 1, 1, num_ghosts, ghostOrder))

    return v


def min_value(state, k, depth, agentIndex, num_ghosts, ghostOrder):
    """Ghost's turn (agentIndex > 0) - Chooses the move that minimizes score."""
    v = float('inf')

    ghostChar = ghostOrder[agentIndex - 1]
    ghostPos = state['ghostPositions'][ghostChar]

    ghostMoves = getValidMoves(state['layout'], ghostPos, state['ghostPositions'], ghostChar)
    if not ghostMoves:
        # Ghost is trapped. Pass the turn to the next agent.
        next_agentIndex = (agentIndex + 1) % (num_ghosts + 1)
        return value_function(state, k, depth + 1, next_agentIndex, num_ghosts, ghostOrder)

    for move in ghostMoves:
        next_state = apply_ghost_move(state, ghostChar, move)

        # Determine the next agent: either the next ghost, or Pacman for a new round (agentIndex=0)
        next_agentIndex = (agentIndex + 1) % (num_ghosts + 1)

        v = min(v, value_function(next_state, k, depth + 1, next_agentIndex, num_ghosts, ghostOrder))

    return v


# 4. GAME STATE UTILITY FUNCTIONS

def apply_pacman_move(state, move):
    """Returns a new state dictionary after Pacman makes a move."""
    newState = copy.deepcopy(state)

    oldPos = newState['pacmanPos']
    newPos = applyMove(oldPos, move)

    # Clear old Pacman cell
    newState['layout'][oldPos[0]][oldPos[1]] = ' '

    # Eat food if present
    if newPos in newState['foodPositions']:
        newState['score'] += EAT_FOOD_SCORE
        newState['foodPositions'].remove(newPos)

    newState['score'] += PACMAN_MOVING_SCORE
    newState['pacmanPos'] = newPos

    # Draw Pacman
    newState['layout'][newPos[0]][newPos[1]] = 'P'

    # Collision check is handled by check_terminal/evaluate_state for minimax,
    # but the game loop needs the actual collision check here.

    return newState


def apply_ghost_move(state, ghostChar, move):
    """Returns a new state dictionary after a Ghost makes a move."""
    newState = copy.deepcopy(state)

    oldPos = newState['ghostPositions'][ghostChar]
    newPos = applyMove(oldPos, move)

    # Restore food if ghost leaves a food square
    newState['layout'][oldPos[0]][oldPos[1]] = '.' if oldPos in newState['foodPositions'] else ' '

    newState['ghostPositions'][ghostChar] = newPos

    # Draw Ghost
    newState['layout'][newPos[0]][newPos[1]] = ghostChar

    # Collision check is handled by check_terminal/evaluate_state for minimax,
    # but the game loop needs the actual collision check here.

    return newState


def check_terminal(state):
    """Checks for terminal state (win/loss). Returns 'Pacman', 'Ghost', or None."""

    # Pacman collision
    if state['pacmanPos'] in state['ghostPositions'].values():
        return 'Ghost'

    # Pacman wins
    if not state['foodPositions']:
        return 'Pacman'

    return None


def evaluate_state(state, is_terminal=False, winner=None):
    """
    Evaluation function for Minimax.
    Returns the score of the state.
    """

    # Terminal State Evaluation
    if is_terminal:
        if winner == 'Pacman':
            return state['score'] + PACMAN_WIN_SCORE
        elif winner == 'Ghost':
            return state['score'] + PACMAN_EATEN_SCORE

        # If terminal but no winner (e.g., max depth reached)
        # Fall through to heuristic

    # Heuristic Evaluation (Reused from p4's evaluatePosition, but adapted for the state)

    pacmanPos = state['pacmanPos']
    ghostPositions = state['ghostPositions']
    foodPositions = state['foodPositions']

    current_score = state['score']

    if not foodPositions:
        # Should be caught by terminal check, but as a safeguard
        return current_score + 1000

        # Closest food distance
    minFoodDist = min(manhattanDistance(pacmanPos, food) for food in foodPositions)

    # Closest ghost distance
    minGhostDist = min(manhattanDistance(pacmanPos, gPos) for gPos in ghostPositions.values())

    # Heuristic component based on food and ghost proximity

    # Penalty for being near ghost (more severe than p4 since this is the only lookahead)
    if minGhostDist <= 1:
        # If Pacman is next to a ghost, this is an immediate loss in the next step
        # unless the ghost moves away. We apply a huge penalty.
        return current_score - 5000
    elif minGhostDist <= 2:
        return current_score - 2500

    # Reward for being close to food and away from ghosts.
    # The term 'minGhostDist * 3' encourages moving away from ghosts.
    heuristic_value = current_score + 150 / (minFoodDist + 1) + minGhostDist * 3

    return heuristic_value


# 5. GENERAL UTILITY FUNCTIONS (Reused from p4)

def manhattanDistance(pos1, pos2):
    """Calculate Manhattan distance between two positions"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def getValidMoves(layout, position, ghostPositions, currentGhost=None):
    """Return list of valid moves from current position"""
    row, col = position
    moves = []

    occupiedPositions = set()

    if currentGhost:
        # Ghosts are not allowed to step on other ghosts
        for ghost, pos in ghostPositions.items():
            if ghost != currentGhost:
                occupiedPositions.add(pos)
    else:
        # Pacman cannot move onto any ghost
        occupiedPositions = set(ghostPositions.values())

    # Check all four directions
    if layout[row - 1][col] != '%' and (row - 1, col) not in occupiedPositions:
        moves.append('N')
    if layout[row][col + 1] != '%' and (row, col + 1) not in occupiedPositions:
        moves.append('E')
    if layout[row + 1][col] != '%' and (row + 1, col) not in occupiedPositions:
        moves.append('S')
    if layout[row][col - 1] != '%' and (row, col - 1) not in occupiedPositions:
        moves.append('W')

    return moves


def applyMove(position, move):
    """Apply a move to a position and return new position"""
    row, col = position
    if move == 'N':
        return (row - 1, col)
    elif move == 'E':
        return (row, col + 1)
    elif move == 'S':
        return (row + 1, col)
    elif move == 'W':
        return (row, col - 1)
    return position


# 6. EXECUTION BLOCK

if __name__ == "__main__":
    # The image shows 'python p5.py 1 3 1 0', corresponding to:
    # test_case_id=1, k=3, num_trials=1, verbose=False

    # Read arguments
    test_case_id = int(sys.argv[1])
    problem_id = 5
    file_name_problem = str(test_case_id) + '.prob'
    file_name_sol = str(test_case_id) + '.sol'
    path = os.path.join('test_cases', 'p' + str(problem_id))

    # Load problem data
    problem = parse.read_layout_problem(os.path.join(path, file_name_problem))

    # Read k, num_trials, and verbose from command line
    k = int(sys.argv[2])
    num_trials = int(sys.argv[3])
    verbose = bool(int(sys.argv[4]))

    # Print header information
    print('test_case_id:', test_case_id)
    print('k:', k)
    print('num_trials:', num_trials)
    print('verbose:', verbose)

    # Run trials and track time/wins
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        # Use a deepcopy to ensure each trial starts from a fresh state
        solution, winner = min_max_multiple_ghosts(copy.deepcopy(problem), k)
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)

    win_p = win_count / num_trials * 100
    end = time.time()

    # Print results
    print('time: ', end - start)
    print('win %', win_p)