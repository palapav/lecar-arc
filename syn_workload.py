"""Contains very large synthetic workload generation (no phase changes)"""
import random

NUM_REQUESTS_SET = [100000, 250000, 500000]

UNIVERSE_SET_SIZE = 200000
UNIVERSE_SET = list(range(1, UNIVERSE_SET_SIZE+1))
WORKING_SET_SIZE = int(0.25 * UNIVERSE_SET_SIZE) # arbitrarily determined


text_file_names = ["traces/syn_workload1.txt", "traces/syn_workload2.txt", "traces/syn_workload3.txt"]
for iter, NUM_REQUESTS in enumerate(NUM_REQUESTS_SET):
    workload = [] # ints
    unique_working_set = random.sample(UNIVERSE_SET, WORKING_SET_SIZE)
    for request_number in range(NUM_REQUESTS):
        selected_page = random.choice(unique_working_set)
        workload.append(selected_page)

    with open(text_file_names[iter], 'w') as file:
        for number in workload:
            file.write(str(number) + '\n')


