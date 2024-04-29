from typing import List, Literal, Union, Annotated

from pydantic import BaseModel, root_validator, NonNegativeInt

########################################################################################

__all__ = ["Program", "UnaryGate", "BinaryGate"]

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


class Program(BaseModel):
    N: Literal[5] = 5
    instructions: List[Union[UnaryGate, BinaryGate]]

    @root_validator
    def consistency_check(cls, values):
        for gate in values["instructions"]:
            if gate.target >= values["N"]:
                raise ValueError(f"Inconsistency: target exceeds N")
            if isinstance(gate, BinaryGate) and gate.control >= values["N"]:
                raise ValueError(f"Inconsistency: control exceeds N")
        return values
