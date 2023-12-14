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
        def __init__(self, request_key, current_time) -> None:
            self.inserted_time = current_time
            self.request_key = request_key # request of type int from user
            self.evicted_time = None
            self.history_time = 0 # time page has spent in history, reset once no longer in history
    
    def __init__(self, cache_size) -> None:
        random.seed(0) # for debugging
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
        else: value = self.lfu_history.popitem(last=False)

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

    def check_cache_hit(self, requested_page_key):
        found = False
        if requested_page_key in self.lru.keys() and requested_page_key in self.lfu.keys():
            found = True
            # reset time clock for this entry
            # self.lru[requested_page_key].inserted_time = self.current_time
            # self.lfu[requested_page_key].inserted_time = self.current_time
            # print(f"is requested page in LFUL{requested_page_key in self.lfu.keys()}")
            self.lru[requested_page_key].inserted_time = self.current_time
            self.lfu[requested_page_key].inserted_time = self.current_time
        return found
    
    def process_cache_miss(self, requested_page_key):
        requested_page_value = self.Page(requested_page_key, self.current_time)

        if requested_page_key in self.lru_history.keys():
            print(f"requested page keyzz: {requested_page_key}")
            # print(f"LRU HISTORY values:{self.lru_history.values()}")
            removed_page_value = self.lru_history.pop(requested_page_key)
            assert isinstance(removed_page_value, self.Page)
            # inserted time needs to be start of history
            requested_page_value.history_time = self.current_time - removed_page_value.evicted_time
        elif requested_page_key in self.lfu_history.keys():
            removed_page_value = self.lfu_history.pop(requested_page_key)
            requested_page_value.history_time = self.current_time - removed_page_value.evicted_time
        
        self.update_weights(requested_page_value)
        
        # refactor the below code
        if self._is_cache_full():
            print(f"CACHE IS FULL NOW!!")
            sampled_action = self.sample_action()
            print(f"sampled action:{sampled_action}")
            if sampled_action == self.LRU_ACTION:
                if self._is_history_full(isLRU=True): self.del_lru_history(isLRU=True)
                # if history is not full -> evict from LeCaR LRU cache and add to LRU history
                evicted_page_key, evicted_page_value = self.lru.popitem()
                evicted_page_value.evicted_time = self.current_time
                print(f"eviction time in page value:{evicted_page_value.evicted_time}")
                self.lru_history[evicted_page_key] = evicted_page_value
            else:
                if self._is_history_full(isLRU=False): self.del_lru_history(isLRU=True)
                # if history is not full -> evict from LeCaR LFU cache and add to LFU history
                evicted_page_key, evicted_page_value = self.lfu.popitem()
                evicted_page_value.evicted_time = self.current_time
                self.lfu_history[evicted_page_key] = evicted_page_value

        # add to LeCaR cache if its cache is not full
        self.lru[requested_page_key] = requested_page_value
        self.lfu[requested_page_key] = requested_page_value

    def process(self, requested_page):
        if not isinstance(requested_page, int): raise ValueError("request is not of type int")
        # request is of type int
        found = None
        self.current_time += 1
        found = self.check_cache_hit(requested_page)
        if not found: self.process_cache_miss(requested_page)
        return found

def main():
    lecar_cache = LeCaR(cache_size=10)
    NUM_REQUESTS = 1000
    cache_hits = 0
    for i in range(NUM_REQUESTS):
        print(f"Iteration:{i}")
        # print(f"LRU cache numbers:{lecar_cache.lru.keys()}")
        rand_number = random.randint(0,10)
        found = lecar_cache.process(rand_number)
        if found: cache_hits +=1


    print(f"Hit rate: {cache_hits/NUM_REQUESTS}")

if __name__ == "__main__":
    main()