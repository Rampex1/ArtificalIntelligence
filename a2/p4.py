import sys, parse
import time, os, copy
import random

def better_play_multiple_ghosts(problem):
    #Your p4 code here

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

        # Choose best move
        bestMove = None
        bestValue = float('-inf')

        for move in pacmanMoves:
            newPos = applyMove(pacmanPos, move)
            value = evaluatePosition(newPos, ghostPositions, foodPositions)
            if value > bestValue:
                bestValue = value
                bestMove = move

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
            if not ghostMoves: continue

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


def evaluatePosition(pacmanPos, ghostPositions, foodPositions):
    """
    Evaluate quality of a position for Pacman

    It first calculates the Manhattan distance from the Pacman to the closest food and ghost
    It then returns a value associated to the move. The higher, the better
    """

    if not foodPositions:
        return 1000

    minFoodDist = min(manhattanDistance(pacmanPos, food) for food in foodPositions)
    minGhostDist = min(manhattanDistance(pacmanPos, gPos) for gPos in ghostPositions.values())

    # Penalty for being near ghost
    if minGhostDist <= 1:
        return -1000
    elif minGhostDist <= 2:
        return -500

    return 150 / (minFoodDist + 1) + minGhostDist * 3


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
    problem_id = 4
    file_name_problem = str(test_case_id)+'.prob' 
    file_name_sol = str(test_case_id)+'.sol'
    path = os.path.join('test_cases','p'+str(problem_id)) 
    problem = parse.read_layout_problem(os.path.join(path,file_name_problem))
    num_trials = int(sys.argv[2])
    verbose = bool(int(sys.argv[3]))
    print('test_case_id:',test_case_id)
    print('num_trials:',num_trials)
    print('verbose:',verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = better_play_multiple_ghosts(copy.deepcopy(problem))
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)