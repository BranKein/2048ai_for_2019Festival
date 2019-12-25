import puzzle

def main():
    School = "None"
    Name = "None"
    Score = 0
    ifWin = False

    School = input("Please enter your school name : ")
    Name = input("Please enter your name : ")
    print("Let's play 2048!")
    
    gamegrid = puzzle.puzzle()

    done = True

    while done:
        if(gamegrid.ifgameset()):
            Score = gamegrid.GetScore()
            ifWin = gamegrid.ifwintoai()
            Upload(School, Name, Score, ifWin)
            done = False


if __name__ == "__main__":
    main()

def Upload(School, Name, Score, ifWin):
    print("ChiHo will upload the datas")