import sys, grader, parse, math
import random

def random_play_multiple_ghosts(problem):
    random.seed(problem['seed'], version=1)

    # Score constants
    eatFoodScore = 10
    pacmanEatenScore = -500
    pacmanWinScore = 500
    pacmanMovingScore = -1

    currentLayout = [list(row) for row in problem['layout']]

    # Find initial positions
    pacmanPos = None
    ghostPositions = {}  # Maps ghost character to position
    foodPositions = set()

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
            break

        pacmanMove = random.choice(sorted(pacmanMoves))
        newPacmanPos = applyMove(pacmanPos, pacmanMove)

        # Clear old Pacman cell
        currentLayout[pacmanPos[0]][pacmanPos[1]] = ' '

        # Eat food if present
        if newPacmanPos in foodPositions:
            score += eatFoodScore
            foodPositions.remove(newPacmanPos)

        score += pacmanMovingScore
        pacmanPos = newPacmanPos

        # ✅ Check collision BEFORE drawing Pacman
        if pacmanPos in ghostPositions.values():
            score += pacmanEatenScore
            solution += f"{moveCount}: P moving {pacmanMove}\n"
            solution += '\n'.join(''.join(row) for row in currentLayout) + '\n'
            solution += f"score: {score}\nWIN: Ghost"
            return solution

        # Now safe to draw Pacman
        currentLayout[pacmanPos[0]][pacmanPos[1]] = 'P'

        solution += f"{moveCount}: P moving {pacmanMove}\n"
        solution += '\n'.join(''.join(row) for row in currentLayout) + '\n'

        # ✅ Apply win bonus before printing score
        if not foodPositions:
            score += pacmanWinScore
            solution += f"score: {score}\nWIN: Pacman"
            return solution

        solution += f"score: {score}\n"

        # ---------------- GHOSTS TURN ----------------
        for ghostChar in ghostOrder:
            moveCount += 1
            ghostPos = ghostPositions[ghostChar]

            ghostMoves = getValidMoves(currentLayout, ghostPos, ghostPositions, ghostChar)
            if not ghostMoves:
                solution += f"{moveCount}: {ghostChar} moving \n"
                solution += '\n'.join(''.join(row) for row in currentLayout) + '\n'
                solution += f"score: {score}\n"
                continue

            ghostMove = random.choice(sorted(ghostMoves))
            newGhostPos = applyMove(ghostPos, ghostMove)

            # Restore food if ghost leaves a food square
            currentLayout[ghostPos[0]][ghostPos[1]] = ' ' if ghostPos not in foodPositions else '.'

            ghostPositions[ghostChar] = newGhostPos
            ghostPos = newGhostPos

            # Ghost catches Pacman
            if ghostPos == pacmanPos:
                score += pacmanEatenScore
                solution += f"{moveCount}: {ghostChar} moving {ghostMove}\n"
                currentLayout[ghostPos[0]][ghostPos[1]] = ghostChar
                solution += '\n'.join(''.join(row) for row in currentLayout) + '\n'
                solution += f"score: {score}\nWIN: Ghost"
                return solution

            currentLayout[ghostPos[0]][ghostPos[1]] = ghostChar

            solution += f"{moveCount}: {ghostChar} moving {ghostMove}\n"
            solution += '\n'.join(''.join(row) for row in currentLayout) + '\n'
            solution += f"score: {score}\n"

    # Safety fallback
    solution += f"score: {score}\nWIN: Ghost"
    return solution


def getValidMoves(layout, position, ghostPositions, currentGhost=None):
    """Return list of valid moves from current position"""
    row, col = position
    moves = []

    occupiedPositions = set()
    if currentGhost:
        # For ghosts, don’t allow stepping on *other* ghosts
        for ghost, pos in ghostPositions.items():
            if ghost != currentGhost:
                occupiedPositions.add(pos)
    else:
        # For Pacman, DO NOT block ghost positions
        occupiedPositions = set()

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
    problem_id = 3
    grader.grade(problem_id, test_case_id, random_play_multiple_ghosts, parse.read_layout_problem)
