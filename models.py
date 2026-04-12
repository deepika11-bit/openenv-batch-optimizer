from pydantic import BaseModel


class BatchObservation(BaseModel):
    temperature: float
    pressure: float
    speed: float
    energy: float
    yield_rate: float
    quality: float


class BatchAction(BaseModel):
    temperature_change: float
    pressure_change: float
    speed_change: float


class BatchReward(BaseModel):
    reward: float