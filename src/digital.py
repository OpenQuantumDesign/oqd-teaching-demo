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

from pydantic import BaseModel, root_validator, NonNegativeInt

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

    @root_validator
    def consistency_check(cls, values):
        if values["control"] == values["target"]:
            raise ValueError("Inconsistency: target equals control")
        return values


class Circuit(BaseModel):
    N: Literal[5] = 5
    instructions: List[Union[UnaryGate, BinaryGate]]

    @root_validator
    def consistency_check(cls, values):
        for gate in values["instructions"]:
            if gate.target >= values["N"]:
                raise ValueError("Inconsistency: target exceeds N")
            if isinstance(gate, BinaryGate) and gate.control >= values["N"]:
                raise ValueError("Inconsistency: control exceeds N")
        return values


class Program(BaseModel):
    clock: float = 1.0
    circuit: Circuit
