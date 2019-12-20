import Environment as env
import Environment_logic as logic
import Agent # Model-Free Agent
import numpy as np 
import random
import matplotlib.pyplot as plt
import csv
import Agent_constants as ac

def PlayGame():
    TheGamePlayer = env.puzzle("Player")
    TheGameAI = env.puzzle("AI")
    TheGamePlayer.ifCanAct = True

    TheAIAgent = Agent.Agent(ac.STATECOUNT, ac.ACTIONS)

    while True:
        if TheGamePlayer.lose:
            print("player lose")
        elif TheGameAI.lose:
            print("AI lose")
        else:


# =======================================================================
def main():
    #
    # Main Method Just Play our Experiment
    Result_Data = PlayGame()
        
        # =======================================================================
if __name__ == "__main__":
    main()
