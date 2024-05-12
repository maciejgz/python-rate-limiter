from dotenv import load_dotenv
from src.api import app
import os


load_dotenv()

@app.middleware("http")
async def add_process_time_header(request, call_next):
    response = await call_next(request)
    print(os.getenv('RATE_LIMITER_ALGORITHM'))
    return response