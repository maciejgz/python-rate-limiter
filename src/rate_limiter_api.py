from dotenv import load_dotenv
from src.api import app
import os
from src.rate_limiter import RateLimiter
from fastapi.responses import JSONResponse


load_dotenv()
rate_limiter_algorithm = os.getenv("RATE_LIMITER_ALGORITHM")

rate_limiter = RateLimiter(rate_limiter_algorithm)

@app.middleware("http")
async def add_process_time_header(request, call_next):

    ## get IP address from request
    ip = request.client.host
    user_agent = request.headers.get("user-agent", "")

    unique_user_key = f"{ip}_{user_agent}"

    rate_limitng_result = rate_limiter.rate_limiter(request)
    
    if rate_limitng_result == False:
        print("Rate limit exceeded. Try again later.")
        return JSONResponse(status_code=429, content={"message": "Rate limit exceeded. Try again later."})
    else:
        response = await call_next(request)
        
    return response

    