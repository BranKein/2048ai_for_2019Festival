
import random

import Environment_logic as logic
import Environment_constants as c

class puzzle():
    def __init__(self):

        self.score = 0 # 이번 판 누적 점수
        self.score_power = 0
        self.episodeScore = 0
        self.episodes = 1 # 누적 판수
        self.commands_AI = [logic.up, logic.down,
                            logic.left, logic.right] #keyboard 입력을 Agent의 Act로 대체
        self.GameState = logic.new_game(4)
        self.grid_cells = []
        self.init_matrix()

    def init_matrix(self):
        self.matrix = logic.new_game(4) # matrix: 게임 타일의 현재 배치 상태
        self.history_matrixs = list()
        self.matrix = logic.add_two(self.matrix)
        self.matrix = logic.add_two(self.matrix)
        self.GameState = self.matrix

    def update_state(self, event):
        self.lose = False

        self.matrix, self.plusscore, self.plusscore_power, self.done = self.commands_AI[event](self.matrix)
        self.score = self.score + self.plusscore
        self.score_power = self.score_power + self.plusscore_power
        if self.done:
            self.matrix = logic.add_two(self.matrix)
            self.history_matrixs.append(self.matrix)
            self.GameState = self.matrix
            self.done = False
            if logic.checking_game_over(self.matrix) == 'lose': # reset and starting new game
                self.lose = True
                self.new_episode()

    def new_episode(self):
        self.episodes += 1
        self.episodeScore = self.score
        self.score = 0
        self.plusscore_power = 0
        self.init_matrix()