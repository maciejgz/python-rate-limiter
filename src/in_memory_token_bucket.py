from datetime import datetime
import threading


class InMemoryTokenBucket:
    def __init__(self, bucket_size, refresh_rate):
        self.refresh_rate = refresh_rate
        self.size = bucket_size
        self.tokens = bucket_size
        self.fill_bucket_thread()
        
    
    user_requests_dict = {}
        
    ## This method should consume tokens from the bucket. User is allowed to make a request if there are enough tokens in the bucket and 
    ## he didn't make a request in the last refresh_rate seconds. If the user is allowed to make a request, the method should return True
    ## and False otherwise. If the user is allowed to make a request, the method should also update the last_update time and the number of tokens in the bucket.
    def consume(self, user_id, tokens):
        current_time = datetime.now()
        
        if self.user_requests_dict.get(user_id) is None:
            self.user_requests_dict[user_id] = current_time
        else:
            if (current_time - self.user_requests_dict[user_id]).seconds < self.refresh_rate:
                print("User made a request in the last refresh_rate seconds: " + str(self.user_requests_dict[user_id]))
                return False
            else:
                self.user_requests_dict[user_id] = current_time
        
        if (self.tokens >= tokens):
            self.tokens -= tokens
            self.user_requests_dict[user_id] = current_time
            print("Bucket updated. Tokens left: " + str(self.tokens))
            return True
        
        return False
    
    def fill_bucket_thread(self):
        threading.Timer(self.refresh_rate, self.add_tokens, args=(self.refresh_rate,)).start()
    
    def add_tokens(self, tokens):
        print("Adding tokens to the bucket " + str(tokens))
        self.tokens = min(self.size, self.tokens + tokens)
        print("Tokens added. Tokens left: " + str(self.tokens))
        self.user_requests_dict = {}
        
    
    
    