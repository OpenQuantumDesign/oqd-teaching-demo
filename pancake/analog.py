from pydantic import BaseModel
from pancake.base import TypeReflectBaseModel


class MathExpr(TypeReflectBaseModel):
    pass


class Linear(MathExpr):
    max: float = 0.0
    min: float = 1.0
    duration: float = 1.0   # seconds


class ExponentialDecay(MathExpr):
    max: float = 0.0
    min: float = 1.0
    duration: float = 1.0   # seconds


class Sinusoidal(MathExpr):
    max: float = 0.0
    min: float = 1.0
    duration: float = 1.0   # seconds
