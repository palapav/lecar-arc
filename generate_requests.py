import random

def generate_requests(file_path, num_requests, max_value):
    with open(file_path, 'w') as file:
        for _ in range(num_requests):
            request = random.randint(1, max_value)
            file.write(f"{request}\n")

# Specify the file path, number of requests, and maximum value for requests
file_path = 'requests.txt'
num_requests = 1000000
max_value = 200000

# Generate requests and write them to the file
generate_requests(file_path, num_requests, max_value)
