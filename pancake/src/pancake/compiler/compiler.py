import itertools as itr
import functools

########################################################################################

from ..interface import *
from .visitor import Transformer

########################################################################################

__all__ = ["PYNQCompiler"]

########################################################################################

ch_map = {
    0: ["D0", "D5"],
    1: ["D1", "D6"],
    2: ["D2", "D7"],
    3: ["D3", "D8"],
    4: ["D4", "D9"],
}

gate_map = {
    "I": ["lll", "lll"],
    "X": ["lhl", "llh"],
    "Z": ["hhl", "lhl"],
    "H": ["hhh", "hlh"],
    "CNOT": ["hhh", "hhh"],
}

########################################################################################


class PYNQCompiler(Transformer):
    @staticmethod
    def _compile_wave(wave):
        current = ""
        new_wave = ""
        for element in wave:
            if element == current or element == ".":
                new_wave += "."
                continue
            else:
                current = element
                new_wave += element
        return new_wave

    def visit_Program(self, model):
        self.N = model.N

        gates = self.visit(model.instructions)
        compiled_gates = functools.reduce(
            lambda pulses1, pulses2: [
                dict(
                    name=pulses1[i]["name"],
                    pin=pulses1[i]["pin"],
                    wave=pulses1[i]["wave"] + pulses2[i]["wave"],
                )
                for i in range(self.N * 2)
            ],
            gates,
        )

        for i in range(self.N * 2):
            compiled_gates[i]["wave"] = self._compile_wave(compiled_gates[i]["wave"])

        compiled_program = {
            "signal": [["control"] + compiled_gates],
            "foot": {"tock": 1},
            "head": {"text": "oqd"},
        }
        return compiled_program

    def visit_UnaryGate(self, model):
        pulses = []
        for i, channel in itr.product(range(self.N), range(2)):
            if i == model.target:
                gate = model.gate
            else:
                gate = "I"
            pulses.append(
                dict(
                    name=f"q{i}ch{channel}",
                    pin=ch_map[i][channel],
                    wave=gate_map[gate][channel],
                )
            )
        return pulses

    def visit_BinaryGate(self, model):
        pulses = []
        for i, channel in itr.product(range(self.N), range(2)):
            if i == model.target or i == model.control:
                gate = model.gate
            else:
                gate = "I"
            pulses.append(
                dict(
                    name=f"q{i}ch{channel}",
                    pin=ch_map[i][channel],
                    wave=gate_map[gate][channel],
                )
            )
        return pulses
