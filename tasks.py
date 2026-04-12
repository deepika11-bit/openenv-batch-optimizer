from environment import BatchEnvironment
from models import BatchAction


class BaseTask:
    def __init__(self):
        self.env = BatchEnvironment()

    def run(self):
        raise NotImplementedError


# ✅ TASK 1 — Energy Optimization
class EnergyOptimizationTask(BaseTask):
    grader = {
        "type": "reward_threshold",
        "threshold": 0.5
    }

    def run(self):
        self.env.reset()
        total = 0

        for _ in range(10):
            action = BatchAction(
                temperature_change=-1,
                pressure_change=0,
                speed_change=-1
            )
            obs, reward, done, _ = self.env.step(action)
            total += reward

        # ✅ Normalize score
        score = total / 10
        score = max(0.0, min(1.0, score))

        # ✅ IMPORTANT: Return dict
        return {
            "score": float(score)
        }


# ✅ TASK 2 — Yield + Energy
class YieldEnergyTask(BaseTask):
    grader = {
        "type": "reward_threshold",
        "threshold": 0.5
    }

    def run(self):
        self.env.reset()
        total = 0

        for _ in range(10):
            action = BatchAction(
                temperature_change=1,
                pressure_change=0,
                speed_change=1
            )
            obs, reward, done, _ = self.env.step(action)
            total += reward

        # ✅ Normalize score
        score = total / 10
        score = max(0.0, min(1.0, score))

        return {
            "score": float(score)
        }


# ✅ TASK 3 — Full Optimization
class FullOptimizationTask(BaseTask):
    grader = {
        "type": "reward_threshold",
        "threshold": 0.5
    }

    def run(self):
        self.env.reset()
        total = 0

        for _ in range(10):
            action = BatchAction(
                temperature_change=0.5,
                pressure_change=0.1,
                speed_change=0.5
            )
            obs, reward, done, _ = self.env.step(action)
            total += reward

        # ✅ Normalize score
        score = total / 10
        score = max(0.0, min(1.0, score))

        return {
            "score": float(score)
        }