from datetime import datetime
import uuid
import redis
import os
from dotenv import load_dotenv
from src.const import REDIS_DB_ENV, REDIS_HOST_ENV, REDIS_PORT_ENV


load_dotenv()
redis_host = os.getenv(REDIS_HOST_ENV, "localhost")
redis_port = os.getenv(REDIS_PORT_ENV, 6379)
redis_db = os.getenv(REDIS_DB_ENV, 0)

REDIS_SLIDING_WINDOW_KEY = "sliding_window_set"

class SlidingWindow:
    
    ## window_size is the number of requests allowed during the time span
    window_size = 0;
    
    ## time_span of the window in seconds
    time_span = 0;
    
    def __init__(self, window_size, time_span):
        self.time_span = time_span;
        self.window_size = window_size
        self.redis = redis.Redis(host=redis_host, port=redis_port, db=redis_db) 
        
    def random_user_key(self, user_id):
        return uuid.uuid4().hex + "_" + user_id

    def add_to_window(self, user_id):
        self.redis.execute_command("zadd", REDIS_SLIDING_WINDOW_KEY, datetime.now().timestamp(), self.random_user_key(user_id))
        
    def remove_old_entries(self):
        ## remove all elements that are older than the time span
        current_time = datetime.now().timestamp()
        self.redis.zremrangebyscore(REDIS_SLIDING_WINDOW_KEY, "-inf", current_time - self.time_span)
        
    def consume(self, user_id):
        ## check if set is empty or number of elements in the set is less than window size
        current_size = self.redis.zcard(REDIS_SLIDING_WINDOW_KEY)        
        if current_size is None or current_size < self.window_size:
            self.add_to_window(user_id)
            print("Sliding window rate limit not exceeded, adding to the window. Current window size: " + self.redis.zcard(REDIS_SLIDING_WINDOW_KEY).__str__())
            return True
        else:
            self.remove_old_entries()
            current_size = self.redis.zcard(REDIS_SLIDING_WINDOW_KEY)
            if current_size < self.window_size:
                self.add_to_window(user_id)
                print("Sliding window rate limit not exceeded, adding to the window. Current window size: " + self.redis.zcard(REDIS_SLIDING_WINDOW_KEY).__str__())
                return True
            else:
                print("Sliding window rate limit exceeded, last request was made at: " + str(self.redis.zrange(REDIS_SLIDING_WINDOW_KEY, 0, 0, withscores=True)))
                return False
        
        


