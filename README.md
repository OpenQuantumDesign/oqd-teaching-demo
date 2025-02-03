# ![Open Quantum Design](https://raw.githubusercontent.com/OpenQuantumDesign/oqd-core/main/docs/img/oqd-logo-text.png)

<h2 align="center">
    Open Quantum Design: Full-stack Trapped-ion Teaching Demo  
</h2>

> [!NOTE]
> :bangbang: This design is still in the prototype stage - version 3 is under active development. Feel free to get in touch if you're interested in getting access to this teaching tool!

What is a trapped ion quantum computer? What are the components that go into building a quantum computer? What are the layers of a "full-stack"? What does it mean to "trap" an ion?

As quantum computers become increasingly widespread in the world, and as their capabilities advance, teaching an intuitive sense of how these machines work, what they are composed of, and how to interact with them is an important mission. At Open Quantum Design, we aim to democratize access to quantum computing technologies and accelerate a quantum-ready workforce and global community.

## Motivation

We want to provide a tactile and interactive activity for learning about, programming, and building quantum computers. This project contains the designs for a "trapped-ion quantum computer," using low-cost, easily accessible electronics.

## What's inside

The demo traps small beads of polystyrene in an acoustic trap, in analogy to ions in an electromagnetic trap, except visible to the naked eye and can be interacted with. Inexpensive diode lasers are added to demonstrate how the ions are manipulated using light. To demonstrate how the real trapped-ion system is measured using photodetectors, a camera module is included. A Raspberry Pi and Arduino Nano control all of these elements, and a touchscreen display provides a user interface. The enclosure is 3D printed and components assembled.

# ![OQD Demo v2](docs/img/demo-v2.jpg)

In the picture of the *version-2* design of the demo unit, six polystyrene balls are suspended in midair by sound. The pressure waves formed by an array of transducers at each end create points where objects are *suspended* in place by the force of the air. While OQD's quantum computers use an electromagnetic potential to trap the ions, the process is quite analogous - and you can actually see the polystyrene beads with your bare eyes, unlike ions! Red and blue lasers, shining onto the "ions," demonstrate how the state of the quantum computer is manipulated and how quantum algorithms are run.

## Want to build your own?

We love to hear that! The current version is still in the prototype stage, and *version-3* is currently in the works. But in this repository, you can find everything you need to build your own trapped ion outreach demo, including the designs, object files to 3D print, electronic wiring diagrams, and the control software.

- [3D printed enclosure components](./design/objects/)
- [Material list](./docs/materials.md)
- [Software](./src/)

## More about quantum computers

Quantum computers utilize the effects of quantum mechanics to process information. Some of the most important effects of quantum mechanics for computing purposes are superposition, entanglement, and measurement.

- **Superposition**: When a quantum particle can be in two distinct states, e.g., spin-up or spin-down, it can also exist in a superposition of those two states.
- **Entanglement**: When two or more quantum particles *interact* with one another, they can become entangled. Entanglement can be seen as two (or more) particles that are correlated in such a way that the state of one particle directly affects the state of the other, no matter the distance between them.
- **Measurement**: The act of measuring a quantum state forces it into one of the possible states, collapsing the superposition.

While classical computers are based on *bits*, information stored as 0s and 1s, quantum computers are based on *qubits*.

Quantum computers can be created using a variety of different underlying quantum systems. Some of the most popular directions that are being pursued include:

- **Atoms/ions**: Isolating individual atoms or ions. These are generally referred to as *trapped ion* or *neutral atom* quantum computers, respectively. These approaches differ in the methods for isolating and controlling the atoms.
- **Photons**: Individual particles, or quanta, of light can be used as the basic building blocks of a quantum computer.
- **Superconducting circuits**: These use superconducting materials to create qubits. Superconducting qubits are one of the most advanced and widely researched types of qubits, with companies like IBM and Google making significant progress in this area.
- **Spins**: Spin-based quantum computers use the spin of electrons or nuclei as qubits. This approach can leverage existing semiconductor technology, making it a promising direction for scalable quantum computing.

Each of these approaches has its own set of advantages and challenges, and research is ongoing to determine which will be the most practical and effective for large-scale quantum computing.

## Ion trap quantum computers

**Advantages of Ion Trap Quantum Computers**

- **Long coherence times**: Ions can remain in a quantum superposition for long times, allowing longer computations to be performed without error.
- **High fidelity operations**: Preparing and measuring the ions can be done to a very high degree of fidelity, which is crucial for accurate quantum computations.
- **All-to-all connectivity**: Trapped ion quantum devices can be made to have *all-to-all* connectivity. Other architectures are limited in which qubits can interact with which other qubits, often due to the physical layout of the device. Trapped ions can overcome this limitation, as the ions can be made to move, or 'shake', with other ions in very controlled ways.
- **Versatility**: Trapped ion systems can be used to simulate a wide range of quantum systems, making them versatile tools for quantum computing and simulation.

These advantages make ion trap quantum computers a promising direction for the development of practical and scalable quantum computing technologies.

Layers of a trapped ion quantum computer include:

- Vacuum chamber to trap ions
- Radiofrequency electrical probes to provide the trapping potential
- Laser system to control ions in the trap, including addressing the ions individually
- Real-time electronics control system
- Software stack enabling users to program the quantum computer

## References

- [1] Maslov, D., Nam, Y. & Kim, J. An Outlook for Quantum Computing [Point of View]. Proc. IEEE 107, 5–10 (2019).
- [2] Pogorelov, I. et al. Compact Ion-Trap Quantum Computing Demonstrator. PRX Quantum 2, 020343 (2021).
- [3] Blatt, R. & Wineland, D. Entangled states of trapped atomic ions. Nature 453, 1008–1015 (2008).
- [4] Shammah, N. et al. Open Hardware in Quantum Technology. Preprint at <https://doi.org/10.48550/arXiv.2309.17233> (2023).
