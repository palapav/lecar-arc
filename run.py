
import argparse
from arc import ARC
from lecar import LeCaR

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ARC vs LeCaR Cache Evaluation')
    # parser.add_argument('algorithm', choices=['lecar', 'arc'], help='Caching algorithm (lecar or arc)')
    parser.add_argument('capacity', type=int, help='Cache capacity')
    parser.add_argument('trace_file', type=str, help='Trace file name')

    args = parser.parse_args()
    requests = 0
    lecar_hits, arc_hits = 0,0

    # cache_algorithm = None
    # if args.algorithm == "arc":
    #     cache_algoritm = ARC(args.capacity)
    # elif args.algorithm == "lecar":
    #     cache_algoritm = LeCaR(args.capacity)

arc_cache = ARC(args.capacity)
lecar_cache = LeCaR(args.capacity)
with open(args.trace_file, 'r') as f:
    for line in f:
        requests += 1

        # determine cache to use here once LeCaR built
        hit = lecar_cache.request(str(line))
        if hit: lecar_hits += 1

        hit = arc_cache.request(str(line))
        if hit: arc_hits += 1

    print(f'ARC Stats: {arc_hits} hits out of {requests} requests. ' +
            f'Hit-rate = {round(arc_hits / requests * 100, 2)}%')
    
    print(f'LeCaR Stats: {lecar_hits} hits out of {requests} requests. ' +
            f'Hit-rate = {round(lecar_hits / requests * 100, 2)}%')