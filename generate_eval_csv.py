import csv
import os
from arc import ARC
from lecar import LeCaR

def process_trace(trace_file, output_csv):
    """
    Process a trace file and generate CSV data about cache hit ratio.
    """
    cache_sizes = [64, 128, 256, 512, 1024, 4096]
    csv_data = []

    # Read the trace file and process with different cache sizes
    print("Another trace!")
    for c in cache_sizes:
        print(f"cache: {c}")
        arc_cache = ARC(c)
        lecar_cache = LeCaR(c)

        hits_arc, hits_lecar = 0, 0
        requests = 0

        # Open and process each line in the trace file
        with open(trace_file, 'r') as f:
            for line in f:
                requests += 1

                hit_arc = arc_cache.request(line)
                if hit_arc:
                    hits_arc += 1

                hit_lecar = lecar_cache.request(line)
                if hit_lecar:
                    hits_lecar += 1

        hit_ratio_arc = round(hits_arc / requests * 100, 2)
        hit_ratio_lecar = round(hits_lecar / requests * 100, 2)

        # Append data to CSV file for each cache
        csv_data.append({
            'Trace': trace_file.split('/')[1],
            'Cache Type': 'ARC',
            'Cache Size': c,
            'Requests': requests,
            'Hits': hits_arc,
            'Hit Ratio': hit_ratio_arc
        })
        csv_data.append({
            'Trace': trace_file.split('/')[1],
            'Cache Type': 'LeCaR',
            'Cache Size': c,
            'Requests': requests,
            'Hits': hits_lecar,
            'Hit Ratio': hit_ratio_lecar
        })

    # Write results to the CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['Trace', 'Cache Type', 'Cache Size', 'Requests', 'Hits', 'Hit Ratio']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for data in csv_data:
            writer.writerow(data)

# Directory containing trace files
traces_directory = "traces"

# Output CSV file
output_csv_path = "simulation_eval.csv"

# Iterate through trace files
for trace_file in os.listdir(traces_directory):
    if trace_file.endswith(".txt"):
        trace_file_path = os.path.join(traces_directory, trace_file)
process_trace(trace_file_path, output_csv_path)