import random
from typing import Tuple

from env.models import BatchObservation, BatchAction


class BatchEnvironment:
    def __init__(self):
        self.state_data = None
        self.steps = 0
        self.max_steps = 10

    def reset(self) -> BatchObservation:
        self.steps = 0

        self.state_data = {
            "temperature": random.uniform(50, 100),
            "pressure": random.uniform(1, 5),
            "speed": random.uniform(10, 50),
        }

        return self._get_observation()

    def state(self):
        return self.state_data

    def step(self, action: BatchAction) -> Tuple[BatchObservation, float, bool, dict]:
        self.steps += 1

        # Apply action
        self.state_data["temperature"] += action.temperature_change
        self.state_data["pressure"] += action.pressure_change
        self.state_data["speed"] += action.speed_change

        # Clamp values
        self.state_data["temperature"] = max(0, min(150, self.state_data["temperature"]))
        self.state_data["pressure"] = max(0, min(10, self.state_data["pressure"]))
        self.state_data["speed"] = max(0, min(100, self.state_data["speed"]))

        obs = self._get_observation()
        reward = self._calculate_reward(obs)

        done = self.steps >= self.max_steps

        return obs, reward, done, {}

    def _get_observation(self) -> BatchObservation:
        temp = self.state_data["temperature"]
        pressure = self.state_data["pressure"]
        speed = self.state_data["speed"]

        # Simulated formulas
        energy = temp * 0.5 + speed * 0.3 + pressure * 10
        yield_rate = max(0, 100 - abs(temp - 80) - abs(speed - 40))
        quality = max(0, 100 - abs(pressure - 3) * 10)

        return BatchObservation(
            temperature=temp,
            pressure=pressure,
            speed=speed,
            energy=energy,
            yield_rate=yield_rate,
            quality=quality,
        )

    def _calculate_reward(self, obs: BatchObservation) -> float:
        # Normalize values
        yield_score = obs.yield_rate / 100
        quality_score = obs.quality / 100
        energy_penalty = obs.energy / 200  # scaled

        reward = (0.4 * yield_score) + (0.4 * quality_score) - (0.2 * energy_penalty)

        return max(0.0, min(1.0, reward))