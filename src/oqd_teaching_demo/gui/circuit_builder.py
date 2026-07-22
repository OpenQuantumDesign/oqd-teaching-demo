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
Interactive Quantum Circuit Builder with guided tutorials.

Users visually build quantum circuits on a grid (qubits x time steps),
simulate the quantum state in real-time, view measurement probabilities,
and execute circuits on the demo hardware.

Includes step-by-step tutorials teaching superposition, bit flips,
entanglement (Bell state), and multi-qubit entanglement (GHZ state).
"""

import threading
import time

from nicegui import ui

from oqd_teaching_demo.digital import Circuit, UnaryGate, BinaryGate
from oqd_teaching_demo.digital_simulator import (
    simulate_circuit,
    get_probabilities,
    get_state_labels,
    sample_measurements,
)
from oqd_teaching_demo.digital_compiler import compile_circuit

########################################################################################

N_QUBITS = 4
MAX_COLUMNS = 10
INITIAL_COLUMNS = 6

GATE_COLORS = {
    "I": "#9E9E9E",
    "X": "#E53935",
    "Z": "#1E88E5",
    "H": "#8E24AA",
    "CNOT": "#FB8C00",
}

GATE_DESCRIPTIONS = {
    "I": "Identity - does nothing",
    "X": "NOT gate - flips |0> to |1> and vice versa",
    "Z": "Phase flip - adds a minus sign to |1>",
    "H": "Hadamard - creates superposition (|0> + |1>)/sqrt(2)",
    "CNOT": "Controlled-NOT - flips target qubit if control is |1>",
}

########################################################################################
# Tutorial definitions
########################################################################################

TUTORIALS = [
    {
        "id": "free",
        "title": "Free Build",
        "description": "Build any circuit you want!",
        "steps": [],
        "preset": None,
    },
    {
        "id": "superposition",
        "title": "Lesson 1: Superposition",
        "description": "Learn how a qubit can be in two states at once",
        "steps": [
            "Welcome! All qubits start in state |0>. The circuit is pre-loaded with "
            "an **H (Hadamard) gate** on Q0 — you can see the purple cell in the grid.\n\n"
            "The H gate puts a qubit into an equal **superposition** of |0> and |1>. "
            "Click **'Simulate'** to see the quantum state!",
            "Look at the probability chart on the right: Q0 has a **50/50 chance** of "
            "being measured as 0 or 1. This is superposition — the qubit is in both "
            "states at once until you measure it!\n\n"
            "Now click **'Sample 100 Shots'** to simulate 100 measurements.",
            "Each measurement randomly collapses the superposition. The histogram should "
            "show roughly 50% |0000> and 50% |1000>.\n\n"
            "Try **'Run on Hardware'** to see the laser fire on the demo! You can also "
            "click 'Reset', place gates yourself, and experiment.",
        ],
        "preset": [UnaryGate(gate="H", target=0)],
    },
    {
        "id": "bit_flip",
        "title": "Lesson 2: Quantum NOT (X Gate)",
        "description": "Learn how the X gate flips a qubit",
        "steps": [
            "The **X gate** is the quantum NOT gate. It flips |0> to |1> and vice versa.\n\n"
            "An X gate is already placed on Q0 (the red cell). Click **'Simulate'** — "
            "you should see 100% probability for |1000>.",
            "Now try adding a SECOND X gate: click the **next empty cell** on Q0, "
            "select **'X'** from the palette, and click **'Place Gate'**.\n\n"
            "Two NOT gates cancel out! Simulate again — the state returns to |0000>. "
            "This is called an involution: X * X = I (identity).",
            "Try placing X gates on different qubits to flip individual bits. Each qubit "
            "maps to one laser on the hardware.\n\nClick **'Run on Hardware'** to see it!",
        ],
        "preset": [UnaryGate(gate="X", target=0)],
    },
    {
        "id": "entanglement",
        "title": "Lesson 3: Entanglement (Bell State)",
        "description": "Create an entangled pair of qubits",
        "steps": [
            "Entanglement is one of the most fascinating quantum phenomena. Two entangled "
            "qubits are perfectly correlated — measuring one instantly determines the other.\n\n"
            "The circuit is pre-loaded with an **H gate** on Q0 and a **CNOT gate** from "
            "Q0 to Q1. The CNOT flips the target qubit IF the control qubit is |1>.",
            "Click **'Simulate'**! You should see:\n"
            "  - 50% probability for |0000>\n"
            "  - 50% probability for |1100>\n\n"
            "Q0 and Q1 are now **ENTANGLED**. They are always the same: both 0 or both 1. "
            "This is called a **Bell state**.",
            "Click **'Sample 100 Shots'** to see the correlations. Every measurement gives "
            "either |0000> or |1100> — Q0 and Q1 always match!",
            "Click **'Run on Hardware'**! The trap will **shake** during the CNOT gate — "
            "this represents the ion-ion interaction that creates entanglement in real "
            "trapped-ion quantum computers.",
        ],
        "preset": [
            UnaryGate(gate="H", target=0),
            BinaryGate(gate="CNOT", control=0, target=1),
        ],
    },
    {
        "id": "ghz",
        "title": "Lesson 4: GHZ State",
        "description": "Entangle all 4 qubits together",
        "steps": [
            "A **GHZ (Greenberger-Horne-Zeilinger)** state extends entanglement to many "
            "qubits. All qubits become maximally entangled.\n\n"
            "The circuit is pre-loaded: H on Q0, then CNOT from Q0 to Q1, Q0 to Q2, "
            "and Q0 to Q3. Click **'Simulate'** to see the result!",
            "You should see:\n"
            "  - 50% probability for |0000>\n"
            "  - 50% probability for |1111>\n\n"
            "All 4 qubits are **entangled**! They are ALL 0 or ALL 1 — nothing in between. "
            "This is a 4-qubit GHZ state.",
            "Click **'Run on Hardware'** to see all 4 lasers fire. The trap shakes "
            "**three times** (once per CNOT) showing the ion-ion interactions needed.\n\n"
            "In real quantum computers, GHZ states are used in error correction and "
            "quantum sensing!",
        ],
        "preset": [
            UnaryGate(gate="H", target=0),
            BinaryGate(gate="CNOT", control=0, target=1),
            BinaryGate(gate="CNOT", control=0, target=2),
            BinaryGate(gate="CNOT", control=0, target=3),
        ],
    },
]

########################################################################################


def circuit_builder_card(board, stream_ip: str):
    """Create the interactive quantum circuit builder dialog."""

    # ---- State ----
    state = {
        "n_columns": INITIAL_COLUMNS,
        "grid": [[None] * INITIAL_COLUMNS for _ in range(N_QUBITS)],
        "selected_gate": "H",
        "cnot_control": 0,
        "selected_cell": None,  # (qubit, col) or None
        "tutorial_idx": 0,
        "tutorial_step": 0,
    }

    # UI references (assigned during build)
    refs = {}

    # ---- Circuit logic ----

    def build_circuit() -> Circuit:
        """Convert grid state into a Circuit object, reading left-to-right."""
        instructions = []
        for col in range(state["n_columns"]):
            for qubit in range(N_QUBITS):
                cell = state["grid"][qubit][col]
                if cell is None:
                    continue
                if cell["type"] == "unary":
                    instructions.append(UnaryGate(gate=cell["gate"], target=qubit))
                elif cell["type"] == "cnot_target":
                    instructions.append(
                        BinaryGate(gate="CNOT", control=cell["control"], target=qubit)
                    )
        return Circuit(N=N_QUBITS, instructions=instructions)

    def on_cell_click(qubit: int, col: int):
        state["selected_cell"] = (qubit, col)
        rebuild_grid()

    def place_gate():
        if state["selected_cell"] is None:
            ui.notify("Click a cell in the grid first", type="warning")
            return
        qubit, col = state["selected_cell"]
        gate = state["selected_gate"]
        if gate == "CNOT":
            ctrl = state["cnot_control"]
            if ctrl == qubit:
                ui.notify("Control and target must be different qubits", type="negative")
                return
            if state["grid"][ctrl][col] is not None:
                ui.notify(f"Q{ctrl} at t{col} is already occupied", type="negative")
                return
            state["grid"][qubit][col] = {
                "type": "cnot_target",
                "gate": "CNOT",
                "control": ctrl,
            }
            state["grid"][ctrl][col] = {
                "type": "cnot_control",
                "gate": "CNOT",
                "target": qubit,
            }
            ui.notify(f"Placed CNOT (Q{ctrl} → Q{qubit}), t{col}", type="positive")
        else:
            state["grid"][qubit][col] = {"type": "unary", "gate": gate}
            ui.notify(f"Placed {gate} gate on Q{qubit}, t{col}", type="positive")
        rebuild_grid()

    def clear_cell():
        if state["selected_cell"] is None:
            ui.notify("Click a cell in the grid first to select it", type="warning")
            return
        qubit, col = state["selected_cell"]
        cell = state["grid"][qubit][col]
        if cell is None:
            ui.notify("Cell is already empty", type="info")
            return
        if cell["type"] == "cnot_target":
            state["grid"][cell["control"]][col] = None
        elif cell["type"] == "cnot_control":
            state["grid"][cell["target"]][col] = None
        state["grid"][qubit][col] = None
        rebuild_grid()

    def reset_circuit():
        state["n_columns"] = INITIAL_COLUMNS
        state["grid"] = [[None] * INITIAL_COLUMNS for _ in range(N_QUBITS)]
        state["selected_cell"] = None
        rebuild_grid()
        if "prob_chart" in refs:
            refs["prob_chart"].options["series"][0]["data"] = []
            refs["prob_chart"].options["xAxis"]["data"] = []
            refs["prob_chart"].update()
        if "hist_chart" in refs:
            refs["hist_chart"].options["series"][0]["data"] = []
            refs["hist_chart"].options["xAxis"]["data"] = []
            refs["hist_chart"].update()
        if "state_label" in refs:
            refs["state_label"].set_text("State: (click Simulate)")

    def add_column():
        if state["n_columns"] < MAX_COLUMNS:
            state["n_columns"] += 1
            for row in state["grid"]:
                row.append(None)
            rebuild_grid()

    def remove_column():
        if state["n_columns"] > 1:
            state["n_columns"] -= 1
            for row in state["grid"]:
                row.pop()
            if state["selected_cell"] and state["selected_cell"][1] >= state["n_columns"]:
                state["selected_cell"] = None
            rebuild_grid()

    # ---- Grid rendering ----

    def rebuild_grid():
        container = refs.get("grid_container")
        if container is None:
            return
        container.clear()
        with container:
            # Column headers
            with ui.row().classes("items-center gap-1 ml-10"):
                for col in range(state["n_columns"]):
                    ui.label(f"t{col}").classes(
                        "w-16 text-center text-xs text-gray-400"
                    )

            for qubit in range(N_QUBITS):
                with ui.row().classes("items-center gap-1"):
                    ui.label(f"Q{qubit}").classes("w-8 text-sm font-bold font-mono")
                    for col in range(state["n_columns"]):
                        _render_cell(qubit, col)

    def _render_cell(qubit: int, col: int):
        cell = state["grid"][qubit][col]
        is_selected = state["selected_cell"] == (qubit, col)

        if cell is None:
            btn = ui.button(
                "---",
                on_click=lambda q=qubit, c=col: on_cell_click(q, c),
            )
            if is_selected:
                btn.props("dense outline color=primary")
                btn.style("border-width: 3px;")
            else:
                btn.props("dense outline color=grey-4")
            btn.classes("w-16 h-10 text-xs")
        elif cell["type"] == "unary":
            gate = cell["gate"]
            color = GATE_COLORS[gate]
            btn = ui.button(
                gate,
                on_click=lambda q=qubit, c=col: on_cell_click(q, c),
            )
            btn.props("dense unelevated")
            btn.style(f"background-color: {color} !important; color: white !important;")
            if is_selected:
                btn.style(add="border: 3px solid #000;")
            btn.classes("w-16 h-10 text-sm font-bold")
        elif cell["type"] == "cnot_control":
            tgt = cell["target"]
            btn = ui.button(
                f"●→{tgt}",
                on_click=lambda q=qubit, c=col: on_cell_click(q, c),
            )
            btn.props("dense unelevated")
            btn.style(f"background-color: {GATE_COLORS['CNOT']} !important; color: white !important;")
            if is_selected:
                btn.style(add="border: 3px solid #000;")
            btn.classes("w-16 h-10 text-sm font-bold")
        elif cell["type"] == "cnot_target":
            ctrl = cell["control"]
            btn = ui.button(
                f"⊕←{ctrl}",
                on_click=lambda q=qubit, c=col: on_cell_click(q, c),
            )
            btn.props("dense unelevated")
            btn.style(f"background-color: {GATE_COLORS['CNOT']} !important; color: white !important;")
            if is_selected:
                btn.style(add="border: 3px solid #000;")
            btn.classes("w-16 h-10 text-sm font-bold")

    # ---- Simulation ----

    def do_simulate():
        circuit = build_circuit()
        if not circuit.instructions:
            ui.notify("Circuit is empty - place some gates first", type="warning")
            return

        sim_state = simulate_circuit(circuit)
        probs = get_probabilities(sim_state)
        labels = get_state_labels(N_QUBITS)

        # Filter to non-zero for state display
        nonzero = [
            (labels[i], sim_state[i][0])
            for i in range(len(probs))
            if probs[i] > 1e-10
        ]
        parts = []
        for label, amp in nonzero:
            if abs(amp.imag) < 1e-10:
                parts.append(f"{amp.real:.3f}{label}")
            else:
                parts.append(f"({amp.real:.3f}{amp.imag:+.3f}i){label}")
        state_str = " + ".join(parts)
        if "state_label" in refs:
            refs["state_label"].set_text(f"State: {state_str}")

        # Update probability chart
        if "prob_chart" in refs:
            # Only show states with non-negligible probability
            display_labels = []
            display_probs = []
            for i, p in enumerate(probs):
                if p > 1e-10:
                    display_labels.append(labels[i])
                    display_probs.append(round(float(p), 4))

            refs["prob_chart"].options["xAxis"]["data"] = display_labels
            refs["prob_chart"].options["series"][0]["data"] = display_probs
            refs["prob_chart"].update()

        ui.notify("Simulation complete", type="positive")

    def do_sample(n_shots: int = 100):
        circuit = build_circuit()
        if not circuit.instructions:
            ui.notify("Circuit is empty - place some gates first", type="warning")
            return

        sim_state = simulate_circuit(circuit)
        probs = get_probabilities(sim_state)
        counts = sample_measurements(probs, n_shots)

        # Filter to non-zero counts
        display_labels = []
        display_counts = []
        for label, count in counts.items():
            if count > 0:
                display_labels.append(label)
                display_counts.append(count)

        if "hist_chart" in refs:
            refs["hist_chart"].options["xAxis"]["data"] = display_labels
            refs["hist_chart"].options["series"][0]["data"] = display_counts
            refs["hist_chart"].update()

        ui.notify(f"Sampled {n_shots} measurements", type="positive")

    # ---- Hardware execution ----

    def do_run_hardware():
        circuit = build_circuit()
        if not circuit.instructions:
            ui.notify("Circuit is empty", type="warning")
            return

        program, trap_commands = compile_circuit(circuit)
        board.device._stop_event.clear()

        def _run():
            trap_idx = 0
            for i in range(len(program)):
                if board.device._stop_event.is_set():
                    break
                while (
                    trap_idx < len(trap_commands)
                    and trap_commands[trap_idx][0] <= i
                ):
                    board.device.trap.mode(trap_commands[trap_idx][1])
                    trap_idx += 1
                board.device.red_lasers.set_intensities(
                    intensities=program.red_lasers_intensity[i]
                )
                time.sleep(program.dt)
            board.device.red_lasers.off()
            board.device.trap.stop()

        thread = threading.Thread(target=_run, daemon=True)
        thread.start()
        ui.notify(
            f"Running on hardware ({len(program)} steps, {len(program) * program.dt:.1f}s)",
            type="info",
        )

    def do_stop():
        board.device._stop_event.set()
        board.device.trap.stop()
        ui.notify("Stopped", type="warning")

    # ---- Export / Inspect ----

    def show_circuit_json():
        """Show the Circuit object as JSON (OQD digital IR)."""
        circuit = build_circuit()
        if not circuit.instructions:
            ui.notify("Circuit is empty", type="warning")
            return
        circuit_json = circuit.model_dump_json(indent=2)
        with ui.dialog() as json_dialog, ui.card().classes("w-full").style(
            "max-width: 600px"
        ):
            ui.label("Circuit IR (JSON)").style(
                "color: #6E93D6; font-size: 150%; font-weight: 300"
            )
            ui.markdown(
                "This is the digital circuit represented as a JSON object using "
                "OQD's `Circuit` / `UnaryGate` / `BinaryGate` data models."
            ).classes("text-sm")
            ui.code(circuit_json, language="json").classes("w-full")
            ui.button("Close", on_click=json_dialog.close).props("flat")
        json_dialog.open()

    def show_laser_program():
        """Show the compiled laser program that would be sent to hardware."""
        circuit = build_circuit()
        if not circuit.instructions:
            ui.notify("Circuit is empty", type="warning")
            return
        program, trap_commands = compile_circuit(circuit)
        lines = []
        lines.append(f"Total steps: {len(program)}")
        lines.append(f"Time per step: {program.dt}s")
        lines.append(f"Total duration: {len(program) * program.dt:.1f}s")
        lines.append(f"Trap commands: {trap_commands}")
        lines.append("")
        lines.append("Step | Laser 0 | Laser 1 | Laser 2 | Laser 3 | Trap")
        lines.append("-----|---------|---------|---------|---------|-----")
        trap_dict = dict(trap_commands)
        current_trap = "stop"
        for i, row in enumerate(program.red_lasers_intensity):
            if i in trap_dict:
                current_trap = trap_dict[i]
            intensities = " | ".join(f"  {v:.2f}  " for v in row)
            lines.append(f"  {i:2d} | {intensities} | {current_trap}")

        with ui.dialog() as prog_dialog, ui.card().classes("w-full").style(
            "max-width: 700px"
        ):
            ui.label("Compiled Laser Program").style(
                "color: #6E93D6; font-size: 150%; font-weight: 300"
            )
            ui.markdown(
                "This shows how the circuit gets compiled to hardware commands. "
                "Each qubit maps to one red laser. Different gates produce "
                "different intensity patterns."
            ).classes("text-sm")
            ui.code("\n".join(lines)).classes("w-full")
            ui.button("Close", on_click=prog_dialog.close).props("flat")
        prog_dialog.open()

    # ---- Tutorial logic ----

    def load_tutorial(idx: int):
        state["tutorial_idx"] = idx
        state["tutorial_step"] = 0
        tutorial = TUTORIALS[idx]

        # Always reset the grid when switching tutorials
        reset_circuit()

        if tutorial["preset"] is not None:
            # Pre-populate the grid with the tutorial's preset circuit
            col = 0
            for instr in tutorial["preset"]:
                if isinstance(instr, UnaryGate):
                    state["grid"][instr.target][col] = {
                        "type": "unary",
                        "gate": instr.gate,
                    }
                    col += 1
                elif isinstance(instr, BinaryGate):
                    state["grid"][instr.target][col] = {
                        "type": "cnot_target",
                        "gate": "CNOT",
                        "control": instr.control,
                    }
                    state["grid"][instr.control][col] = {
                        "type": "cnot_control",
                        "gate": "CNOT",
                        "target": instr.target,
                    }
                    col += 1
            rebuild_grid()

        update_tutorial_text()

    def update_tutorial_text():
        tutorial = TUTORIALS[state["tutorial_idx"]]
        if not tutorial["steps"]:
            text = tutorial["description"]
        else:
            step = state["tutorial_step"]
            total = len(tutorial["steps"])
            text = f"[Step {step + 1}/{total}] {tutorial['steps'][step]}"

        if "tutorial_text" in refs:
            refs["tutorial_text"].set_content(text)

        if "step_label" in refs:
            steps = tutorial["steps"]
            if steps:
                refs["step_label"].set_text(
                    f"Step {state['tutorial_step'] + 1} of {len(steps)}"
                )
            else:
                refs["step_label"].set_text("")

    def next_step():
        tutorial = TUTORIALS[state["tutorial_idx"]]
        if not tutorial["steps"]:
            return
        if state["tutorial_step"] < len(tutorial["steps"]) - 1:
            state["tutorial_step"] += 1
            update_tutorial_text()
        else:
            ui.notify("Tutorial complete! Try building your own circuits.", type="positive")

    def prev_step():
        tutorial = TUTORIALS[state["tutorial_idx"]]
        if not tutorial["steps"]:
            return
        if state["tutorial_step"] > 0:
            state["tutorial_step"] -= 1
            update_tutorial_text()

    # ---- Build the UI ----

    with ui.dialog().props("maximized") as circuit_dialog, ui.card().classes(
        "w-full h-full"
    ):
        # Header
        with ui.row().classes("w-full items-center justify-between"):
            ui.label("Quantum Circuit Playground").style(
                "color: #6E93D6; font-size: 200%; font-weight: 300"
            )
            ui.button(icon="close", on_click=circuit_dialog.close).props(
                "flat round"
            )

        with ui.row().classes("w-full flex-nowrap gap-4").style("min-height: 80vh"):
            # ===== LEFT PANEL: Circuit + Controls =====
            with ui.column().classes("flex-1"):
                # Tutorial section
                with ui.card().classes("w-full").style(
                    "background-color: #E3F2FD;"
                ):
                    with ui.row().classes("items-center gap-2 flex-wrap"):
                        ui.label("Tutorial:").classes("text-sm font-bold")
                        tutorial_options = {
                            i: t["title"] for i, t in enumerate(TUTORIALS)
                        }
                        ui.select(
                            tutorial_options,
                            value=0,
                            on_change=lambda e: load_tutorial(e.value),
                        ).classes("w-56")
                        ui.button(
                            icon="arrow_back", on_click=prev_step
                        ).props("flat round dense")
                        refs["step_label"] = ui.label("").classes("text-xs")
                        ui.button(
                            icon="arrow_forward", on_click=next_step
                        ).props("flat round dense")

                    refs["tutorial_text"] = ui.markdown(
                        TUTORIALS[0]["description"]
                    ).classes("text-sm")

                ui.separator()

                # Circuit grid
                ui.label("Circuit").classes("text-lg font-bold")
                refs["grid_container"] = ui.column().classes("w-full")
                rebuild_grid()

                # Gate palette
                with ui.row().classes("items-center gap-2 mt-2 flex-wrap"):
                    ui.label("Gate:").classes("text-sm font-bold")
                    for gate_name in ["I", "X", "Z", "H", "CNOT"]:

                        def _select_gate(g=gate_name):
                            state["selected_gate"] = g
                            ui.notify(
                                f"Selected: {g} - {GATE_DESCRIPTIONS[g]}",
                                type="info",
                            )

                        btn = ui.button(gate_name, on_click=_select_gate)
                        btn.style(
                            f"background-color: {GATE_COLORS[gate_name]} !important; color: white !important;"
                        )
                        btn.props("dense").classes("w-14")

                    ui.button("Place Gate", on_click=place_gate).props(
                        "color=primary"
                    )
                    ui.button("Clear Cell", on_click=clear_cell).props(
                        "flat color=negative"
                    )

                # CNOT control + column management
                with ui.row().classes("items-center gap-4 flex-wrap"):
                    with ui.row().classes("items-center gap-1"):
                        ui.label("CNOT Control:").classes("text-sm")
                        ui.select(
                            {i: f"Q{i}" for i in range(N_QUBITS)},
                            value=0,
                            on_change=lambda e: state.update(
                                {"cnot_control": int(e.value) if e.value is not None else 0}
                            ),
                        ).classes("w-20").props("dense")

                    with ui.row().classes("items-center gap-1"):
                        ui.button("+ Column", on_click=add_column).props(
                            "flat color=primary size=sm"
                        )
                        ui.button("- Column", on_click=remove_column).props(
                            "flat color=negative size=sm"
                        )
                        ui.button(
                            "Reset", icon="delete_sweep", on_click=reset_circuit
                        ).props("flat color=negative size=sm")

                ui.separator()

                # Action buttons
                with ui.row().classes("items-center gap-2 flex-wrap"):
                    ui.button(
                        "Simulate", icon="science", on_click=do_simulate
                    ).props("color=primary")
                    ui.button(
                        "Run on Hardware",
                        icon="play_arrow",
                        on_click=do_run_hardware,
                    ).props("color=positive")
                    ui.button(
                        "Stop", icon="stop", on_click=do_stop
                    ).props("color=negative")
                    ui.button(
                        "Sample 100 Shots",
                        icon="casino",
                        on_click=lambda: do_sample(100),
                    ).props("color=teal")
                    ui.button(
                        "Sample 1000",
                        icon="casino",
                        on_click=lambda: do_sample(1000),
                    ).props("flat color=teal")

                with ui.row().classes("items-center gap-2 flex-wrap"):
                    ui.button(
                        "Show Circuit JSON",
                        icon="data_object",
                        on_click=show_circuit_json,
                    ).props("flat color=grey-8")
                    ui.button(
                        "Show Laser Program",
                        icon="memory",
                        on_click=show_laser_program,
                    ).props("flat color=grey-8")

            # ===== RIGHT PANEL: Results =====
            with ui.column().classes("w-96"):
                ui.label("Simulation Results").classes("text-lg font-bold")

                refs["state_label"] = ui.label("State: (click Simulate)").classes(
                    "font-mono text-sm break-all"
                )

                # Probability bar chart (ECharts - bundled with NiceGUI)
                refs["prob_chart"] = ui.echart(
                    {
                        "title": {"text": "Measurement Probabilities", "textStyle": {"fontSize": 13}},
                        "tooltip": {"trigger": "axis"},
                        "xAxis": {
                            "type": "category",
                            "data": [],
                            "axisLabel": {"rotate": 45, "fontSize": 10},
                        },
                        "yAxis": {
                            "type": "value",
                            "max": 1,
                            "name": "Probability",
                        },
                        "series": [
                            {
                                "data": [],
                                "type": "bar",
                                "itemStyle": {"color": "#6E93D6"},
                            }
                        ],
                        "grid": {"bottom": 80},
                    }
                ).classes("w-full").style("height: 250px;")

                # Measurement histogram
                refs["hist_chart"] = ui.echart(
                    {
                        "title": {"text": "Measurement Histogram", "textStyle": {"fontSize": 13}},
                        "tooltip": {"trigger": "axis"},
                        "xAxis": {
                            "type": "category",
                            "data": [],
                            "axisLabel": {"rotate": 45, "fontSize": 10},
                        },
                        "yAxis": {"type": "value", "name": "Count"},
                        "series": [
                            {
                                "data": [],
                                "type": "bar",
                                "itemStyle": {"color": "#66BB6A"},
                            }
                        ],
                        "grid": {"bottom": 80},
                    }
                ).classes("w-full").style("height: 250px;")

                ui.separator()

                # Camera feed
                ui.label("Hardware Camera").classes("text-sm font-bold")
                ui.image(stream_ip).classes("w-full")

    return circuit_dialog
