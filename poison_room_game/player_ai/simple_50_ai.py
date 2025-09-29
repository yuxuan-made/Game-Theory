import numpy as np
import pandas as pd
import random

def bot(rooms_remaining, poisonous_room_remaining, antidote_remaining):
    if rooms_remaining <= antidote_remaining:
        return 0  # No need to use antidote, all remaining rooms can be checked safely
    elif poisonous_room_remaining == 0:
        return 0  # No poisonous rooms left, safe to check without antidote
    elif poisonous_room_remaining >= antidote_remaining:
        return 1  # High risk, use antidote
    else:
        # Calculate probability of encountering a poisonous room
        prob_poison = poisonous_room_remaining / rooms_remaining
        if prob_poison > 0.5:
            return 1  # More than 50% chance of poison, use antidote
        else:
            return 0  # Less than 50% chance, take the risk