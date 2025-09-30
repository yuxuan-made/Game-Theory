import numpy as np
import pandas as pd
import random
from player_ai import optimal_ai, simple_50_ai
from counterparty_ai import *

CONFIG = {
    "num_rooms": 10,
    "poisonous_room": 5,
    "antidote": 6,
    "Human_player": 0, # If True, the game will prompt user input for each move
    "AI_player_select": 0, # select AI model from AI_model_list, index starts from 0
    "AI_model_list": [optimal_ai, simple_50_ai], # Options: see file Game-Theory/poison_room_game/player_ai
    "Auto_replay": 500000, # If True, the game will auto-play for {Auto_replay} times
    "Counterparty": "random" # Options: random, rational. If not random, an AI counterparty will play against the player
}

class PoisonRoomGame:
    """A game where a player must navigate through a series of rooms, some of which are poisonous.
    The player has a limited number of antidotes to survive encounters with poisonous rooms."""
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
        # self.survive_times = 0

    def _reset(self) -> None:
        self.poisonous_room_remaining = self.poisonous_room
        self.rooms_remaining = self.num_rooms
        self.antidote_remaining = self.antidote
        self.rooms = [0] * (self.num_rooms - self.poisonous_room) + [1] * self.poisonous_room # 0 for safe, 1 for poisonous, create rooms
        random.shuffle(self.rooms) # Shuffle the rooms -> [0,0,0,0,1,1,1,1] -> [0,1,1,0,1,0,1,0]
        self.state = {
            "rooms_remaining": self.rooms_remaining,
            "poisonous_room_remaining": self.poisonous_room_remaining,
            "antidote_remaining": self.antidote_remaining,
            "game_result": 0 # 0 for ongoing, 1 for win, -1 for lose
        }
        return
    
    def _check_room(self, response: int) -> int:
        check = self.rooms.pop() # Remove the last room, check if it's poisonous, 0 for safe, 1 for poisonous
        self.rooms_remaining -= 1
        if response:
            self.antidote_remaining -= 1 # If antidote used, decrease the count of remaining antidotes
        if check:
            self.poisonous_room_remaining -= 1 # If poisonous, decrease the count of remaining poisonous rooms
        else: # only when safe room is found, check this condition would be meaningful
            if self.antidote_remaining < self.poisonous_room_remaining:
                return -1 # Not enough antidote, game over
        if check > response: # Poisonous room (1) encountered without antidote (0)
            return -1 # Poisoned, game over
        return self._check_win_condition() # Safe, continue game and check win condition
    
    def _check_win_condition(self) -> int:
        win_condition_1 = self.rooms_remaining <= self.antidote_remaining # All rooms can be checked safely
        win_condition_2 = self.poisonous_room_remaining == 0 # All poisonous rooms have been found
        if win_condition_1 or win_condition_2:
            return 1 # Win
        return 0 # Not win yet

    def _next_state(self, response: int) -> dict:

        result = self._check_room(response)
        new_state = {
            "rooms_remaining": self.rooms_remaining,
            "poisonous_room_remaining": self.poisonous_room_remaining,
            "antidote_remaining": self.antidote_remaining,
            "game_result": result
        }
        return new_state

    def human_play(self) -> None:
        self._reset()
        while True:
            check_poisonous_number = self.poisonous_room_remaining
            print(f"Rooms remaining: {self.rooms_remaining}, Poisonous rooms remaining: {self.poisonous_room_remaining}, Antidote remaining: {self.antidote_remaining}")
            response = int(input("Enter your response (0 for no antidote, 1 for antidote): "))
            if response not in [0, 1]:
                print("Invalid response. Please enter 0 or 1.")
                continue
            self.state = self._next_state(response) # Get the next state based on the player's response
            if self.state["poisonous_room_remaining"] < check_poisonous_number:
                print("You found a poisonous room!")
            else:
                print("You found a safe room!")
            if self.state["game_result"] == 1:
                print("Congratulations! You have successfully navigated through the rooms.")
                break
            if self.state["game_result"] == -1:
                print("Game over! You have been poisoned.")
                break
            print("Continue exploring...")
        replay = input("Do you want to play again? (y/n): ")
        if replay.lower() in ['y', 'yes']:
            self.human_play()
    
    def bot_play(self) -> None:
        ai_model = self.config["AI_model_list"][self.config["AI_player_select"]] # Select AI model based on config
        print(f"AI model selected: {ai_model.__name__}")
        ai_model = ai_model.bot
        self.survive_times = 0
        for _ in range(self.config["Auto_replay"]):
            self._reset()
            while True:
                response = ai_model(**self.state) # Get the AI's response based on the current state
                self.state = self._next_state(response) # Get the next state based on the AI's response
                if self.state["game_result"] == 1:
                    self.survive_times += 1
                    break
                if self.state["game_result"] == -1:
                    break
                else:
                    continue
        print(f"Total games: {self.config['Auto_replay']}, Survived: {self.survive_times}, Survival rate: {self.survive_times/self.config['Auto_replay']:.4f}")
    
    def play(self) -> None:
        if self.config["Human_player"]:
            self.human_play()
        else:
            self.bot_play()



if __name__ == "__main__":
    game = PoisonRoomGame(CONFIG)
    game.play()