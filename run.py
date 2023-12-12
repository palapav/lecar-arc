
import sys
from arccache import ARCCache

if __name__ == '__main__':
    c = int(sys.argv[1])
    requests_file = sys.argv[2]
    requests, hits = 0, 0

    arc_cache = ARCCache(c)
    with open(requests_file, 'r') as f:
        for line in f:
            requests += 1

            hit = arc_cache.request(int(line))

            if hit:
                hits += 1

        print("ARC Stats: %d hits out of %d requests. Hit-rate = %.2f%".format() %
                (hits, requests, round(hits / requests * 100, 2)))