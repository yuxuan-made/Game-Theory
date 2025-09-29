import numpy as np
import pandas as pd
import random
from player_ai import optimal_ai
from counterparty_ai import *

CONFIG = {
    "num_rooms": 8,
    "poisonous_room": 4,
    "antidote": 5,
    "Human_player": False, # If True, the game will prompt user input for each move
    "AI_player_select": 1, # If select other than 0, AI will play the game
    "AI_model_list": [None, optimal_ai], # Options: see file Game-Theory/poison_room_game/player_ai
    "probability_test": True, # If True, the game will run a probability test for the AI model selected
    "Auto_replay": 1000000, # If True, the game will auto-play for {Auto_replay} times
    "Counterparty": "random" # Options: random, rational. If not random, an AI counterparty will play against the player
}

class PoisonRoomGame:
    def __init__(self, config):
        self.config = config
        self.num_rooms = config["num_rooms"]
        self.rooms_remaining = self.num_rooms
        self.poisonous_room = config["poisonous_room"]
        self.poisonous_room_remaining = self.poisonous_room
        self.antidote = config["antidote"]
        self.antidote_remaining = self.antidote
        self.rooms = [0] * self.num_rooms # Initialize all rooms as safe (0)
        if not (0 <= self.poisonous_room <= self.antidote <= self.num_rooms):
            raise ValueError("Room / Poisonous room / Antidote index out of bounds")
        self._reset()
        self.survive_times = 0

    def _reset(self) -> None:
        self.poisonous_room_remaining = self.poisonous_room
        self.rooms_remaining = self.num_rooms
        self.antidote_remaining = self.antidote
        self.rooms = [0] * (self.num_rooms - self.poisonous_room) + [1] * self.poisonous_room # 0 for safe, 1 for poisonous, create rooms
        random.shuffle(self.rooms) # Shuffle the rooms -> [0,0,0,0,1,1,1,1] -> [0,1,1,0,1,0,1,0]
        return
    
    def _check_room(self, response: int) -> int:
        check = self.rooms.pop() # Remove the last room, check if it's poisonous, 0 for safe, 1 for poisonous
        self.rooms_remaining -= 1
        if check:
            print("One poisonous room encountered!")
            self.poisonous_room_remaining -= 1 # If poisonous, decrease the count of remaining poisonous rooms
        else:
            print("Safe room encountered!")
            if self.antidote_remaining < self.poisonous_room_remaining:
                print("Not enough antidote to survive remaining poisonous rooms!")
                return -1 # Not enough antidote, game over
        if check > response:
            return -1 # Poisoned, game over
        return 0 # Safe, continue game
    
    def _check_win_condition(self) -> bool:
        win_condition_1 = self.rooms_remaining <= self.antidote_remaining # All rooms can be checked safely
        win_condition_2 = self.poisonous_room_remaining == 0 # All poisonous rooms have been found
        return win_condition_1 or win_condition_2

    def _next_state(self, response: int) -> dict:

        result = self._check_room(response)
        new_state = {
            "rooms_remaining": self.rooms_remaining,
            "poisonous_room_remaining": self.poisonous_room_remaining,
            "antidote_remaining": self.antidote_remaining
        }
        return new_state

    def play(self) -> None:

        self._reset()
        while True:
            print(f"Rooms remaining: {self.rooms_remaining}, Poisonous rooms remaining: {self.poisonous_room_remaining}, Antidote remaining: {self.antidote_remaining}")
            ai_model = self.config["AI_model_list"][self.config["AI_player_select"]] # Select AI model based on config
            if ai_model is None: # Human player
                response = int(input("Enter your response (0 for no antidote, 1 for antidote): "))
            else:
                response = ai_model.bot(self.rooms_remaining, self.poisonous_room_remaining, self.antidote) # AI player, the main function would always called "bot"
                print(f"AI chooses response: {response}")
            if response not in [0, 1]:
                print("Invalid response. Please enter 0 or 1.")
                continue
            if response == 1:
                self.antidote_remaining -= 1
            result = self._check_room(response) # Check the selected room
            if result == -1: # If poisoned, _check_room would return -1, else return 0
                print("Game over! You were poisoned.")
                break
            if self._check_win_condition(): # If not dead yet, check win condition
                print("Congratulations! You win the game.")
                self.survive_times += 1
                break
            print("Continue exploring...")
        # return survive_times
        # self._reset()
    
    def replay(self) -> None:
        if self.config["probability_test"]:
            total_games = self.config["Auto_replay"]
            for _ in range(total_games):
                self.play()
            print(f"Total games: {total_games}, Survived: {self.survive_times}, Survival rate: {self.survive_times/total_games:.4f}")
        else:
            self.play()
        ask = input("Do you want to play again? (y/n)")
        if ask.lower() == ('y' or 'yes'):
            self.play()
    
    def human_play(self) -> None:
        self.config["Human_player"] = True
        self.play()
        
    


if __name__ == "__main__":
    game = PoisonRoomGame(CONFIG)
    # game.play()
    game.replay()