import csv
from arccache import ARCCache

# Function to process a trace file and generate CSV data
def process_trace(trace_file, output_csv):
    # Cache sizes to iterate over
    cache_sizes = [1024, 4096, 16384, 131072, 262144, 524288]

    # Initialize the CSV data
    csv_data = []

    # Read the trace file and process with different cache sizes
    for c in cache_sizes:
        arc_cache = ARCCache(c)
        requests = 0
        hits = 0

        # Open and process each line in the trace file
        with open(trace_file, 'r') as f:
            for line in f:
                requests += 1

                hit = arc_cache.request(line)

                if hit:
                    hits += 1

        # Calculate hit ratio
        hit_ratio = round(hits / requests * 100, 2)

        # Append data to the CSV
        csv_data.append({
            'Cache Size': c,
            'Requests': requests,
            'Hits': hits,
            'Hit Ratio': hit_ratio
        })

    # Write results to the CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['Cache Size', 'Requests', 'Hits', 'Hit Ratio']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for data in csv_data:
            writer.writerow(data)

azure_trace_file_path = "azure_trace.txt"
azure_output_csv_path = "azure_trace_eval.csv"
process_trace(azure_trace_file_path, azure_output_csv_path)