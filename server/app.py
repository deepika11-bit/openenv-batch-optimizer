from fastapi import FastAPI
import asyncio
from inference import main

app = FastAPI()

@app.post("/reset")
async def reset():
    return {"status": "reset ok"}

@app.post("/step")
async def step():
    return {"status": "step ok"}

@app.get("/")
def root():
    return {"message": "OpenEnv running"}


# ✅ IMPORTANT ADD THIS
def main():
    return app