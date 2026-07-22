# Copyright 2024-2025 Open Quantum Design

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from typing import List, Literal, Union

from pydantic import BaseModel, Field, model_validator, NonNegativeInt

########################################################################################

__all__ = ["Program", "UnaryGate", "BinaryGate", "Circuit"]

########################################################################################


class UnaryGate(BaseModel):
    gate: Literal["I", "X", "Z", "H"]
    target: NonNegativeInt


class BinaryGate(BaseModel):
    gate: Literal["CNOT"]
    control: NonNegativeInt
    target: NonNegativeInt

    @model_validator(mode="after")
    def consistency_check(self):
        if self.control == self.target:
            raise ValueError("Inconsistency: target equals control")
        return self


class Circuit(BaseModel):
    N: int = Field(default=4, ge=1, le=8)
    instructions: List[Union[UnaryGate, BinaryGate]]

    @model_validator(mode="after")
    def consistency_check(self):
        for gate in self.instructions:
            if gate.target >= self.N:
                raise ValueError("Inconsistency: target exceeds N")
            if isinstance(gate, BinaryGate) and gate.control >= self.N:
                raise ValueError("Inconsistency: control exceeds N")
        return self


class Program(BaseModel):
    clock: float = 1.0
    circuit: Circuit
