from fastapi import FastAPI
from datetime import datetime
from src.leaking_bucket_queue import LeakingBucketQueue, LeakingBucketQueueProcessor

app = FastAPI()

# Inicjalizacja kolejki i procesora jako globalne obiekty
bucket_queue = LeakingBucketQueue()
processor = LeakingBucketQueueProcessor(interval=5.0)

@app.on_event("startup")
async def startup_event():
    bucket_queue.clear_queue()
    processor.start()

@app.on_event("shutdown")
async def shutdown_event():
    processor.stop()

@app.get("/")
async def root():
    return {"message": "RATE LIMITING API " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")}