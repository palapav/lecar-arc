class Node:
    """
    Internal node class to be used for LRU cache in ARC implementation.
    Note that the key/value pair is redundant given the current cache
    usage.

    In the event key/value pairs were to be stored in the cache,
    this Node can then make use of both."""
    def __init__(self, key, val, prev=None, nextt=None):
        self.key = key
        self.val = val
        self.prev = prev
        self.next = nextt

class LRUCache:
    def __init__(self):
        """
        Instantiate an LRU cache with no fixed capacity.

        Under the hood, uses a linked list where each node's
        key is a key in a dictionary, mapping to that node.
        """
        self.head = Node(-1,-1)
        self.tail = Node(-1,-1)
        self.tail.next = self.head
        self.head.prev = self.tail
        self.nodeMap = {}

    def __str__(self):
        return str(list(self.nodeMap.keys()))

    def __contains__(self, x):
        return x in self.nodeMap

    def __len__(self):
        return len(self.nodeMap)

    def clear(self):
        """Clear all entries from the LRU cache."""
        self.__init__()

    def delete(self, x):
        """
        Removes the entry from the LRU cache.

        Under the hood, removes the node from the linked list and the dictionary.
        """
        node = self.nodeMap[x]
        del self.nodeMap[x]
        nxt = node.next
        prv = node.prev
        prv.next = nxt
        nxt.prev = prv

    def deleteLRU(self):
        """
        Deletes the LRU entry in the cache.

        Under the hood, deletes the tail of the linked list.
        """
        evicted = self.tail.next.key
        self.delete(evicted)
        return evicted

    def moveToMRU(self, x):
        """
        Moves x to the MRU entry of the cache.

        Under the hood, moves the node with key x to the
        head of the linked list.
        """
        if x in self.nodeMap:
            self.delete(x)
        node = Node(x, x)
        self.nodeMap[x] = node
        p = self.head.prev
        p.next = node
        node.next = self.head
        self.head.prev = node
        node.prev = p