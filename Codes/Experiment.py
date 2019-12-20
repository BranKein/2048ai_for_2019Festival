
#
#  MyPong DQN Reinforcement Learning Experiment
#
#  Plays Pong Game (DQN control of Left Hand Yellow Paddle)
#  Objective is simply measured as succesfully returning of the Ball 
#  The programed oponent player is a pretty hot player. Imagine success as being able to return ball served from Serena Williams)
#  Moving Average Score from [-10, +10] from Complete failure to return the balls, to full success in returning the Ball.
#
#  This Reinforcement learning employs Direct Features [ Paddle Y, Ball X, Y and Ball X,Y Directions feeding into DQN Nueral net Estimator of Q[S,A] function.
#  So this is NOT a Convolutional Network based RL, based Game Video Frame states [Which in my experience takes much too Long to Learn on standard PCs] 
#  So unfortunaly this is Game Specific DQN Reinforecment Learning, and cannot be generalised to other games. Requires specific Features to be identified. 
#      
# This experiment demonstrates DQN based agent, improves from poor performace ~ 5.0 towards reasonably good +8.0 (Fluctuating) 
# return rate in around 15,000 game cycles [Not returns]
#
#  The  code is based upon Siraj Raval's inspiring vidoes on Machine learning and Reinforcement Learning [ Which is full convolutional DQN example] 
#  https://github.com/llSourcell/pong_neural_network_live
# 
#  requires pygame, numpy, matplotlib, keras [and hence Tensorflow or Theono backend] 
# ==========================================================================================
import Environment as env
import Environment_logic as logic
import Agent # Model-Free Agent
import numpy as np 
import random
import matplotlib.pyplot as plt
import csv
import Agent_constants as ac


#agent observeperiod - 횟수가 아니라 판수 기준으로 바꿔야?
# 죄다 횟수가 아니라 판수 기준으로?

# =====================================================================

# =====================================================================
# Main Experiment Method

def PlayExperiment():
        GameHistory = []
        
        # Create our PongGame instance
        TheGame = env.puzzle()

        #  Create our Agent (including DQN based Brain)
        TheAgent = Agent.Agent(ac.STATECOUNT, ac.ACTIONS)
        #TheAgent.Load(119400)

        gametime = 0 #총 턴수
        episodes = 0 # 현재까지 판수
        reward = 0

    # =================================================================
        #Main Experiment Loop
        while (episodes<ac.TOTAL_EPISODES):
                # First just Update the Game Display
                episodes = TheGame.episodes
                GameState = np.array(TheGame.GameState)
                GameState = GameState.flatten()

                BestAction = TheAgent.Act(GameState) # 현재 상태로 행동을 선택

                # 선택한 행동으로 한 타입스텝 진행
                TheGame.update_state(BestAction)
                NextState = np.array(TheGame.GameState)
                NextState = GameState.flatten()
                reward = ac.LOSE_REWARD if TheGame.lose else TheGame.plusscore_power

                # Capture the Sample [S, A, R, S"] in Agent Experience Replay Memory 
                TheAgent.CaptureSample((GameState, BestAction, reward, NextState))
                TheAgent.Process()
                '''
                에이전트는 매 타임스템마다 경험한 것을 샘플로 메모리에 저장
                '''

                #  Now Request Agent to DQN Train process  Against Experience

                #Environment.py 호출해서 다음 state로 넘어가도록 해야 함
                #혹은             GameState = NextState  // 안됨
                #print(type(BestAction))
                #print(BestAction)


                # Move gametime Click
                gametime += 1
                if TheGame.lose:
                        GameHistory.append((episodes, TheGame.episodeScore))
                        item_length = len(GameHistory)
                        with open('test.csv', 'w') as test_file:
                                file_writer = csv.writer(test_file, lineterminator='\n')
                                for i in range(item_length):
                                        file_writer.writerow([GameHistory[i][0], GameHistory[i][1]])

        #print our where wer are after saving where we are



                if episodes % 100 == 0 and TheGame.lose:
                        #s = len([x for x in TheGame.recentScores if x > 0])
                        print("{0}번째 시행, {1}판째, 현재 게임 최고 {2}점, epsilon {3}".format(gametime, episodes, TheGame.episodeScore, TheAgent.epsilon))
                        TheAgent.Save(episodes)

                        #print("Game Time: ", gametime," Total Game Score: ", "{0} : {1}".format(TheGame.Display_Score1, TheGame.Display_Score2)," Winning Rate: ","{0} : {1}".format(s, MyPong.RECENT_SCORE-s) )
                        #RECENT_SCORE = 100 (승률 합)


                     #score 매 판 초기화되도록
                     #그래프 그리기, 기록, tensorboard

        # ===============================================
        # End of Game Loop  so Plot the Score vs Game Time profile

        
        #TheAgent.Save()
        
        x_val = [x[0] for x in GameHistory]
        y_val = [x[1] for x in GameHistory]

        plt.plot(x_val,y_val)
        plt.xlabel("Episodes")
        plt.ylabel("Score")
        plt.show()
        
        
        
        # =======================================================================
def main():
    #
        # Main Method Just Play our Experiment
        PlayExperiment()
        
        # =======================================================================
if __name__ == "__main__":
    main()
