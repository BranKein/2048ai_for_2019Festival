import time

currentGrid = [0, 0, 0, 0,
               0, 0, 0, 0,
               0, 0, 0, 0,
               0, 0, 0, 0]

UP = 100
LEFT = 101
DOWN = 102
RIGHT = 103

scoreGrid = [50, 30, 15, 5,
               30, -10, 0, 0,
               15, 0, 0, 0,
               5, 0, 0, 0]



def swipeRow(row):
    prev = -1
    i = 0
    temp = [0, 0, 0, 0]

    for element in row:

        if element != 0:
            if prev == -1:
                prev = element
                temp[i] = element
                i += 1
            elif prev == element:
                temp[i - 1] = 2 * prev
                prev = -1
            else:
                prev = element
                temp[i] = element
                i += 1

    return temp

def getNextGrid(grid, move):

    temp = [0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0]

    if move == UP:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[i + 4*j])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[i + 4*j] = val

    elif move == LEFT:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[4*i + j])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[4*i + j] = val

    elif move == DOWN:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[i + 4 * (3-j)])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[i + 4 * (3-j)] = val

    elif move == RIGHT:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[4 * i + (3-j)])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[4 * i + (3-j)] = val

    return temp

def getScore(grid, ori):
    score =0
    same = True

    for i in range(16):
        if grid[i] != ori[i]:
            same = False

    if same:
        return -100

    for i in range(4):
        for j in range(4):
            score += grid[4*i+j]*scoreGrid[4*i+j]

    return score


def getBestMove(grid):
    scoreUp = getScore(getNextGrid(grid, UP), grid)
    scoreDown = getScore(getNextGrid(grid, DOWN), grid)
    scoreLeft = getScore(getNextGrid(grid, LEFT), grid)
    scoreRight = getScore(getNextGrid(grid, RIGHT), grid)

    maxScore = max(scoreUp, scoreDown, scoreLeft, scoreRight)

    if scoreUp == maxScore:
        return 0
    elif scoreDown == maxScore:
        return 1
    elif scoreLeft == maxScore:
        return 2
    else:
        return 3


