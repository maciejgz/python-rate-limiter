from datetime import datetime
import threading
import redis
import json


class RedisTokenBucket:
    def __init__(self, bucket_size, refresh_rate, refilling_enabled):
        self.refresh_rate = refresh_rate
        self.size = bucket_size
        self.tokens = bucket_size
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        if refilling_enabled:
            self.fill_bucket_thread()
            
            
    def store_rate_limit_info(self, user_id):
        rate_limit_info = {
            'last_request_time': datetime.now().isoformat()
        }
        self.redis.set(user_id, json.dumps(rate_limit_info))
        
    def get_rate_limit_info(self, user_id):
        rate_limit_info = self.redis.get(user_id)
        if rate_limit_info:
            return json.loads(rate_limit_info)
        else:
            return None
        
        
    ## refilling the bucket    
    def fill_bucket_thread(self):
        threading.Timer(self.refresh_rate, self.add_tokens, args=(self.refresh_rate,)).start()
    
    def add_tokens(self, tokens):
        ## TODO implement
        mock = tokens