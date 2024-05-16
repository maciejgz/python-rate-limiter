from dotenv import load_dotenv
from src.api import app
import os
from datetime import datetime, timedelta

load_dotenv()
rate_limiter_algorithm = os.getenv("RATE_LIMITER_ALGORITHM")


@app.middleware("http")
async def add_process_time_header(request, call_next):

    ## get IP address from request
    ip = request.client.host
    user_agent = request.headers.get("user-agent", "")

    unique_user_key = f"{ip}_{user_agent}"

    print(f"Unique user key: {unique_user_key}")
    rate_limiter = RateLimiter(rate_limiter_algorithm)
    rate_limiter.rate_limiter(request)

    response = await call_next(request)
    return response


class RateLimiter:
    def __init__(self, algorithm):
        self.algorithm = algorithm
        
    token_bucket = {}

    def rate_limiter(self, request):
        if self.algorithm == "fixed_window":
            self.fixed_window_rate_limiter(request)
        elif self.algorithm == "sliding_window":
            self.sliding_window_rate_limiter(request)
        elif self.algorithm == "token_bucket":
            self.token_bucket_rate_limiter(request)

    def fixed_window_rate_limiter(self, request):
        print("Fixed window rate limiter logic")

    def sliding_window_rate_limiter(self, request):
        print("Sliding window rate limiter logic")

    def token_bucket_rate_limiter(self, request):
        print("Token bucket rate limiter logic")

        # Get the current time
        current_time = datetime.now()

        user_agent = request.headers.get("user-agent", "")

        # Create a unique key for the user agent
        # in real-world scenarios, this should be more sophisticated e.g. using a hash function of the JWT token, IP and user agent
        ip = request.client.host   
        unique_user_key = f"{ip}_{user_agent}"
        

        # Check if the user agent key exists in the token bucket dictionary
        if unique_user_key not in self.token_bucket:
            # If the key does not exist, create a new token bucket for the user agent
            self.token_bucket[unique_user_key] = {
                "tokens": 4,  # Max bucket size of 4 requests per minute
                "last_request_time": current_time
            }

        # Get the token bucket for the user agent
        bucket = self.token_bucket[unique_user_key]

        # Calculate the time elapsed since the last request
        time_elapsed = current_time - bucket["last_request_time"]

        # Calculate the number of tokens that should be added to the bucket
        tokens_to_add = int(time_elapsed.total_seconds() / 15)

        # Add the tokens to the bucket, up to the maximum bucket size
        bucket["tokens"] = min(bucket["tokens"] + tokens_to_add, 600)

        print(f"Tokens in bucket: {bucket['tokens']}")
        print(f"bucket: {self.token_bucket}")

        # Check if there are enough tokens in the bucket to allow the request
        if bucket["tokens"] >= 1:
            # If there are enough tokens, decrement the token count and update the last request time
            bucket["tokens"] -= 1
            bucket["last_request_time"] = current_time
            print("Request allowed")
        else:
            # If there are not enough tokens, reject the request
            print("Request rejected")

        return







