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

import numpy as np

import functools

########################################################################################

from src import Transformer

########################################################################################

__all__ = ["EmulatorCompiler"]

########################################################################################

basis_map = {"ket0": np.array([[1, 0]]).T, "ket1": np.array([[0, 1]]).T}

gate_map = {
    "I": np.array([[1, 0], [0, 1]]),
    "H": np.array([[1, 1], [1, -1]]) / np.sqrt(2),
    "X": np.array([[0, 1], [1, 0]]),
    "Z": np.array([[1, 0], [0, -1]]),
}

########################################################################################


class EmulatorCompiler(Transformer):
    def visit_Program(self, model):
        return self.visit(model.circuit)

    def visit_Circuit(self, model):
        self.N = model.N

        initial_state = functools.reduce(
            np.kron, [basis_map["ket0"] for _ in range(self.N)]
        )
        gates = self.visit(model.instructions)
        final_state = functools.reduce(np.matmul, reversed(gates)) @ initial_state
        return final_state

    def visit_UnaryGate(self, model):
        return functools.reduce(
            np.kron,
            [
                gate_map[model.gate] if i == model.target else gate_map["I"]
                for i in range(self.N)
            ],
        )

    def visit_BinaryGate(self, model):
        return functools.reduce(
            np.kron,
            [
                (
                    basis_map["ket0"] @ basis_map["ket0"].T
                    if i == model.control
                    else (gate_map["I"] if i == model.target else gate_map["I"])
                )
                for i in range(self.N)
            ],
        ) + functools.reduce(
            np.kron,
            [
                (
                    basis_map["ket1"] @ basis_map["ket1"].T
                    if i == model.control
                    else (gate_map["X"] if i == model.target else gate_map["I"])
                )
                for i in range(self.N)
            ],
        )
