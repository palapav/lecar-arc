"""
An implementation of LeCaR in Python
"""
from cachetools import LRUCache, LFUCache
from collections import OrderedDict
import math
import random
class LeCaR:
    class Page:
        """
        Page represented a fixed-sized block of memory used in temporary storage
        One page represents one entry in the LeCaR cache
        """
        def __init__(self, request_key) -> None:
            self.request_key = request_key # request of type int from user
            self.evicted_time = None
            self.history_time = 0 # time page has spent in history, reset once no longer in history
    
    def __init__(self, cache_size) -> None:
        self.cache_size = cache_size
        self.current_time = 0
        
        # initial RL parameters
        self.weight = 0.5
        self.learning_rate = 0.45
        self.discount_rate = 0.005 ** (1 / self.cache_size)
        self.lru = LRUCache(self.cache_size)
        self.lfu = LFUCache(self.cache_size)
        
        self.lru_history = OrderedDict() # stores page objects
        self.lfu_history = OrderedDict() # stores page objects
        self.lru_weight, self.lfu_weight = self.weight, 1-self.weight
        
        self.weights = [self.lru_weight, self.lfu_weight]
        self.LRU_ACTION = 0
        self.LFU_ACTION = 1
        self.action_types = [self.LRU_ACTION,self.LFU_ACTION]
    
    def _is_cache_full(self):
        # can choose either LRU or LFU cache for checking if LeCaR cache is full
        return self.lru.currsize == self.cache_size
    
    def _is_history_full(self, isLRU):
        if isLRU: return len(self.lru_history.keys()) == self.cache_size
        return len(self.lfu_history.keys()) == self.cache_size
    
    def sample_action(self):
        """samples either LFU or LRU cache based on respective weight"""
        return random.choices(self.action_types, weights=self.weights)[0]
    
    def del_lru_history(self, isLRU):
        if isLRU: value = self.lru_history.popitem(last=False)
        value = self.lfu_history.popitem(last=False)

    # q is the page
    def update_weights(self, page_request_value):
        page_history_time = page_request_value.history_time
        page_reward = self.discount_rate ** page_history_time
        page_request_key = page_request_value.request_key
        if page_request_key in self.lru_history.keys():
            # increase weight for LFU (less regret here)
            self.lfu_weight *= math.exp(self.learning_rate * page_reward)
        elif page_request_key in self.lfu_history.keys():
            self.lru_weight *= math.exp(self.learning_rate * page_reward)
        
        self.lru_weight = self.lru_weight / (self.lru_weight + self.lfu_weight)
        self.lfu_weight = 1 - self.lfu_weight

    def check_cache_hit(self, requested_page):
        found = False
        if requested_page in self.lru.keys():
            found = True
            # reset time clock for this entry
            self.lru[requested_page].inserted_time = self.current_time
            self.lfu[requested_page].inserted_time = self.current_time
        return found
    def process_cache_miss(self, requested_page_key):
        requested_page_value = self.Page(requested_page_key)
        if requested_page_key in self.lru_history.keys():
            removed_page_value = self.lru_history.pop(requested_page_key)
            # inserted time needs to be start of history
            requested_page_value.history_time = self.current_time - removed_page_value.evicted_time
        elif requested_page_key in self.lfu_history.keys():
            removed_page_value= self.lfu_history.pop(requested_page_key)
            requested_page_value.history_time = self.current_time - removed_page_value.evicted_time
        
        self.update_weights(requested_page_value)
        
        # refactor the below code
        if self._is_cache_full():
            sampled_action = self.sample_action()
            if sampled_action == self.LRU_ACTION:
                if self._is_history_full(isLRU=True): self.del_lru_history(isLRU=True)
                # if history is not full -> evict from LeCaR LRU cache and add to LRU history
                evicted_page_key, evicted_page_value = self.lru.popitem()
                evicted_page_value.eviction_time = self.current_time
                self.lru_history[evicted_page_key] = evicted_page_value
            else:
                if self._is_history_full(isLRU=False): self.del_lru_history(isLRU=True)
                # if history is not full -> evict from LeCaR LFU cache and add to LFU history
                evicted_page_key, evicted_page_value = self.lfu.popitem()
                evicted_page_value.eviction_time = self.current_time
                self.lfu_history[evicted_page_key] = evicted_page_value

        # add to LeCaR cache if its cache is not full
        self.lru[requested_page_key] = self.Page(requested_page_key)
        self.lfu[requested_page_key] = self.Page(requested_page_key)

    def process(self, requested_page):
        if not isinstance(requested_page, int): raise ValueError("request is not of type int")
        # request is of type int
        evicted_page, found = None, None
        self.current_time += 1
        found = self.check_cache_hit(requested_page)
        if not found: evicted_page = self.process_cache_miss(requested_page)
        return found, evicted_page

def main():
    pass
if "__name__" == "__main__":
    main()