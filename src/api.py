from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")}