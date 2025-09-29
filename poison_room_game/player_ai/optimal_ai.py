import numpy as np
import pandas as pd
import random

def bot(rooms_remaining, poisonous_room_remaining, antidote_remaining):
    ai = dynamic_programming_bot(rooms_remaining, poisonous_room_remaining, antidote_remaining)
    return ai.decision()

class dynamic_programming_bot:
    def __init__(self, rooms_remaining, poisonous_room_remaining, antidote_remaining):
        self.rooms_remaining = rooms_remaining
        self.poisonous_room_remaining = poisonous_room_remaining
        self.antidote_remaining = antidote_remaining
    
    def prob(self, rooms_remaining, poisonous_room_remaining, antidote_remaining) -> float:
        """ Return the probability of survival from the current state """
        # Base termination conditions
        if rooms_remaining <= antidote_remaining:
            return 1  # Survive, score 1
        if poisonous_room_remaining == 0:
            return 1  # Survive, score 1
        if poisonous_room_remaining > antidote_remaining:
            return 0  # Dead, score 0

        prob_tuple = self._prob_calculation(rooms_remaining, poisonous_room_remaining, antidote_remaining)

        return max(prob_tuple)

    # Calculate probabilities for each action
    # extract to a separate function to avoid redundant calculations
    def _prob_calculation(self, rooms_remaining, poisonous_room_remaining, antidote_remaining) -> tuple:
        prob_poison = poisonous_room_remaining / rooms_remaining # Calculate probability of encountering a poisonous room

        use_antidote = ((1 - prob_poison) * self.prob(rooms_remaining - 1, poisonous_room_remaining, antidote_remaining - 1) # enter safe room, next state
                        + prob_poison * self.prob(rooms_remaining - 1, poisonous_room_remaining - 1, antidote_remaining - 1)) # enter poisonous room, next state
        no_antidote = (1 - prob_poison) * self.prob(rooms_remaining - 1, poisonous_room_remaining, antidote_remaining) # enter safe room, next state
        return (use_antidote, no_antidote)

    def decision(self):
        use_antidote, no_antidote = self._prob_calculation(self.rooms_remaining, self.poisonous_room_remaining, self.antidote_remaining)
        return 1 if use_antidote > no_antidote else 0
    
if __name__ == "__main__":
    # Example usage
    rooms_remaining = 8
    poisonous_room_remaining = 4
    antidote_remaining = 5
    ai = dynamic_programming_bot(rooms_remaining, poisonous_room_remaining, antidote_remaining)
    survive_probability = ai.prob(rooms_remaining, poisonous_room_remaining, antidote_remaining)
    decision = ai.decision()
    print(f"AI decision (0 for no antidote, 1 for antidote): {decision}, with survival probability: {survive_probability:.4f}")