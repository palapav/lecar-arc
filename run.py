
import argparse
from arccache import ARCCache

if __name__ == '__main__':# Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='ARC vs LeCaR Cache Evaluation')
    parser.add_argument('algorithm', choices=['lecar', 'arc'], help='Caching algorithm (lecar or arc)')
    parser.add_argument('capacity', type=int, help='Cache capacity')
    parser.add_argument('trace_file', type=str, help='Trace file name')

    args = parser.parse_args()
    requests, hits = 0, 0

    arc_cache = ARCCache(args.capacity)
    with open(args.trace_file, 'r') as f:
        for line in f:
            requests += 1

            # determine cache to use here once LeCaR built
            hit = arc_cache.request(line)

            if hit:
                hits += 1

        print(f'ARC Stats: {hits} hits out of {requests} requests. ' +
              f'Hit-rate = {round(hits / requests * 100, 2)}%')