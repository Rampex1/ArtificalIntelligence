import sys, parse
import time, os, copy
import random


def expecti_max_multiple_ghosts(problem, k):
    #Your p6 code here

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

    # Game loop
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

        bestMove = None
        bestValue = float('-inf')

        for move in pacmanMoves:
            newPacmanPos = applyMove(pacmanPos, move)
            newFoodPos = foodPositions.copy()
            if newPacmanPos in newFoodPos:
                newFoodPos.remove(newPacmanPos)

            # Check immediate loss
            if newPacmanPos in ghostPositions.values():
                continue

            # Evaluate this move using expectimax
            value = expectimaxValue(newPacmanPos, ghostPositions, newFoodPos,
                                    currentLayout, k - 1, False, 0, ghostOrder)

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

            ghostMove = random.choice(ghostMoves)
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


def expectimaxValue(pacmanPos, ghostPositions, foodPositions, layout, depth,
                    isPacmanTurn, ghostIndex, ghostOrder):
    """Recursively compute expectimax value"""
    # Terminal conditions
    if pacmanPos in ghostPositions.values():
        return -1000
    if not foodPositions:
        return 1000
    if depth == 0:
        return evaluateState(pacmanPos, ghostPositions, foodPositions)

    if isPacmanTurn:
        # Pacman maximizes
        maxValue = float('-inf')
        moves = getValidMovesSimple(layout, pacmanPos, ghostPositions)

        for move in moves:
            newPos = applyMove(pacmanPos, move)
            if newPos in ghostPositions.values():
                continue

            newFood = foodPositions.copy()
            if newPos in newFood:
                newFood.remove(newPos)

            value = expectimaxValue(newPos, ghostPositions, newFood, layout,
                                    depth, False, 0, ghostOrder)
            maxValue = max(maxValue, value)

        return maxValue if maxValue != float('-inf') else evaluateState(pacmanPos, ghostPositions, foodPositions)
    else:
        # Ghosts move randomly - compute expected value
        if ghostIndex >= len(ghostOrder):
            # All ghosts moved, back to Pacman
            return expectimaxValue(pacmanPos, ghostPositions, foodPositions, layout,
                                   depth - 1, True, 0, ghostOrder)

        ghostChar = ghostOrder[ghostIndex]
        ghostPos = ghostPositions[ghostChar]

        moves = getValidMovesSimple(layout, ghostPos, ghostPositions, ghostChar)

        if not moves:
            # Ghost stuck, skip to next ghost
            return expectimaxValue(pacmanPos, ghostPositions, foodPositions, layout,
                                   depth, False, ghostIndex + 1, ghostOrder)

        # Calculate expected value over all possible ghost moves
        totalValue = 0
        for move in moves:
            newGhostPos = applyMove(ghostPos, move)
            newGhostPositions = ghostPositions.copy()
            newGhostPositions[ghostChar] = newGhostPos

            value = expectimaxValue(pacmanPos, newGhostPositions, foodPositions, layout,
                                    depth, False, ghostIndex + 1, ghostOrder)
            totalValue += value

        return totalValue / len(moves)


def evaluateState(pacmanPos, ghostPositions, foodPositions):
    """Evaluate the quality of a game state"""
    if not foodPositions:
        return 1000

    minFoodDist = min(manhattanDistance(pacmanPos, food) for food in foodPositions)
    minGhostDist = min(manhattanDistance(pacmanPos, gPos) for gPos in ghostPositions.values())

    # Penalize proximity to ghosts
    ghostPenalty = 0
    if minGhostDist <= 1:
        ghostPenalty = -800
    elif minGhostDist <= 2:
        ghostPenalty = -300

    # Reward being close to food and far from ghosts
    foodReward = 100 / (minFoodDist + 1)
    ghostReward = minGhostDist * 5
    foodCountPenalty = len(foodPositions) * 10

    return foodReward + ghostReward - foodCountPenalty + ghostPenalty


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


def getValidMovesSimple(layout, position, ghostPositions, currentGhost=None):
    """Simplified move generation for expectimax"""
    return getValidMoves(layout, position, ghostPositions, currentGhost)


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
    problem_id = 6
    file_name_problem = str(test_case_id)+'.prob' 
    file_name_sol = str(test_case_id)+'.sol'
    path = os.path.join('test_cases','p'+str(problem_id)) 
    problem = parse.read_layout_problem(os.path.join(path,file_name_problem))
    k = int(sys.argv[2])
    num_trials = int(sys.argv[3])
    verbose = bool(int(sys.argv[4]))
    print('test_case_id:',test_case_id)
    print('k:',k)
    print('num_trials:',num_trials)
    print('verbose:',verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = expecti_max_multiple_ghosts(copy.deepcopy(problem), k)
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)