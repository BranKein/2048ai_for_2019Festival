import random
from tkinter import *
import time
import numpy as np

import logic
import constants as c
import ThePCGeek_2048


class puzzle():
    def __init__(self):

        #self.AI = Agent.Agent(16, 4)

        self.RootFrame = Tk()

        self.score = 0
        self.AIscore = 0
        self.order = 0

        self.GameSet = False
        self.Win = False

        self.RootFrame.title("2048 AI vs Human")

        self.RootFrame.geometry("1400x500+100+100")
        self.RootFrame.resizable(True, True)

        self.frame1forhuman = Frame(self.RootFrame, relief = "solid", bd = 2)
        self.frame1forhuman.pack(side="left", fill="both", expand=True)

        self.frame2forAI = Frame(self.RootFrame, relief = "solid", bd = 2)
        self.frame2forAI.pack(side="right", fill="both", expand=True)
        self.frames = [self.frame1forhuman, self.frame2forAI]
        self.RootFrame.bind("<Key>", self.key_down)

        # self.gamelogic = gamelogic
        self.commands = {c.KEY_UP: logic.up, c.KEY_DOWN: logic.down,
                         c.KEY_LEFT: logic.left, c.KEY_RIGHT: logic.right,
                         c.KEY_UP_ALT: logic.up, c.KEY_DOWN_ALT: logic.down,
                         c.KEY_LEFT_ALT: logic.left,
                         c.KEY_RIGHT_ALT: logic.right}
        self.commands_AI = {logic.up, logic.down,
                            logic.left, logic.right}

        self.grid_cells = [] # 0 : Player, 1 : AI
        self.grid_cell_score = []
        self.init_grid()
        self.init_grid_score()
        self.init_matrix()
        self.update_grid_cells()

        self.RootFrame.mainloop()

    def init_grid(self):
        #background = Frame(self, bg=c.BACKGROUND_COLOR_GAME,width=200, height=125)
        #background.grid()

        for k in range(2):
            grid_cells_one = []
            for i in range(4):
                grid_row = []
                for j in range(4):
                    cell = Frame(self.frames[k], bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                             width=10,
                             height=10)
                    cell.grid(row=i+1, column=j, padx=5,
                          pady=5)
                    t = Label(master=cell, text="",
                          bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                          justify=CENTER, font=c.FONT, width=3, height=1)
                    t.grid()
                    grid_row.append(t)

                grid_cells_one.append(grid_row)
            self.grid_cells.append(grid_cells_one)

    def init_grid_score(self):
        cell_human_title = Frame(self.frames[0], bg = c.BACKGROUND_COLOR_CELL_EMPTY, width =10, height=10)
        cell_human_title.grid(row=5, column=0, padx=5,pady=5)
        t_human_title = Label(master=cell_human_title, text="Score",bg=c.BACKGROUND_COLOR_CELL_EMPTY,justify=CENTER, font=(c.FONT, 20), width=7, height=2)
        t_human_title.grid()
        cell_human_num = Frame(self.frames[0], bg = c.BACKGROUND_COLOR_CELL_EMPTY, width =10, height=10)
        cell_human_num.grid(row=5, column=1, padx=5,pady=5)
        t_human_num = Label(master=cell_human_num, text="",bg=c.BACKGROUND_COLOR_CELL_EMPTY,justify=CENTER, font=(c.FONT, 15), width=3, height=1)
        t_human_num.grid()
        cell_human_name = Frame(self.frames[0], bg = c.BACKGROUND_COLOR_CELL_EMPTY, width =10, height=10)
        cell_human_name.grid(row=5, column=3, padx=5,pady=5)
        t_human_name = Label(master=cell_human_name, text="You",bg=c.BACKGROUND_COLOR_CELL_EMPTY,justify=CENTER, font=(c.FONT, 15), width=3, height=1)
        t_human_name.grid()

        cell_ai_title = Frame(self.frames[1], bg = c.BACKGROUND_COLOR_CELL_EMPTY, width =10, height=10)
        cell_ai_title.grid(row=5, column=0, padx=5,pady=5)
        t_ai_title = Label(master=cell_ai_title, text="Score",bg=c.BACKGROUND_COLOR_CELL_EMPTY,justify=CENTER, font=(c.FONT, 20), width=7, height=2)
        t_ai_title.grid()
        cell_ai_num = Frame(self.frames[1], bg = c.BACKGROUND_COLOR_CELL_EMPTY, width =10, height=10)
        cell_ai_num.grid(row=5, column=1, padx=5,pady=5)
        t_ai_num = Label(master=cell_ai_num, text="",bg=c.BACKGROUND_COLOR_CELL_EMPTY,justify=CENTER, font=(c.FONT, 15), width=3, height=1)
        t_ai_num.grid()
        cell_ai_name = Frame(self.frames[1], bg = c.BACKGROUND_COLOR_CELL_EMPTY, width =10, height=10)
        cell_ai_name.grid(row=5, column=3, padx=5,pady=5)
        t_ai_name = Label(master=cell_ai_name, text="AI",bg=c.BACKGROUND_COLOR_CELL_EMPTY,justify=CENTER, font=(c.FONT, 15), width=3, height=1)
        t_ai_name.grid()

        self.grid_cell_score.append(t_human_num)
        self.grid_cell_score.append(t_ai_num)

    def gen(self):
        return random.randint(0, c.GRID_LEN - 1)

    def init_matrix(self):
        matrix_p = logic.new_game(4)
        matrix_c = logic.new_game(4)
        self.matrix = [matrix_p, matrix_c]
        for i in range(2):
            for j in range(2):
                self.matrix[i] = logic.add_two(self.matrix[i])

    def update_grid_cells(self):  # 0 : player, 1 : AI
        for k in range(2):

            for i in range(c.GRID_LEN):
                for j in range(c.GRID_LEN):
                    new_number = self.matrix[k][i][j]
                    if new_number == 0:
                        self.grid_cells[k][i][j].configure(
                        text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    else:
                        self.grid_cells[k][i][j].configure(text=str(
                        new_number), bg=c.BACKGROUND_COLOR_DICT[new_number],
                        fg=c.CELL_COLOR_DICT[new_number])
            self.RootFrame.update_idletasks()

        self.update_grid_cell_number()

    def update_grid_cell_number(self):
        self.grid_cell_score[0].configure(text=str(self.score),bg=c.BACKGROUND_COLOR_DICT[2],
                        fg=c.CELL_COLOR_DICT[2])
        self.grid_cell_score[1].configure(text=str(self.AIscore), bg=c.BACKGROUND_COLOR_DICT[2],
                        fg=c.CELL_COLOR_DICT[2])

    def key_down(self, event):

        matrix_temp = self.matrix[0]
        done = False

        moved = False

        if(event.char == 'w' and self.checkifcanmove(logic.up(matrix_temp)[0], matrix_temp)):
            matrix_temp, self.plusscore, done = logic.up(matrix_temp)
            self.score = self.score + self.plusscore
            moved = True
        elif(event.char == 'a' and self.checkifcanmove(logic.left(matrix_temp)[0], matrix_temp)):
            matrix_temp, self.plusscore, done = logic.left(matrix_temp)
            self.score = self.score + self.plusscore
            moved = True
        elif(event.char == 'd' and self.checkifcanmove(logic.right(matrix_temp)[0], matrix_temp)):
            matrix_temp, self.plusscore, done = logic.right(matrix_temp)
            self.score = self.score + self.plusscore
            moved = True
        elif(event.char == 's' and self.checkifcanmove(logic.down(matrix_temp)[0], matrix_temp)):
            matrix_temp, self.plusscore, done = logic.down(matrix_temp)
            self.score = self.score + self.plusscore
            moved = True

        if(logic.game_state(self.matrix[0]) == 'lose'):
            self.GameSet = True

        if(logic.game_state(self.matrix[0]) == 'not over' and logic.game_state(self.matrix[1]) == 'lose'):
            self.Win = True
            
        
        if (logic.game_state(self.matrix[0]) == 'not over') and done and moved:
            print("done")
            print(matrix_temp)
            matrix_temp = logic.add_two(matrix_temp)
            self.matrix[0] = matrix_temp
            # record last move
            self.update_grid_cells()

            self.order = self.order + 1
            
            if not self.Win:
                self.AIAction(0.2)

            done = False


        if self.GameSet and not self.Win:
            self.Finish()

        if self.GameSet and self.Win:
            self.RootFrame.quit()

    def checkifcanmove(self, grid, ori):
        grid = np.array(grid)
        ori = np.array(ori)

        grid = grid.flatten()
        ori = ori.flatten()

        same = True

        for i in range(16):
            if(grid[i] != ori[i]):
                same = False

        return not same

        

    def Finish(self):
        while True:
            if logic.game_state(self.matrix[1]) == 'not over':
                
                self.AIAction(0)
            else:
                print("It is my Best!")
                return
        

    def AIAction(self, delay):
        GameState = np.array(self.matrix[1])
        print("Thinking...")
        time.sleep(delay)

        BestAction = ThePCGeek_2048.getBestMove(GameState.flatten())

        print("AI Choose" + str(BestAction))

        if(BestAction == 0):
            matrix_temp, self.plusscore, done = logic.up(GameState)
            self.AIscore = self.AIscore + self.plusscore
        elif(BestAction == 1):
            matrix_temp, self.plusscore, done = logic.down(GameState)
            self.AIscore = self.AIscore + self.plusscore
        elif(BestAction == 2):
            matrix_temp, self.plusscore, done = logic.left(GameState)
            self.AIscore = self.AIscore + self.plusscore
        elif(BestAction == 3):
            matrix_temp, self.plusscore, done = logic.right(GameState)
            self.AIscore = self.AIscore + self.plusscore

        matrix_temp = logic.add_two(matrix_temp)
        self.matrix[1] = matrix_temp
        self.update_grid_cells()

        #print("AI")
        self.order = self.order + 1

    def generate_next(self):
        index = (self.gen(), self.gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (self.gen(), self.gen())
        self.matrix[index[0]][index[1]] = 2


    def GetScore(self):
        return self.score

    def ifgameset(self):
        if logic.game_state(self.matrix[0]) == 'lose':
            return True
        else:
            return False

    def ifwintoai(self):
        if logic.game_state(self.matrix[1]) == 'lose':
            return True
        else:
            return False
