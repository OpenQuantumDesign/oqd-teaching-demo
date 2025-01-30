## Quantum computers
Quantum computers utilize the effects of quantum mechanics to process information. 
Some of the most important effects of quantum mechanics for computing purposes are superposition, entanglement, and measurement.

* **Superposition**: When a quantum particle can be in two distinct states, e.g., spin-up or spin-up, it can also exist in a superposition of those two states -- the particles 
* **Entanglement**: When two or more quantum particles *interact* with one another, they can become entangled. Entanglement can be seen as two (or more) particles that 
* **Measurement**:

While classical computers are based on *bits*, information stored as 0 and 1's, quantum computers are based on *qubits*. 

Quantum computers can be created using a variety of different underlying quantum systems. 
Some of the most popular directions that are being pursued include:
* **Atoms/ions**: Isolating individual atoms or ions. These are generally referred to as *trapped ion* or *neutral atom* quantum computers, respectively. These approaches differ in the methods for isolating and controlling the atoms. 
* **Photons**: Individual particles, or quanta, of light can be used as the basic building blocks of a quantum computer. 
* **Superconducting circuits**: These use superconducting materials to create qubits. Superconducting qubits are one of the most advanced and widely researched types of qubits, with companies like IBM and Google making significant progress in this area.
* **Spins**: Spin-based quantum computers use the spin of electrons or nuclei as qubits. This approach can leverage existing semiconductor technology, making it a promising direction for scalable quantum computing.

Each of these approaches has its own set of advantages and challenges, and research is ongoing to determine which will be the most practical and effective for large-scale quantum computing.


## Ion trap quantum computers
* Ions can remain in a quantum superposition for long times, allowing longer computations to be performed without error.
* Preparing and measuring the ions can be done to a very high degree of fidelity.
* Trapped ion quantum devices can be made to have *all-to-all* connectivity. Other architectures are limited in which qubits can interact with which other qubits, often due to the physical layout of the device. Trapped ions can overcome this limitation, as the ions can be made to move, or 'shake', coupled with other ions in very controlled ways. 

<!-- ![trapped-ion](img/ion-trap-connected.png) -->
<!-- ![trap-design](img/simplified-hardware-stack.png) -->

Layers of trapped ion quantum computer include:
* Vacuum chamber to trap ions
* Radiofrequency electrical probes to provide the trapping potential
* Laser system to control ions in the trap, including addressing the ions individually
* Real-time electronics control system
* Software stack enabling users to program the quantum computer


## References
* [1] Maslov, D., Nam, Y. & Kim, J. An Outlook for Quantum Computing [Point of View]. Proc. IEEE 107, 5–10 (2019).
* [2] Pogorelov, I. et al. Compact Ion-Trap Quantum Computing Demonstrator. PRX Quantum 2, 020343 (2021).
* [3] Blatt, R. & Wineland, D. Entangled states of trapped atomic ions. Nature 453, 1008–1015 (2008).
* [4] Shammah, N. et al. Open Hardware in Quantum Technology. Preprint at https://doi.org/10.48550/arXiv.2309.17233 (2023).