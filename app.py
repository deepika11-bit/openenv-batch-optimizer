from fastapi import FastAPI
import asyncio
from inference import main  # your existing logic

app = FastAPI()

@app.post("/reset")
async def reset():
    return {"status": "reset done"}

@app.post("/step")
async def step():
    return {"status": "step done"}

@app.get("/")
def root():
    return {"message": "OpenEnv running"}

@app.on_event("startup")
async def run_inference():
    asyncio.create_task(main())