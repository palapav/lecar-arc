class Node:
    def __init__(self, key, val, prev=None, nextt=None):
        self.key = key
        self.val = val
        self.prev = prev
        self.next = nextt

class LRUCache:
    def __init__(self):
        self.head = Node(0,0)
        self.tail = Node(0,0)
        self.tail.next = self.head
        self.head.prev = self.tail
        self.nodeMap = {}

    def __len__(self):
        return len(self.nodeMap)

    def delete(self, node):
        nxt = node.next
        prv = node.prev
        prv.next = nxt
        nxt.prev = prv

    def deleteTail(self):
        self.delete(self.tail.next)

    def moveToMRU(self, x):
        if x not in self.nodeMap:
            node = Node(x, x)
            self.nodeMap[x] = node
        p = self.head.prev
        p.next = node
        node.next = self.head
        self.head.prev = node
        node.prev = p