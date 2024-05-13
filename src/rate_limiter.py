from dotenv import load_dotenv
from src.api import app
import os

load_dotenv()
rate_limiter_algorithm = os.getenv("RATE_LIMITER_ALGORITHM")

@app.middleware("http")
async def add_process_time_header(request, call_next):
    
    ## get IP address from request
    ip = request.client.host    
    user_agent = request.headers.get('user-agent', '')

    unique_user_key = f"{ip}_{user_agent}"
    
    print(f"Unique user key: {unique_user_key}")
    rate_limiter(request);
    
    response = await call_next(request)
    return response


def rate_limiter(request):
    if rate_limiter_algorithm == "fixed_window":
        fixed_window_rate_limiter(request);
    elif rate_limiter_algorithm == "sliding_window":
        sliding_window_rate_limiter(request);
    elif rate_limiter_algorithm == "token_bucket":
        token_bucket_rate_limiter(request);
    return


def fixed_window_rate_limiter(request):
    print("Fixed window rate limiter logic")
    return


def sliding_window_rate_limiter(request):
    print("Sliding window rate limiter logic")
    return

def token_bucket_rate_limiter(request):
    print("Token bucket rate limiter logic")
    return