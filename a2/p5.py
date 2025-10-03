import sys, parse
import time, os, copy

def min_max_multiple_ghosts(problem, k):
    # Score constants
    EAT_FOOD_SCORE = 10
    PACMAN_EATEN_SCORE = -500
    PACMAN_WIN_SCORE = 500
    PACMAN_MOVING_SCORE = -1

    # Find initial positions
    pacmanPos = None
    ghostPositions = {}
    foodPositions = set()

    currentLayout = [list(row) for row in problem['layout']]
    for row in range(len(currentLayout)):
        for col in range(len(currentLayout[row])):
            cell = currentLayout[row][col]
            if cell == 'P':
                pacmanPos = (row, col)
            elif cell in ['W', 'X', 'Y', 'Z']:
                ghostPositions[cell] = (row, col)
            elif cell == '.':
                foodPositions.add((row, col))

    solution = f"seed: {problem['seed']}\n0\n"
    solution += '\n'.join(''.join(row) for row in currentLayout) + '\n'

    score = 0
    moveCount = 0
    ghostOrder = sorted(ghostPositions.keys())

    while True:
        moveCount += 1

        # ---------------- PACMAN TURN ----------------
        pacmanMoves = getValidMoves(currentLayout, pacmanPos, ghostPositions)
        if not pacmanMoves:
            score += PACMAN_EATEN_SCORE
            solution += f"{moveCount}: Pacman has no moves (trapped)\n"
            solution += '\n'.join(''.join(row) for row in currentLayout) + '\n'
            solution += f"score: {score}\nWIN: Ghost"
            return solution, 'Ghost'

        # Run minimax to find best move
        bestMove = None
        bestValue = float('-inf')

        for i, move in enumerate(pacmanMoves):
            newPacmanPos = applyMove(pacmanPos, move)

            # Skip moves into ghosts
            if newPacmanPos in ghostPositions.values():
                continue

            newFoodPos = foodPositions.copy()
            if newPacmanPos in newFoodPos:
                newFoodPos.remove(newPacmanPos)

            # Evaluate using minimax
            value = minimaxValue(newPacmanPos, ghostPositions, newFoodPos,
                                 currentLayout, k, False, 0, ghostOrder, 0)

            if value > bestValue:
                bestValue = value
                bestMove = move

        if bestMove is None:
            bestMove = pacmanMoves[0]

        pacmanMove = bestMove
        newPacmanPos = applyMove(pacmanPos, pacmanMove)

        currentLayout[pacmanPos[0]][pacmanPos[1]] = ' '

        if newPacmanPos in foodPositions:
            score += EAT_FOOD_SCORE
            foodPositions.remove(newPacmanPos)

        score += PACMAN_MOVING_SCORE
        pacmanPos = newPacmanPos

        if pacmanPos in ghostPositions.values():
            score += PACMAN_EATEN_SCORE
            solution += f"{moveCount}: P moving {pacmanMove}\n"
            solution += '\n'.join(''.join(row) for row in currentLayout) + '\n'
            solution += f"score: {score}\nWIN: Ghost"
            return solution, 'Ghost'

        currentLayout[pacmanPos[0]][pacmanPos[1]] = 'P'

        solution += f"{moveCount}: P moving {pacmanMove}\n"
        solution += '\n'.join(''.join(row) for row in currentLayout) + '\n'
        solution += f"score: {score}\n"

        if not foodPositions:
            score += PACMAN_WIN_SCORE
            solution += f"score: {score}\nWIN: Pacman"
            return solution, 'Pacman'

        # ---------------- GHOSTS TURN ----------------
        for ghostChar in ghostOrder:
            moveCount += 1
            ghostPos = ghostPositions[ghostChar]

            ghostMoves = getValidMoves(currentLayout, ghostPos, ghostPositions, ghostChar)
            if not ghostMoves:
                continue

            # Use minimax to find best ghost move
            bestGhostMove = None
            bestGhostValue = float('inf')

            for move in ghostMoves:
                newGhostPos = applyMove(ghostPos, move)

                # Check for immediate capture
                if newGhostPos == pacmanPos:
                    # This is a winning move for ghosts
                    bestGhostMove = move
                    break

                newGhostPositions = ghostPositions.copy()
                newGhostPositions[ghostChar] = newGhostPos

                # Find the index of the next ghost to move
                currentGhostIndex = ghostOrder.index(ghostChar)
                nextGhostIndex = currentGhostIndex + 1

                # Evaluate using minimax
                value = minimaxValue(pacmanPos, newGhostPositions, foodPositions,
                                     currentLayout, k, False,
                                     nextGhostIndex, ghostOrder)

                if value < bestGhostValue:
                    bestGhostValue = value
                    bestGhostMove = move

            if bestGhostMove is None:
                bestGhostMove = ghostMoves[0]

            ghostMove = bestGhostMove
            newGhostPos = applyMove(ghostPos, ghostMove)

            currentLayout[ghostPos[0]][ghostPos[1]] = ' ' if ghostPos not in foodPositions else '.'
            ghostPositions[ghostChar] = newGhostPos
            ghostPos = newGhostPos

            if ghostPos == pacmanPos:
                score += PACMAN_EATEN_SCORE
                solution += f"{moveCount}: {ghostChar} moving {ghostMove}\n"
                currentLayout[ghostPos[0]][ghostPos[1]] = ghostChar
                solution += '\n'.join(''.join(row) for row in currentLayout) + '\n'
                solution += f"score: {score}\nWIN: Ghost"
                return solution, 'Ghost'

            currentLayout[ghostPos[0]][ghostPos[1]] = ghostChar

            solution += f"{moveCount}: {ghostChar} moving {ghostMove}\n"
            solution += '\n'.join(''.join(row) for row in currentLayout) + '\n'
            solution += f"score: {score}\n"


