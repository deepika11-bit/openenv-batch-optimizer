from fastapi import FastAPI

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

# ✅ REQUIRED FUNCTION
def main():
    return app

# ✅ REQUIRED FOR VALIDATION
if __name__ == "__main__":
    main()