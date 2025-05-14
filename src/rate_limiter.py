from src.in_memory_token_bucket import InMemoryTokenBucket
from src.leaking_bucket_queue import LeakingBucketQueue
from src.redis_token_bucket import RedisTokenBucket
from src.sliding_window import SlidingWindow


global_in_memory_bucket = InMemoryTokenBucket(15, 15);
redis_token_bucket = RedisTokenBucket(5, 5)
sliding_window = SlidingWindow(5, 5)
leaking_bucket_queue = LeakingBucketQueue()

class RateLimiter:
    def __init__(self, algorithm):
        print("Rate limiter algorithm: " + algorithm)
        self.algorithm = algorithm
        
    token_bucket = {}
    
    def create_unique_key(self, request):
        # Create a unique key for the user agent
        # in real-world scenarios, this should be more sophisticated e.g. using a hash function of the JWT token, IP and user agent
        user_agent = request.headers.get("user-agent", "")
        ip = request.client.host
        return f"{ip}_{user_agent}"
    

    def rate_limiter(self, request):
        if self.algorithm == "redis_token_bucket":
            return self.redis_token_bucket_rate_limiter(request)
        elif self.algorithm == "sliding_window":
            return self.sliding_window_rate_limiter(request)
        elif self.algorithm == "in_memory_token_bucket":
            return self.token_bucket_rate_limiter(request)
        elif self.algorithm == "leaking_bucket_queue":
            return self.leaking_bucket_queue_rate_limiter(request)

    def sliding_window_rate_limiter(self, request):
        print("Sliding window rate limiter logic")
        return sliding_window.consume(self.create_unique_key(request))

    def token_bucket_rate_limiter(self, request):
        print("In memory token bucket rate limiter logic")        
        return global_in_memory_bucket.consume(self.create_unique_key(request), 1);
        
    def redis_token_bucket_rate_limiter(self, request):
        print("Redis token bucket rate limiter logic")
        return redis_token_bucket.consume(self.create_unique_key(request), 1);
    
    def leaking_bucket_queue_rate_limiter(self, request):
        print("Leaking bucket queue rate limiter logic")
        return leaking_bucket_queue.consume(self.create_unique_key(request), 1);
        
    
    