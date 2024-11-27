#  Copyright 2024 OPEN QUANTUM DESIGN
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from src.base import TypeReflectBaseModel


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
