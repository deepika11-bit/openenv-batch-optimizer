from env.environment import BatchEnvironment
from env.models import BatchAction


class BaseTask:
    def __init__(self):
        self.env = BatchEnvironment()

    def run(self):
        raise NotImplementedError


# 🟢 EASY TASK — Minimize Energy
class EnergyOptimizationTask(BaseTask):
    def run(self):
        obs = self.env.reset()
        total_energy = 0

        for _ in range(10):
            action = BatchAction(
                temperature_change=-1,
                pressure_change=0,
                speed_change=-1
            )

            obs, reward, done, _ = self.env.step(action)
            total_energy += obs.energy

            if done:
                break

        avg_energy = total_energy / 10
        score = max(0, min(1, 1 - (avg_energy / 150)))

        return {"score": score}


# 🟡 MEDIUM TASK — Balance Yield + Energy
class YieldEnergyTask(BaseTask):
    def run(self):
        obs = self.env.reset()
        total_score = 0

        for _ in range(10):
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

            if done:
                break

        score = max(0, min(1, total_score / 10))
        return {"score": score}

# 🔴 HARD TASK — Full Optimization
class FullOptimizationTask(BaseTask):
    def run(self):
        obs = self.env.reset()
        total_score = 0

        for _ in range(10):
            action = BatchAction(
                temperature_change=0.5,
                pressure_change=0.1,
                speed_change=0.5
            )

            obs, reward, done, _ = self.env.step(action)

            yield_score = obs.yield_rate / 100
            quality_score = obs.quality / 100
            energy_penalty = obs.energy / 200

            step_score = (0.4 * yield_score) + (0.4 * quality_score) - (0.2 * energy_penalty)
            total_score += step_score

            if done:
                break

        score = max(0, min(1, total_score / 10))
        return {"score": score}