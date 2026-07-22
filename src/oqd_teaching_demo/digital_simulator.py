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

"""
Self-contained quantum state simulator for digital circuits.

Provides functions to simulate quantum circuits defined with the digital.py
gate models, compute measurement probabilities, and sample measurement outcomes.
The math follows the same kronecker product approach as emulator.py but without
the external Transformer dependency.
"""

import functools
from typing import Dict, List

import numpy as np

from oqd_teaching_demo.digital import Circuit, UnaryGate, BinaryGate

########################################################################################

__all__ = [
    "simulate_circuit",
    "get_probabilities",
    "get_state_labels",
    "sample_measurements",
]

########################################################################################

basis_map = {
    "ket0": np.array([[1, 0]]).T,
    "ket1": np.array([[0, 1]]).T,
}

gate_map = {
    "I": np.array([[1, 0], [0, 1]], dtype=complex),
    "H": np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2),
    "X": np.array([[0, 1], [1, 0]], dtype=complex),
    "Z": np.array([[1, 0], [0, -1]], dtype=complex),
}

########################################################################################


def _build_unary_operator(gate_name: str, target: int, n_qubits: int) -> np.ndarray:
    """Build full-system operator for a single-qubit gate via kronecker product."""
    return functools.reduce(
        np.kron,
        [
            gate_map[gate_name] if i == target else gate_map["I"]
            for i in range(n_qubits)
        ],
    )


def _build_cnot_operator(control: int, target: int, n_qubits: int) -> np.ndarray:
    """Build full-system CNOT operator: |0><0| x I + |1><1| x X."""
    proj0 = basis_map["ket0"] @ basis_map["ket0"].T
    proj1 = basis_map["ket1"] @ basis_map["ket1"].T

    term0 = functools.reduce(
        np.kron,
        [proj0 if i == control else gate_map["I"] for i in range(n_qubits)],
    )
    term1 = functools.reduce(
        np.kron,
        [
            (
                proj1
                if i == control
                else (gate_map["X"] if i == target else gate_map["I"])
            )
            for i in range(n_qubits)
        ],
    )
    return term0 + term1


def simulate_circuit(circuit: Circuit) -> np.ndarray:
    """Simulate a quantum circuit and return the final state vector."""
    n = circuit.N
    initial_state = functools.reduce(
        np.kron, [basis_map["ket0"] for _ in range(n)]
    )

    state = initial_state.astype(complex)
    for instruction in circuit.instructions:
        if isinstance(instruction, UnaryGate):
            op = _build_unary_operator(instruction.gate, instruction.target, n)
        elif isinstance(instruction, BinaryGate):
            op = _build_cnot_operator(instruction.control, instruction.target, n)
        else:
            continue
        state = op @ state

    return state


def get_probabilities(state: np.ndarray) -> np.ndarray:
    """Compute measurement probabilities |amplitude|^2 for each basis state."""
    return np.abs(state.flatten()) ** 2


def get_state_labels(n_qubits: int) -> List[str]:
    """Generate basis state labels like |0000>, |0001>, etc."""
    return [f"|{format(i, f'0{n_qubits}b')}>" for i in range(2**n_qubits)]


def sample_measurements(probabilities: np.ndarray, n_shots: int = 100) -> Dict[str, int]:
    """Simulate n_shots measurements and return a histogram of outcome counts."""
    n_qubits = int(np.log2(len(probabilities)))
    labels = get_state_labels(n_qubits)
    indices = np.random.choice(len(probabilities), size=n_shots, p=probabilities)
    counts = {label: 0 for label in labels}
    for idx in indices:
        counts[labels[idx]] += 1
    return counts
