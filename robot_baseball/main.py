import numpy as np
import pandas as pd
from game_config import CONFIG
# from robot import pitcher, batter

# Idea: use dynamic programming to solve the game
# 1. create the solver to solve game theory reaction of the very ending case
# 2. use the solver to solve the previous state, until the initial state
# 3. return the optimal strategy and probability of hitting full count

class solver:
    def __init__(self, state, config):
        """
        input:
        state: current state of the game, a dictionary {"balls":0, "strikes":0}
        config: game configuration, a dictionary
        """
        self.state = state
        self.config = config

    def nash_equilibrium(self, payoff_matrix):
        """
        input:
        payoff_matrix: a 2D numpy array, where each element is a float (score)
        first dimension is for batter (swing or wait), second dimension is for pitcher (strike or ball)
        [[1.2, 0], 
        [0, 1]] means if batter swings and pitcher balls, score is 1.2, etc.
        [[strike & swing, ball & swing],
        [strike & wait , ball & wait]]
        
        return: 
        optimal frequency (probability) for pitcher strike and batter swing, each is a float
        """
        # Method:
        # First check if the game has a pure strategy Nash equilibrium
        # Then Using the formula for 2x2 matrix Nash equilibrium
        # p = (d - b) / (a - b - c + d)
        # q = (d - c) / (a - b - c + d)
        # In this case, if the batter always swings, the pitcher will always throw a ball, and vice versa,
        # that simplifies the game if there is a pure strategy Nash equilibrium
        # Then if there is no pure strategy Nash equilibrium, and the denominator is 0, then the game is a tie, and we can return any strategy
        a, b, c, d = payoff_matrix[0,0], payoff_matrix[0,1], payoff_matrix[1,0], payoff_matrix[1,1]
        
        # pure strategy Nash equilibrium check
        if a > c and b > d: # batter always swing, then picher always ball
            p_swing = 1.0
            p_strike = 0.0
            return p_strike, p_swing
        elif a < c and b < d: # batter always wait, then pitcher always strike
            p_swing = 0.0
            p_strike = 1.0
            return p_strike, p_swing

        # mixed strategy Nash equilibrium
        denominator = a - b - c + d
        if denominator == 0:
            p_swing = 0.5
            p_strike = 0.5
            return p_strike, p_swing
        else:
            p_swing = (d - c) / denominator
            p_strike = (d - b) / denominator
            return p_strike , p_swing

    def solve(self, state):
        """
        state: current state of the game, a dictionary {"balls":0, "strikes":0}
        return: optimal strategy and probability of hitting full count
        """
        # base case: if the game is over, return the score
        p_full_count = 0
        if state["balls"] == self.config["max_balls"]-1 and state["strikes"] == self.config["max_strikes"]-1:
            p_full_count = 1
        if state["balls"] >= self.config["max_balls"]:
            return self.config["ball_score"], p_full_count
        if state["strikes"] >= self.config["max_strikes"]:
            return self.config["strike_score"], p_full_count
        
        
        # recursive case: calculate the expected score for each action
        # pitcher can throw a ball or a strike
        # batter can swing or not swing
        # calculate the expected score for each combination of actions
        # return the optimal strategy and probability of hitting full count

        # Placeholder for actual implementation
        optimal_strategy = {"pitcher": "ball", "batter": "swing"}
        prob_full_count = 0.5

        return optimal_strategy, prob_full_count
