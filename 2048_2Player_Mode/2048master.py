# This is for the little study about learning of 2048 game in AI
# Producer Kim Yeon Hyuk, Jung Ji Min
# Belong to Incheon Jinsan Science High School Computing club "JS++"
# Pre-code we use is "2048-python" made by yangshun
# Github: https://github.com/yangshun/2048-python
# Edited: scoring system for the learing attribute
#         auto-key_down system for auto playing AI
# This Code will import the original code "puzzle" for management of game

# This Code Edit Started 2019.6.21
#           Edit Ended   2019.

import tensorflow as tf
import puzzle
import matplotlib as mtb



gamegrid = puzzle.GameGrid()

