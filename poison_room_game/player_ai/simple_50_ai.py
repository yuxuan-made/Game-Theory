import numpy as np
import pandas as pd
import random

def bot(rooms_remaining, poisonous_room_remaining, antidote_remaining, **kwargs):

    # Calculate probability of encountering a poisonous room
    prob_poison = poisonous_room_remaining / rooms_remaining
    if prob_poison > 0.5:
        return 1  # More than 50% chance of poison, use antidote
    elif prob_poison == 0.5:
        return random.choice([0, 1])  # Exactly 50% chance, random choice
    else:
        return 0  # Less than 50% chance, take the risk