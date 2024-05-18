from src.in_memory_token_bucket import InMemoryTokenBucket
from datetime import datetime, timedelta


global_in_memory_bucket = InMemoryTokenBucket(15, 15);

class RateLimiter:
    def __init__(self, algorithm):
        self.algorithm = algorithm
        
    token_bucket = {}
    

    def rate_limiter(self, request):
        if self.algorithm == "fixed_window":
            return self.fixed_window_rate_limiter(request)
        elif self.algorithm == "sliding_window":
            return self.sliding_window_rate_limiter(request)
        elif self.algorithm == "in_memory_token_bucket":
            return self.token_bucket_rate_limiter(request)

    def fixed_window_rate_limiter(self, request):
        print("Fixed window rate limiter logic")

    def sliding_window_rate_limiter(self, request):
        print("Sliding window rate limiter logic")

    def token_bucket_rate_limiter(self, request):
        print("In memory token bucket rate limiter logic")

        # Get the current time
        current_time = datetime.now()

        user_agent = request.headers.get("user-agent", "")

        # Create a unique key for the user agent
        # in real-world scenarios, this should be more sophisticated e.g. using a hash function of the JWT token, IP and user agent
        ip = request.client.host   
        unique_user_key = f"{ip}_{user_agent}"
        
        return global_in_memory_bucket.consume(unique_user_key, 1);
        
        
    
    