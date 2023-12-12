from flexlru import LRUCache

class ARCCache:
    def __init__(self, capacity):
        self.p = 0
        self.capacity = capacity
        self.T1 = LRUCache()
        self.T2 = LRUCache()
        self.B1 = LRUCache()
        self.B2 = LRUCache()

    def __contains__(self, x):
        return x in self.T1 or x in self.T2 or x in self.B1 or x in self.B2

    def __len__(self):
        """
        Return the number of bindings in the cache.
        """
        return len(self.T1) + len(self.T2) + len(self.B1) + len(self.B2)

    def __str__(self):
        return f'T1: {self.T1}, T2: {self.T2}, B1: {self.B1}, B2: {self.B2}'

    def _replace(self, x):
        """
        REPLACE subroutine for taking a page from T and moving it to B.
        """
        if (len(self.T1) > 0 and (len(self.T1) > self.p)) or (
        x in self.B2 and len(self.T1) == self.p):
            self.T1.deleteLRU()
            self.B1.moveToMRU(x)
        else:
            self.T2.deleteLRU()
            self.B2.moveToMRU(x)

    def _topCacheHit(self, x):
        """Move x to the MRU position of T2."""
        if x in self.T1:
            self.T1.delete(x)
        else:
            self.T2.delete(x)
        self.T2.moveToMRU(x)

    def _ghostHitOne(self, x):
        """Move x to the MRU position of T2. Increase size of T1."""
        d1 = 1 if len(self.B1) > len(self.B2) else (len(self.B2) / len(self.B1))
        self.p = min(self.p + d1, self.capacity)
        self._replace(x)

        self.B1.delete(x)
        self.T2.moveToMRU(x)

    def _ghostHitTwo(self, x):
        """Move x to the MRU position of T2. Increase size of T2."""
        d2 = 1 if len(self.B2) > len(self.B1) else (len(self.B1) / len(self.B2))
        self.p = max(self.p - d2, 0)
        self._replace(x)

        self.B2.delete(x)
        self.T2.moveToMRU(x)

    def _cacheMiss(self, x):
        """Move x to the MRU position of T1. Evict from either B1, B2, or neither."""
        # Case A: L1 has exactly c pages.
        if len(self.T1) + len(self.B1) == self.capacity:
            if len(self.T1) < self.capacity:
                self.B1.deleteLRU()
                self._replace(x)
            else:
                self.T1.deleteLRU()
        # Case B: L1 has less than c pages.
        elif len(self.T1) + len(self.B1) < self.capacity:
            if len(self) >= self.capacity:
                if len(self) == 2 * self.capacity:
                    self.B2.deleteLRU()
                self._replace(x)
        self.T1.moveToMRU(x)

    def request(self, x):
        """Request x from ARC. Returns True if cache hit, and False otherwise."""
        hit = False
        if x in self.T1 or x in self.T2: # Cache hit
            self._topCacheHit(x)
            hit = True
        elif x in self.B1:               # Ghost cache 1 hit
            self._ghostHitOne(x)
        elif x in self.B2:               # Ghost cache 2 hit
            self._ghostHitTwo(x)
        elif x not in self:              # Total cache miss
            self._cacheMiss(x)
        return hit

    def clear(self):
        """Clear all items from the cache."""
        self.T1.clear()
        self.T2.clear()
        self.B1.clear()
        self.B2.clear()
