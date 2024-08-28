from pydantic import BaseModel


class Linear(BaseModel):
    start: float = 0.0
    stop: float = 1.0
    duration: float = 1.0  # seconds


class ExponentialDecay(BaseModel):
    start: float = 0.0
    stop: float = 1.0
    duration: float = 1.0  # seconds


class Sinusoidal(BaseModel):
    start: float = 0.0
    stop: float = 1.0
    duration: float = 1.0  # seconds