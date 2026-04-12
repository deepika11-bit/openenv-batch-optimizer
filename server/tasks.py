print("TASKS MODULE LOADED", flush=True)

from environment import BatchEnvironment
from models import BatchAction


class BaseTask:
    def __init__(self):
        self.env = BatchEnvironment()

    def run(self):
        raise NotImplementedError


# 🔧 Helper to ensure STRICT (0,1)
def normalize_score(score):
    if score <= 0:
        return 0.01
    elif score >= 1:
        return 0.99
    return float(score)


# 🟢 EASY
class EnergyOptimizationTask(BaseTask):
    grader = {
        "type": "score"
    }

    def run(self):
        obs = self.env.reset()
        total_energy = 0
        steps = 10
        actual_steps = 0

        for _ in range(steps):
            action = BatchAction(
                temperature_change=-1,
                pressure_change=0,
                speed_change=-1
            )

            obs, reward, done, _ = self.env.step(action)
            total_energy += obs.energy
            actual_steps += 1

            if done:
                break

        avg_energy = total_energy / max(1, actual_steps)
        score = 1 - (avg_energy / 150)

        return {
            "score": normalize_score(score)
        }


# 🟡 MEDIUM
class YieldEnergyTask(BaseTask):
    grader = {
        "type": "score"
    }

    def run(self):
        obs = self.env.reset()
        total_score = 0
        steps = 10
        actual_steps = 0

        for _ in range(steps):
            action = BatchAction(
                temperature_change=1,
                pressure_change=0,
                speed_change=1
            )

            obs, reward, done, _ = self.env.step(action)

            yield_score = obs.yield_rate / 100
            energy_penalty = obs.energy / 150

            step_score = (0.7 * yield_score) - (0.3 * energy_penalty)

            total_score += step_score
            actual_steps += 1

            if done:
                break

        score = total_score / max(1, actual_steps)

        return {
            "score": normalize_score(score)
        }


# 🔴 HARD
class FullOptimizationTask(BaseTask):
    grader = {
        "type": "score"
    }

    def run(self):
        obs = self.env.reset()
        total_score = 0
        steps = 10
        actual_steps = 0

        for _ in range(steps):
            action = BatchAction(
                temperature_change=0.5,
                pressure_change=0.1,
                speed_change=0.5
            )

            obs, reward, done, _ = self.env.step(action)

            yield_score = obs.yield_rate / 100
            quality_score = obs.quality / 100
            energy_penalty = obs.energy / 200

            step_score = (
                (0.4 * yield_score)
                + (0.4 * quality_score)
                - (0.2 * energy_penalty)
            )

            total_score += step_score
            actual_steps += 1

            if done:
                break

        score = total_score / max(1, actual_steps)

        return {
            "score": normalize_score(score)
        }


# ✅ REQUIRED
TASKS = {
    "energy_optimization": EnergyOptimizationTask,
    "yield_energy_balance": YieldEnergyTask,
    "full_optimization": FullOptimizationTask,
}