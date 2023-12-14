import unittest

from lecar import LeCaR

class TestARCCache(unittest.TestCase):
    def test_cache_operations(self):
        # Initialize your cache (replace ARCCacheClass with the actual name of your class)
        arc_cache = ARCCache(3)

        # Test initial state
        self.assertEqual(len(arc_cache), 0)

        # Test cache insertion
        arc_cache.request("key1")
        arc_cache.request("key2")
        arc_cache.request("key3")

        print(arc_cache)

        # Test cache size after insertions
        self.assertEqual(len(arc_cache), 3)

        # Test cache lookup
        self.assertTrue(arc_cache.request("key1"))
        self.assertTrue(arc_cache.request("key2"))
        print(arc_cache)
        self.assertTrue(arc_cache.request("key3"))
        self.assertFalse(arc_cache.request("key4"))
        print(arc_cache)

        # Test cache clear
        arc_cache.clear()
        self.assertEqual(len(arc_cache), 0)

if __name__ == '__main__':
    unittest.main()