def minimaxValue(pacmanPos, ghostPositions, foodPositions, layout, depth,
                 isPacmanTurn, ghostIndex, ghostOrder, callDepth=0):
    # Terminal conditions
    if pacmanPos in ghostPositions.values():
        return -1000
    if not foodPositions:
        return 1000
    if depth == 0:
        result = evaluateState(pacmanPos, ghostPositions, foodPositions, layout)
        return result

    # Pacman's turn (maximize)
    if isPacmanTurn:
        maxValue = float('-inf')
        moves = getValidMoves(layout, pacmanPos, ghostPositions)

        if not moves:
            return -1000

        for move in moves:
            newPos = applyMove(pacmanPos, move)

            if newPos in ghostPositions.values():
                continue

            newFood = foodPositions.copy()
            if newPos in newFood:
                newFood.remove(newPos)

            # After Pacman moves, first ghost moves
            value = minimaxValue(newPos, ghostPositions, newFood, layout,
                                 depth, False, 0, ghostOrder, callDepth + 1)
            maxValue = max(maxValue, value)

        return maxValue if maxValue != float('-inf') else -1000

    # Ghosts' turn (minimize)
    else:
        if ghostIndex >= len(ghostOrder):
            # All ghosts have moved, NOW decrease depth and return to Pacman
            if depth <= 1:
                # No more depth to search after this round
                return evaluateState(pacmanPos, ghostPositions, foodPositions, layout)
            else:
                # Continue to next round
                return minimaxValue(pacmanPos, ghostPositions, foodPositions, layout,
                                    depth - 1, True, 0, ghostOrder, callDepth + 1)

        ghostChar = ghostOrder[ghostIndex]
        ghostPos = ghostPositions[ghostChar]
        minValue = float('inf')

        moves = getValidMoves(layout, ghostPos, ghostPositions, ghostChar)

        if not moves:
            return minimaxValue(pacmanPos, ghostPositions, foodPositions, layout,
                                depth, False, ghostIndex + 1, ghostOrder, callDepth + 1)

        for move in moves:
            newGhostPos = applyMove(ghostPos, move)
            newGhostPositions = ghostPositions.copy()
            newGhostPositions[ghostChar] = newGhostPos

            if newGhostPos == pacmanPos:
                value = -1000
            else:
                value = minimaxValue(pacmanPos, newGhostPositions, foodPositions, layout,
                                     depth, False, ghostIndex + 1, ghostOrder, callDepth + 1)

            minValue = min(minValue, value)

        return minValue if minValue != float('inf') else 0


def evaluateState(pacmanPos, ghostPositions, foodPositions, layout):
    if not foodPositions:
        return 1000  # Pacman wins

    minFoodDist = min(manhattanDistance(pacmanPos, food) for food in foodPositions)
    minGhostDist = min(manhattanDistance(pacmanPos, gPos) for gPos in ghostPositions.values())

    # Food attraction (positive for being close to food)
    food_score = 100.0 / (minFoodDist + 1)

    # Ghost danger
    if minGhostDist == 0:
        ghost_score = -1000
    elif minGhostDist == 1:
        ghost_score = -500   #
    elif minGhostDist == 2:
        ghost_score = -200
    else:
        ghost_score = -50 / minGhostDist

    food_count_penalty = -len(foodPositions) * 10

    result = food_score + ghost_score + food_count_penalty
    return result


def manhattanDistance(pos1, pos2):
    """Calculate Manhattan distance between two positions"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def getValidMoves(layout, position, ghostPositions, currentGhost=None):
    """Return list of valid moves from current position"""
    row, col = position
    moves = []

    occupiedPositions = set()
    if currentGhost:
        for ghost, pos in ghostPositions.items():
            if ghost != currentGhost:
                occupiedPositions.add(pos)
    else:
        occupiedPositions = set(ghostPositions.values())

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


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 5
    file_name_problem = str(test_case_id) + '.prob'
    file_name_sol = str(test_case_id) + '.sol'
    path = os.path.join('test_cases', 'p' + str(problem_id))
    problem = parse.read_layout_problem(os.path.join(path, file_name_problem))
    k = int(sys.argv[2])
    num_trials = int(sys.argv[3])
    verbose = bool(int(sys.argv[4]))
    print('test_case_id:', test_case_id)
    print('k:', k)
    print('num_trials:', num_trials)
    print('verbose:', verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = min_max_multiple_ghosts(copy.deepcopy(problem), k)
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count / num_trials * 100
    end = time.time()
    print('time: ', end - start)
    print('win %', win_p)