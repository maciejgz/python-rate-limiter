from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "RATE LIMITING API " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")}