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
Compiles a digital quantum Circuit into a hardware Program (laser intensity
arrays and trap commands) for execution on the teaching demo.

Gate-to-laser mapping rationale:
In a real trapped-ion quantum computer, single-qubit gates are performed by
shining a laser on a specific ion. Different gates require different pulse
patterns. For this teaching demo, each qubit maps to one red laser, and each
gate type maps to a characteristic intensity pattern:

  - X gate (bit flip): full power pulse [1.0, 1.0]
  - Z gate (phase flip): half power pulse [0.5, 0.5]
  - H gate (superposition): ramp pattern [0.7, 0.3, 0.7]
  - I gate (identity): no laser activity
  - CNOT (entanglement): control + target lasers fire together, trap shakes
"""

from typing import List, Tuple

from oqd_teaching_demo.digital import Circuit, UnaryGate, BinaryGate
from oqd_teaching_demo.program import Program

########################################################################################

__all__ = ["compile_circuit"]

########################################################################################

N_LASERS = 4

# Each gate type produces a sequence of intensity values for its target laser.
GATE_PATTERNS = {
    "I": [],
    "X": [1.0, 1.0],
    "Z": [0.5, 0.5],
    "H": [0.7, 0.3, 0.7],
}

########################################################################################


def compile_circuit(
    circuit: Circuit, dt: float = 0.3
) -> Tuple[Program, List[Tuple[int, str]]]:
    """
    Compile a Circuit into laser intensity sequences and trap commands.

    Returns:
        (Program, trap_commands) where trap_commands is a list of
        (step_index, trap_mode) tuples for coordinating trap movement
        during CNOT gates.
    """
    all_intensities: List[List[float]] = []
    trap_commands: List[Tuple[int, str]] = []

    for instruction in circuit.instructions:
        if isinstance(instruction, UnaryGate):
            pattern = GATE_PATTERNS.get(instruction.gate, [])
            if not pattern:
                continue
            target = instruction.target
            if target >= N_LASERS:
                continue
            for intensity in pattern:
                row = [0.0] * N_LASERS
                row[target] = intensity
                all_intensities.append(row)

        elif isinstance(instruction, BinaryGate):
            control = instruction.control
            target = instruction.target
            if control >= N_LASERS or target >= N_LASERS:
                continue

            # Record trap shake start for ion-ion interaction
            trap_commands.append((len(all_intensities), "shake"))

            # Step 1: Control qubit illuminated (identify the control)
            row = [0.0] * N_LASERS
            row[control] = 0.6
            all_intensities.append(row)

            # Step 2-3: Both qubits illuminated (interaction)
            for _ in range(2):
                row = [0.0] * N_LASERS
                row[control] = 0.6
                row[target] = 1.0
                all_intensities.append(row)

            # Step 4: Target qubit only (gate applied)
            row = [0.0] * N_LASERS
            row[target] = 1.0
            all_intensities.append(row)

            # Record trap stop after CNOT completes
            trap_commands.append((len(all_intensities), "stop"))

    if not all_intensities:
        all_intensities = [[0.0] * N_LASERS]

    return Program(red_lasers_intensity=all_intensities, dt=dt), trap_commands
