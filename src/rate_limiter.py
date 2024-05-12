from dotenv import load_dotenv
from src.api import app
import os

load_dotenv()
rate_limiter_algorithm = os.getenv("RATE_LIMITER_ALGORITHM")

@app.middleware("http")
async def add_process_time_header(request, call_next):
    response = await call_next(request)
    return response