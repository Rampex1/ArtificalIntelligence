import sys, random, grader, parse

def random_play_single_ghost(problem):
    random.seed(problem['seed'], version=1)

    # Score constants
    eatFoodScore = 10
    pacmanEatenScore = -500
    pacmanWinScore = 500
    pacmanMovingScore = -1

    # Copy layout for manipulation
    currentLayout = [list(row) for row in problem['layout']]

    # Find initial positions
    pacmanPos = None
    ghostPos = None
    foodPositions = set()

    for row in range(len(currentLayout)):
        for col in range(len(currentLayout[row])):
            if currentLayout[row][col] == 'P':
                pacmanPos = (row, col)
            elif currentLayout[row][col] == 'W':
                ghostPos = (row, col)
            elif currentLayout[row][col] == '.':
                foodPositions.add((row, col))

    # Build output string
    solution = f"seed: {problem['seed']}\n0\n"
    solution += '\n'.join(''.join(row) for row in currentLayout) + '\n'

    score = 0
    moveCount = 0

    # Game loop
    while True:
        moveCount += 1

        # ---------------- PACMAN TURN ----------------
        pacmanMoves = getValidMoves(currentLayout, pacmanPos)
        if not pacmanMoves:
            break

        pacmanMove = random.choice(sorted(pacmanMoves))
        newPacmanPos = applyMove(pacmanPos, pacmanMove)

        # Clear old position
        currentLayout[pacmanPos[0]][pacmanPos[1]] = ' '

        # Eat food if present
        if newPacmanPos in foodPositions:
            score += eatFoodScore
            foodPositions.remove(newPacmanPos)

        # Moving cost
        score += pacmanMovingScore
        pacmanPos = newPacmanPos

        # Pacman runs into ghost
        if pacmanPos == ghostPos:
            score += pacmanEatenScore
            solution += f"{moveCount}: P moving {pacmanMove}\n"
            solution += '\n'.join(''.join(row) for row in currentLayout) + '\n'
            solution += f"score: {score}\nWIN: Ghost"
            return solution

        # Place Pacman in new position
        currentLayout[pacmanPos[0]][pacmanPos[1]] = 'P'

        solution += f"{moveCount}: P moving {pacmanMove}\n"
        solution += '\n'.join(''.join(row) for row in currentLayout) + '\n'

        # ✅ Check win condition BEFORE printing score
        if not foodPositions:
            score += pacmanWinScore
            solution += f"score: {score}\nWIN: Pacman"
            return solution

        # Otherwise, print intermediate score
        solution += f"score: {score}\n"

        # ---------------- GHOST TURN ----------------
        moveCount += 1
        ghostMoves = getValidMoves(currentLayout, ghostPos)
        if not ghostMoves:
            continue

        ghostMove = random.choice(sorted(ghostMoves))
        newGhostPos = applyMove(ghostPos, ghostMove)

        # Restore food if ghost leaves a food square
        currentLayout[ghostPos[0]][ghostPos[1]] = ' ' if ghostPos not in foodPositions else '.'
        ghostPos = newGhostPos

        # Ghost catches Pacman
        if ghostPos == pacmanPos:
            score += pacmanEatenScore
            solution += f"{moveCount}: W moving {ghostMove}\n"
            currentLayout[ghostPos[0]][ghostPos[1]] = 'W'
            solution += '\n'.join(''.join(row) for row in currentLayout) + '\n'
            solution += f"score: {score}\nWIN: Ghost"
            return solution

        # Place ghost in new position
        currentLayout[ghostPos[0]][ghostPos[1]] = 'W'

        solution += f"{moveCount}: W moving {ghostMove}\n"
        solution += '\n'.join(''.join(row) for row in currentLayout) + '\n'
        solution += f"score: {score}\n"


def getValidMoves(layout, position):
    """Return list of valid moves from current position"""
    row, col = position
    moves = []

    # Check all four directions
    if layout[row - 1][col] != '%':  # North
        moves.append('N')
    if layout[row][col + 1] != '%':  # East
        moves.append('E')
    if layout[row + 1][col] != '%':  # South
        moves.append('S')
    if layout[row][col - 1] != '%':  # West
        moves.append('W')

    return moves
    return solution

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
    problem_id = 1
    grader.grade(problem_id, test_case_id, random_play_single_ghost, parse.read_layout_problem)