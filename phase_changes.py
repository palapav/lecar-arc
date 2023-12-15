"""Contains synthetic workload generation with and without phase changes"""

import random

def phase_changes_dataset():
    PHASE_SIZE = 5000
    NUM_PHASES = 5
    UNIVERSE_SET_SIZE = 2000
    WORKING_SET_SIZE = 30
    WS_SAME = 0.90
    random.seed(0)
    universe_set = list(range(1, UNIVERSE_SET_SIZE+1))
    working_set = list(range(1, WORKING_SET_SIZE+1))

    phase_changes_dataset = []

    for i in range(0, NUM_PHASES):

        working_set = random.sample(list(range(1, UNIVERSE_SET_SIZE+1)), WORKING_SET_SIZE)
                
        for _ in range(0, PHASE_SIZE):
        
            if random.random() < WS_SAME:
                page = random.choice(working_set)
            else:
                page = random.choice(universe_set)
            phase_changes_dataset.append(int(page))
    
    return phase_changes_dataset
    