import numpy as np
import pandas as pd
from game_config import CONFIG

class robot:
    def __init__(self, state, config):
        """
        state: current state of the game, a dictionary {"balls":0, "strikes":0}
        config: game configuration, a dictionary
        """
        self.config = config
        keys_to_check_state = ["balls", "strikes"]
        key_to_check_config = ["max_balls", "max_strikes", "ball_score", "strike_score", "home_run_score", "p_home_run"]
        if any(key not in config for key in key_to_check_config): # check if config has the required keys
            raise ValueError(f"Config must contain keys: {key_to_check_config}")
        else:
            self.max_balls = config["max_balls"]
            self.max_strikes = config["max_strikes"]
            self.ball_score = config["ball_score"]
            self.strike_score = config["strike_score"]
            self.home_run_score = config["home_run_score"]
            self.p_home_run = config["p_home_run"]
        
        if any(key not in state for key in keys_to_check_state): # check if state has the required keys
            raise ValueError(f"State must contain keys: {keys_to_check_state}")
        else:
            self.balls = state["balls"]
            self.strikes = state["strikes"]
        

class pitcher(robot):
    def __init__(self, state, config):
        """
        state: current state of the game, a dictionary {"balls":0, "strikes":0}
        config: game configuration, a dictionary
        """
        super().__init__(state, config)
        


class batter(robot):
    pass