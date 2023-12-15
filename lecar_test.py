import sys
import unittest
import random
from lecar import LeCaR

"""
Sanity check testing of LeCaR cache algorithm.
More advanced testing can be found in the evals folder
"""

class TestLeCaRCache(unittest.TestCase):
    def test_cache_operations(self):
        lecar_cache = LeCaR(3)

        # Test initial state
        self.assertEqual(len(lecar_cache.lru), 0)
        self.assertEqual(len(lecar_cache.lfu), 0)

        # Test cache insertion
        lecar_cache.request("key1")
        lecar_cache.request("key2")
        lecar_cache.request("key3")

        # Test cache size after insertions
        self.assertEqual(len(lecar_cache.lfu), 3)

        # Test cache lookup
        self.assertTrue(lecar_cache.request("key1"))
        self.assertTrue(lecar_cache.request("key2"))
        self.assertTrue(lecar_cache.request("key3"))
        self.assertFalse(lecar_cache.request("key4"))

        lecar_cache = LeCaR(cache_size=4)
        NUM_REQUESTS = 1000
        cache_hits = 0
        for i in range(NUM_REQUESTS):
            rand_number = random.randint(0,10)
            found = lecar_cache.request(rand_number)
            if found: cache_hits +=1
        print(f"Cache hit ratio: {cache_hits/NUM_REQUESTS}")

if __name__ == '__main__':
    unittest.main()