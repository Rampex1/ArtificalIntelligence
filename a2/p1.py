import sys, random, grader, parse
from typing import List


def random_play_single_ghost(problem):
    random.seed(problem['seed'], version=1)

    # Constants
    EAT_FOOD_SCORE = 10
    PACMAN_EATEN_SCORE = -500
    PACMAN_WIN_SCORE = 500
    PACMAN_MOVING_SCORE = -1


    # Find initial positions
    pacmanPos = None
    ghostPos = None
    foodPositions = set()

    currentLayout = [list(row) for row in problem['layout']]
    for row in range(len(currentLayout)):
        for col in range(len(currentLayout[row])):
            if currentLayout[row][col] == 'P':
                pacmanPos = (row, col)
            elif currentLayout[row][col] == 'W':
                ghostPos = (row, col)
            elif currentLayout[row][col] == '.':
                foodPositions.add((row, col))

    # Output Info
    solution = f"seed: {problem['seed']}\n0\n"
    solution += '\n'.join(''.join(row) for row in currentLayout) + '\n'
    score = 0
    moveCount = 0

    while True:
        moveCount += 1

        # ---------------- PACMAN TURN ----------------
        pacmanMoves = getValidMoves(currentLayout, pacmanPos)
        if not pacmanMoves: break

        pacmanMove = random.choice(sorted(pacmanMoves))
        newPacmanPos = applyMove(pacmanPos, pacmanMove)

        # Clear old position
        currentLayout[pacmanPos[0]][pacmanPos[1]] = ' '

        # Eat food if present
        if newPacmanPos in foodPositions:
            score += EAT_FOOD_SCORE
            foodPositions.remove(newPacmanPos)

        # Moving cost
        score += PACMAN_MOVING_SCORE
        pacmanPos = newPacmanPos

        # Pacman runs into ghost
        if pacmanPos == ghostPos:
            score += PACMAN_EATEN_SCORE
            solution += f"{moveCount}: P moving {pacmanMove}\n"
            solution += '\n'.join(''.join(row) for row in currentLayout) + '\n'
            solution += f"score: {score}\nWIN: Ghost"
            return solution

        # Place Pacman in new position
        currentLayout[pacmanPos[0]][pacmanPos[1]] = 'P'
        solution += f"{moveCount}: P moving {pacmanMove}\n"
        solution += '\n'.join(''.join(row) for row in currentLayout) + '\n'

        # Winning condition
        if not foodPositions:
            score += PACMAN_WIN_SCORE
            solution += f"score: {score}\nWIN: Pacman"
            return solution

        # Score display
        solution += f"score: {score}\n"

        # ---------------- GHOST TURN ----------------
        moveCount += 1
        ghostMoves = getValidMoves(currentLayout, ghostPos)
        if not ghostMoves: continue

        ghostMove = random.choice(sorted(ghostMoves))
        newGhostPos = applyMove(ghostPos, ghostMove)

        # Restore food if ghost leaves a food square
        currentLayout[ghostPos[0]][ghostPos[1]] = ' ' if ghostPos not in foodPositions else '.'
        ghostPos = newGhostPos

        # Ghost catches Pacman
        if ghostPos == pacmanPos:
            score += PACMAN_EATEN_SCORE
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

def getValidMoves(layout, position) -> List[str]:
    """Return list of valid moves from current position"""
    row, col = position
    moves = []

    if layout[row - 1][col] != '%':  # North
        moves.append('N')
    if layout[row][col + 1] != '%':  # East
        moves.append('E')
    if layout[row + 1][col] != '%':  # South
        moves.append('S')
    if layout[row][col - 1] != '%':  # West
        moves.append('W')

    return moves

def applyMove(position, move) -> (int, int):
    """Apply a move to a position and return new position"""
    row, col = position
    if move == 'N':
        return row - 1, col
    elif move == 'E':
        return row, col + 1
    elif move == 'S':
        return row + 1, col
    elif move == 'W':
        return row, col - 1
    return position

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, random_play_single_ghost, parse.read_layout_problem)