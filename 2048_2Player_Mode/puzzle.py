import random
from tkinter import Frame, Label, CENTER

import logic
import constants as c


class puzzle(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.score = 0
        self.order = 0

        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)

        # self.gamelogic = gamelogic
        self.commands = {c.KEY_UP: logic.up, c.KEY_DOWN: logic.down,
                         c.KEY_LEFT: logic.left, c.KEY_RIGHT: logic.right,
                         c.KEY_UP_ALT: logic.up, c.KEY_DOWN_ALT: logic.down,
                         c.KEY_LEFT_ALT: logic.left,
                         c.KEY_RIGHT_ALT: logic.right}
        self.commands_AI = {logic.up, logic.down,
                            logic.left, logic.right}

        self.grid_cells = [] # 0 : Player, 1 : AI
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()

        self.mainloop()

    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME,
                           width=900, height=500)
        background.grid()

        for k in range(2):
            grid_cells_one = []
            for i in range(1, 5):
                grid_row = []
                for j in range(c.GRID_LEN):
                    cell = Frame(background, bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                             width=c.SIZE / c.GRID_LEN,
                             height=c.SIZE / c.GRID_LEN)
                    cell.grid(row=i, column=j + k*5, padx=c.GRID_PADDING,
                          pady=c.GRID_PADDING)
                    t = Label(master=cell, text="",
                          bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                          justify=CENTER, font=c.FONT, width=5, height=2)
                    t.grid()
                    grid_row.append(t)

                grid_cells_one.append(grid_row)
            self.grid_cells.append(grid_cells_one)

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
            self.update_idletasks()

    def key_down(self, action):
        
        key = repr(event.char)

        matrix_temp = self.matrix[self.order % 2]
        
        matrix_temp, self.plusscore, done = self.commands[action](matrix_temp)
        self.score = self.score + self.plusscore
        if done:
            matrix_temp = logic.add_two(matrix_temp)
            self.matrix[self.order % 2] = matrix_temp
            # record last move
            self.update_grid_cells()
            done = False

        self.order = self.order + 1

    def generate_next(self):
        index = (self.gen(), self.gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (self.gen(), self.gen())
        self.matrix[index[0]][index[1]] = 2

    def Lose(self):
        if logic.game_state(self.matrix) == 'lose':
            self.grid_cells[1][4].configure(
                    text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
            self.grid_cells[2][4].configure(
                    text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
    def Win(self):
        if logic.game_state(self.matrix) == 'win':
            self.grid_cells[1][4].configure(
                    text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
            self.grid_cells[2][4].configure(
                    text="Win!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)

    def GetScore(self):
        return self.score


gamegrid = puzzle()
