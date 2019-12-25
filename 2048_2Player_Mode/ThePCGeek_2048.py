from PIL import ImageGrab, ImageOps
import pyautogui, time

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

print(pyautogui.displayMousePosition())


class Cords:
    cord11 = (310, 430)
    cord12 = (450, 430)
    cord13 = (590, 430)
    cord14 = (730, 430)
    cord21 = (310, 570)
    cord22 = (450, 570)
    cord23 = (590, 570)
    cord24 = (730, 570)
    cord31 = (310, 710)
    cord32 = (450, 710)
    cord33 = (590, 710)
    cord34 = (730, 710)
    cord41 = (310, 850)
    cord42 = (450, 850)
    cord43 = (590, 850)
    cord44 = (730, 850)

    cordArray = [cord11, cord12, cord13, cord14,
                 cord21, cord22, cord23, cord24,
                 cord31, cord32, cord33, cord34,
                 cord41, cord42, cord43, cord44]


class Values:
    empty = 193
    two = 228
    four = 224
    eight = 177
    sixteen = 149
    thirtyTwo = 124
    sixtyFour = 94
    oneTwentyEight = 205
    twoFiftySix = 201
    fiveOneTwo = 197
    oneZeroTwoFour = 193
    twoZeroFourEight = 189

    valueArray = [empty, two, four, eight, sixteen, thirtyTwo, sixtyFour
        , oneTwentyEight, twoFiftySix, fiveOneTwo, oneZeroTwoFour,
                  twoZeroFourEight]


def getGrid():
    image = ImageGrab.grab()
    grayImage = ImageOps.grayscale(image)

    for index, cord in enumerate(Cords.cordArray):
        pixel = grayImage.getpixel(cord)
        pos = Values.valueArray.index(pixel)
        if pos == 0:
            currentGrid[index] = 0
        else:
            currentGrid[index] = pow(2, pos)


def printGrid(grid):
    for i in range(16):
        if i % 4 == 0:
            print("[ " + str(grid[i]) + " " + str(grid[i + 1]) + " " + str(grid[i + 2]) + " " + str(grid[i + 3]) + " ]")


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

def getScore(grid):
    score =0
    for i in range(4):
        for j in range(4):
            score += grid[4*i+j]*scoreGrid[4*i+j]

    return score


def getBestMove(grid):
    scoreUp = getScore(getNextGrid(grid, UP))
    scoreDown = getScore(getNextGrid(grid, Down))
    scoreLeft = getScore(getNextGrid(grid, Left))
    scoreRight = getScore(getNextGrid(grid, Right))

    maxScore = max(scoreUp, scoreDown, scoreLeft, scoreRight)

    if scoreUP == maxScore:
        return UP
    elif scoreDown == maxScore:
        return DOWN
    elif scoreLeft == maxScore:
        return Left
    elif scoreRight == maxScore:
        return Right

def performMove(move):
    if move == UP:
        pyautogui.keyDown('up')
        time.sleep(0.05)
        pyautogui.keyUp('up')
    elif move == DOWN:
        pyautogui.keyDown('down')
        time.sleep(0.05)
        pyautogui.keyUp('down')
    elif move == LEFT:
        pyautogui.keyDown('left')
        time.sleep(0.05)
        pyautogui.keyUp('left')
    elif move == RIGHT:
        pyautogui.keyDown('right')
        time.sleep(0.05)
        pyautogui.keyUp('right')

def main():
    time.sleep(3)
    while True:
        getGrid()
        performMove(getBestMove(currentGrid))


        time.sleep(0.1)

