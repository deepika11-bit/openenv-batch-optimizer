from fastapi import FastAPI
from environment import BatchEnvironment
from models import BatchAction

app = FastAPI()

# create global env instance
env = BatchEnvironment()


@app.post("/reset")
async def reset():
    obs = env.reset()
    return {"observation": obs.__dict__}


@app.post("/step")
async def step():
    # simple default action (can be static)
    action = BatchAction(
        temperature_change=0.5,
        pressure_change=0.1,
        speed_change=0.5,
    )

    obs, reward, done, info = env.step(action)

    return {
        "observation": obs.__dict__,
        "reward": reward,
        "done": done,
        "info": info,
    }


@app.get("/")
def root():
    return {"message": "OpenEnv running"}


# ✅ REQUIRED FUNCTION
def main():
    return app


# ✅ REQUIRED FOR VALIDATION
if __name__ == "__main__":
    main()