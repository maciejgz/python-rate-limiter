from dotenv import load_dotenv
from src.api import app
import os
from src.rate_limiter import RateLimiter
from fastapi.responses import JSONResponse


load_dotenv()
rate_limiter_algorithm = os.getenv("RATE_LIMITER_ALGORITHM", "bucket_token")

rate_limiter = RateLimiter(rate_limiter_algorithm)

@app.middleware("http")
async def add_process_time_header(request, call_next):

    rate_limitng_result = rate_limiter.rate_limiter(request)
    
    if rate_limitng_result == False:
        print("Rate limit exceeded. Try again later.")
        return JSONResponse(status_code=429, content={"message": "Rate limit exceeded. Try again later."})
    else:
        response = await call_next(request)
        
    return response

    