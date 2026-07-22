import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def run_ion_engine(num_qubits, target_str, moves):
    """
    Core Quantum Engine for the OQD Ion-Maze.
    Maps UI 'Pulses' to Qiskit gates and executes a Grover iteration.
    """
    # Initialize Simulator
    simulator = AerSimulator()
    qc = QuantumCircuit(num_qubits)

    # 1. STEP: INITIAL SUPERPOSITION (Preparation)
    # Apply Hadamard to all ions to create an equal superposition of all states.
    for i in range(num_qubits):
        qc.h(i)

    # 2. STEP: USER-DEFINED ORACLE (Phase Marking)
    # This is the "Maze" part. The user must rotate the target to |1...1> 
    # so the LOCK (Multi-Controlled Phase) gate can flip its sign.
    for move in moves:
        if move.startswith('X'):
            idx = int(move[1:])
            if idx < num_qubits:
                qc.x(idx)
        elif move == 'LOCK':
            # MARKER: Flips the phase of the |11...1> state.
            if num_qubits > 1:
                # Multi-Controlled Phase gate (MCP) with pi rotation
                qc.mcp(np.pi, list(range(num_qubits - 1)), num_qubits - 1)
            else:
                qc.z(0)

    # 3. STEP: GROVER DIFFUSER (Amplitude Amplification)
    # Standard reflection about the mean.
    # 
    for i in range(num_qubits):
        qc.h(i)
        qc.x(i)
    
    # Reflection about the |0...0> state
    if num_qubits > 1:
        qc.mcp(np.pi, list(range(num_qubits - 1)), num_qubits - 1)
    else:
        qc.z(0)
        
    for i in range(num_qubits):
        qc.x(i)
        qc.h(i)

    # 4. MEASUREMENT
    qc.measure_all()

    # 5. EXECUTION & ENDIANNESS MAPPING
    # Transpile for performance
    t_qc = transpile(qc, simulator)
    job = simulator.run(t_qc, shots=2048)
    counts = job.result().get_counts()

    # Convert results to Big-Endian for the OQD UI 
    # (Qiskit's '001' is actually our Ion_0=1, Ion_1=0, Ion_2=0)
    total_shots = sum(counts.values())
    probs = {}
    for i in range(2**num_qubits):
        # Generate the state string in the order the UI expects (Big-Endian)
        ui_state = format(i, f'0{num_qubits}b')
        # Reverse it to fetch the data from Qiskit's Little-Endian output
        qiskit_key = ui_state[::-1]
        probs[ui_state] = counts.get(qiskit_key, 0) / total_shots

    return probs.get(target_str, 0.0), probs