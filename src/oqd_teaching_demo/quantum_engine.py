from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def run_quantum_level(qubits, target_room, player_moves):
    qc = QuantumCircuit(qubits)
    qc.h(range(qubits))
    qc.barrier()

    for gate in player_moves:
        if gate == 'X0': qc.x(0)
        if gate == 'X1': qc.x(1)
        if gate == 'X2': qc.x(2)
        if gate == 'CZ' and qubits == 2: qc.cz(0, 1)
        if gate == 'CCZ' and qubits == 3: qc.ccz(0, 1, 2)
    qc.barrier()

    qc.h(range(qubits))
    qc.x(range(qubits))
    if qubits == 2:
        qc.cz(0, 1)
    else:
        qc.h(qubits-1)
        qc.mcx(list(range(qubits-1)), qubits-1)
        qc.h(qubits-1)
    qc.x(range(qubits))
    qc.h(range(qubits))

    state = Statevector.from_instruction(qc)
    probs = state.probabilities_dict()
    win_prob = probs.get(target_room[::-1], 0) 
    return win_prob, probs
