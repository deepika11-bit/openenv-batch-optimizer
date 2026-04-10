import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from tasks import TASKS   

app = FastAPI()

# -----------------------
# STATE (required for tests)
# -----------------------
state = {
    "step_count": 0
}

# -----------------------
# TASKS (from your API)
# -----------------------
tasks = [
    "energy_optimization",
    "yield_energy_balance",
    "full_optimization"
]

# -----------------------
# ROOT
# -----------------------
@app.get("/")
def root():
    return {"message": "OpenEnv running"}

# -----------------------
# RESET
# -----------------------
@app.post("/reset")
def reset():
    state["step_count"] = 0
    return {"status": "reset ok"}

# -----------------------
# STEP (FIXED - IMPORTANT)
# -----------------------
@app.post("/step")
def step():
    state["step_count"] += 1

    task = tasks[(state["step_count"] - 1) % len(tasks)]

    return {
        "status": "step ok",
        "step": state["step_count"],
        "task": task
    }

# -----------------------
# TASKS
# -----------------------
@app.get("/tasks")
def get_tasks():
    return {
        "tasks": list(TASKS.keys())
    }


# ✅ REQUIRED FUNCTION
def main():
    return app


# ✅ REQUIRED FOR VALIDATION
if __name__ == "__main__":
    main()