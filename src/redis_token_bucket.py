from datetime import datetime
import threading
import redis
import json
import os
import time
from dotenv import load_dotenv
from src.const import RATE_LIMITER_ALGORITHM_ENV, MASTER_NODE_ENV, REDIS_DB_ENV, REDIS_HOST_ENV, REDIS_PORT_ENV


load_dotenv()
rate_limiter_algorithm = os.getenv(RATE_LIMITER_ALGORITHM_ENV)
master_node = os.getenv(MASTER_NODE_ENV, False).lower() == "true"
redis_host = os.getenv(REDIS_HOST_ENV, "localhost")
redis_port = os.getenv(REDIS_PORT_ENV, 6379)
redis_db = os.getenv(REDIS_DB_ENV, 0)
REDIS_TOKEN_BUCKET_KEY = "token_bucket"
REDIS_USER_ENTRIES_PREFIX = "user:"


class RedisTokenBucket:
    def __init__(self, bucket_size, refresh_rate):
        self.refresh_rate = refresh_rate
        self.size = bucket_size
        self.redis = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
        if master_node:
            print("Master node. Setting the token bucket size to " + str(self.size))
            self.fill_bucket_thread()
            
            
    def store_rate_limit_info(self, user_id):
        rate_limit_info = {
            'last_request_time': datetime.now().isoformat()
        }
        self.redis.set(REDIS_USER_ENTRIES_PREFIX + user_id, json.dumps(rate_limit_info))
        
    def get_rate_limit_info(self, user_id):
        rate_limit_info = self.redis.get(user_id)
        if rate_limit_info:
            return json.loads(rate_limit_info)
        else:
            return None
        
        
    ## refilling the bucket    
    def fill_bucket_thread(self):
        threading.Thread(target=self.add_tokens, args=()).start()
    
    def add_tokens(self):
        while True:
            print("Adding tokens to the bucket " + str(self.size))
            if(self.redis.get(REDIS_TOKEN_BUCKET_KEY)) is None:
                self.redis.set(REDIS_TOKEN_BUCKET_KEY, self.size)
            self.redis.set(REDIS_TOKEN_BUCKET_KEY, min(self.size, int(self.redis.get(REDIS_TOKEN_BUCKET_KEY)) + self.size))
            print("Tokens added. Tokens left: " + str(self.redis.get(REDIS_TOKEN_BUCKET_KEY)))
            time.sleep(self.refresh_rate)
        
    ## consume
    def consume(self, user_id, tokens):
        current_time = datetime.now()
        rate_limit_info = self.get_rate_limit_info(user_id)
        
        if rate_limit_info is None:
            self.store_rate_limit_info(user_id)
        else:
            if (current_time - datetime.fromisoformat(rate_limit_info['last_request_time'])).seconds < self.refresh_rate:
                print("User made a request in the last refresh_rate seconds: " + rate_limit_info['last_request_time'])
                return False
            else:
                self.store_rate_limit_info(user_id)
        
        if (int(self.redis.get(REDIS_TOKEN_BUCKET_KEY)) >= tokens):
            self.redis.set(REDIS_TOKEN_BUCKET_KEY, int(self.redis.get(REDIS_TOKEN_BUCKET_KEY)) - tokens)
            print("Bucket updated. Tokens left: " + str(self.redis.get(REDIS_TOKEN_BUCKET_KEY)))
            return True
        
        return False