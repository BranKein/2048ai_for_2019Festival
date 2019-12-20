
import random
from tkinter import Frame, Label, CENTER
import Environment_logic as logic
import Environment_constants as c

class puzzle(Frame):
    def __init__(self, name):
        Frame.__init__(self)

        self.grid()
        self.master.title('2048{}'.format(name))
        self.master.bind("<Key>", self.key_down)

        self.ifCanAct = False

        self.score = 0 # 이번 판 누적 점수
        self.score_power = 0
        self.episodeScore = 0
        self.episodes = 1 # 누적 판수

        self.commands = {c.KEY_UP: logic.up, c.KEY_DOWN: logic.down,
                         c.KEY_LEFT: logic.left, c.KEY_RIGHT: logic.right,
                         c.KEY_UP_ALT: logic.up, c.KEY_DOWN_ALT: logic.down,
                         c.KEY_LEFT_ALT: logic.left,
                         c.KEY_RIGHT_ALT: logic.right}
        self.commands_AI = [logic.up, logic.down,
                            logic.left, logic.right] #keyboard 입력을 Agent의 Act로 대체

        self.grid_cells = []
        self.init_grid()
        self.init_matrix()

    def init_matrix(self):
        self.matrix = logic.new_game(4) # matrix: 게임 타일의 현재 배치 상태
        self.history_matrixs = list()
        self.matrix = logic.add_two(self.matrix)
        self.matrix = logic.add_two(self.matrix)
        self.GameState = self.matrix

    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME,
                           width=c.SIZE, height=c.SIZE)
        background.grid()

        for i in range(c.GRID_LEN):
            grid_row = []
            for j in range(c.GRID_LEN):
                cell = Frame(background, bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                             width=c.SIZE / c.GRID_LEN,
                             height=c.SIZE / c.GRID_LEN)
                cell.grid(row=i, column=j, padx=c.GRID_PADDING,
                          pady=c.GRID_PADDING)
                t = Label(master=cell, text="",
                          bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                          justify=CENTER, font=c.FONT, width=5, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def update_state(self, event):  #For Player
        self.lose = False

        self.matrix, self.plusscore, self.plusscore_power, self.done = self.commands_AI[event](self.matrix)
        self.score = self.score + self.plusscore

        if self.done:
            self.matrix = logic.add_two(self.matrix)
            self.GameState = self.matrix
            self.update_grid_cells()
            self.done = False
            if logic.checking_game_over(self.matrix) == 'lose': # reset and starting new game
                self.grid_cells[1][1].configure(
                    text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                self.grid_cells[1][2].configure(
                    text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                self.lose = True


    def key_down(self, action):  #For AI
        key = repr(event.char)
        self.matrix, self.plusscore, self.plusscore_power, self.done = self.commands[action](self.matrix)
        self.score = self.score + self.plusscore

        if done:
            self.matrix = logic.add_two(self.matrix)
            self.GameState = self.matrix
            self.update_grid_cells()
            self.done = False

            if logic.game_state(self.matrix) == 'lose':
                self.grid_cells[1][1].configure(
                    text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                self.grid_cells[1][2].configure(
                    text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                self.lose = True

    def update_grid_cells(self):
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(
                        text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), 
                        bg=c.BACKGROUND_COLOR_DICT[new_number],
                        fg=c.CELL_COLOR_DICT[new_number])
        self.update_idletasks()

    def new_episode(self):
        self.episodes += 1
        self.episodeScore = self.score
        self.score = 0
        self.plusscore_power = 0
        self.init_matrix()