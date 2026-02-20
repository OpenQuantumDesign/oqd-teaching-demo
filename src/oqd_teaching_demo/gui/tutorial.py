"""
Quantum Computing Interactive Tutorial Module
For unitaryDESIGN 2026 - Teaching Tool

This module provides interactive tutorials for learning quantum computing concepts
using the trapped-ion demo hardware.
"""

from nicegui import ui
from typing import List, Dict, Callable, Optional
import random

class QuantumTutorial:
    """Interactive quantum computing tutorials using the OQD demo"""
    
    def __init__(self, board):
        self.board = board
        self.current_lesson = 0
        self.lessons = [
            {
                'title': '🎯 What is a Qubit?',
                'content': '''
A qubit (quantum bit) is the basic unit of quantum information.
Unlike classical bits (0 or 1), a qubit can exist in a superposition of both states simultaneously.
                
In our trapped-ion demo:
- Each polystyrene ball represents a qubit
- The "rest" position = |0⟩ state
- The "excited" position = |1⟩ state
                ''',
                'action': self.lesson_qubit
            },
            {
                'title': '⚡ Superposition',
                'content': '''
Superposition allows a qubit to be in both |0⟩ and |1⟩ at the same time!
When we measure, it collapses to one of the states.
                
In our demo:
- Use the laser to excite the ion to a superposition state
- The ion will "vibrate" between positions
                ''',
                'action': self.lesson_superposition
            },
            {
                'title': '🔄 The Hadamard Gate',
                'content': '''
The Hadamard (H) gate creates superposition from a definite state.
H|0⟩ = (|0⟩ + |1⟩)/√2
                
This is the key to quantum computing - it lets us put qubits in superposition
so we can process multiple possibilities at once.
                ''',
                'action': self.lesson_hadamard
            },
            {
                'title': '🔗 Entanglement',
                'content': '''
Entanglement is a quantum phenomenon where two qubits become correlated.
When you measure one entangled qubit, you instantly know the state of the other,
regardless of distance.
                
In our demo, we can entangle multiple ions using laser pulses.
                ''',
                'action': self.lesson_entanglement
            },
            {
                'title': '📊 Measurement',
                'content': '''
Measurement in quantum mechanics is special - it collapses superposition to a definite state.
The probability of measuring |0⟩ or |1⟩ depends on the quantum state.
                
In our demo, the camera captures the final position of each ion.
                ''',
                'action': self.lesson_measurement
            }
        ]
    
    def lesson_qubit(self):
        """Demo: Show qubit states"""
        # Move trap to center - ion at rest = |0⟩
        self.board.device.trap.mode('stop')
        ui.notify('Qubit at |0⟩ state (rest position)', type='positive')
    
    def lesson_superposition(self):
        """Demo: Create superposition using lasers"""
        # Turn on lasers partially to create superposition
        for i in range(len(self.board.device.red_lasers.channels)):
            self.board.device.red_lasers.set_intensity(idx=i, intensity=0.5)
        ui.notify('Creating superposition state!', type='info')
    
    def lesson_hadamard(self):
        """Demo: Apply Hadamard-like operation"""
        # Pulse the laser to create H gate effect
        for i in range(len(self.board.device.red_lasers.channels)):
            self.board.device.red_lasers.set_intensity(idx=i, intensity=0.7)
        import time
        time.sleep(0.5)
        self.board.device.red_lasers.set_intensity(idx=i, intensity=0.3)
        ui.notify('Hadamard gate applied!', type='positive')
    
    def lesson_entanglement(self):
        """Demo: Show entanglement concept"""
        # Use multiple lasers to correlate ions
        for i in range(len(self.board.device.red_lasers.channels)):
            self.board.device.red_lasers.set_intensity(idx=i, intensity=0.8)
        ui.notify('Entangling multiple ions...', type='info')
    
    def lesson_measurement(self):
        """Demo: Show measurement"""
        # Turn off lasers - ion collapses to rest
        for i in range(len(self.board.device.red_lasers.channels)):
            self.board.device.red_lasers.set_intensity(idx=i, intensity=0.0)
        ui.notify('Measurement complete! Ion collapsed to |0⟩', type='positive')
    
    def render(self):
        """Render the tutorial UI"""
        with ui.card().classes('w-full'):
            ui.label('Quantum Computing Tutorials').style('font-size: 24px; font-weight: bold')
            
            # Lesson selector
            lesson_options = [l['title'] for l in self.lessons]
            
            with ui.row():
                ui.label('Select Lesson:')
                lesson_select = ui.select(
                    options=lesson_options, 
                    value=lesson_options[0],
                    on_change=lambda e: self.show_lesson(lesson_options.index(e.value))
                ).classes('w-64')
            
            # Current lesson content
            self.lesson_card = ui.card()
            self.show_lesson(0)
            
            # Navigation
            with ui.row():
                ui.button('← Previous', on_click=lambda: self.prev_lesson()).props('flat')
                ui.button('Next →', on_click=lambda: self.next_lesson()).props('flat')
    
    def show_lesson(self, index: int):
        """Show a specific lesson"""
        self.current_lesson = index
        lesson = self.lessons[index]
        
        self.lesson_card.clear()
        with self.lesson_card:
            ui.label(lesson['title']).style('font-size: 20px; font-weight: bold; color: #6E93D6')
            ui.markdown(lesson['content'])
            ui.button('Try It!', on_click=lesson['action']).props('color=positive')
    
    def next_lesson(self):
        """Go to next lesson"""
        if self.current_lesson < len(self.lessons) - 1:
            self.show_lesson(self.current_lesson + 1)
    
    def prev_lesson(self):
        """Go to previous lesson"""
        if self.current_lesson > 0:
            self.show_lesson(self.current_lesson - 1)


class QuantumCircuitBuilder:
    """Simple quantum circuit builder for the demo"""
    
    def __init__(self, board, num_qubits: int = 2):
        self.board = board
        self.num_qubits = num_qubits
        self.circuit = []
        self.gate_options = ['H', 'X', 'Z', 'CNOT']
    
    def add_gate(self, gate: str, target: int, control: Optional[int] = None):
        """Add a gate to the circuit"""
        self.circuit.append({'gate': gate, 'target': target, 'control': control})
    
    def run_circuit(self):
        """Execute the circuit on the demo hardware"""
        for step in self.circuit:
            gate = step['gate']
            target = step['target']
            
            if gate == 'H':
                # Hadamard - create superposition
                self.board.device.red_lasers.set_intensity(idx=target, intensity=0.7)
            elif gate == 'X':
                # Pauli-X - flip state
                self.board.device.red_lasers.set_intensity(idx=target, intensity=1.0)
            elif gate == 'Z':
                # Pauli-Z - phase shift
                self.board.device.red_lasers.set_intensity(idx=target, intensity=0.3)
            elif gate == 'CNOT':
                # Controlled-NOT - entangle
                for i in range(self.num_qubits):
                    self.board.device.red_lasers.set_intensity(idx=i, intensity=0.8)
        
        ui.notify(f'Executed {len(self.circuit)} gate(s)!', type='positive')
    
    def render(self):
        """Render the circuit builder UI"""
        with ui.card().classes('w-full'):
            ui.label('Quantum Circuit Builder').style('font-size: 24px; font-weight: bold')
            
            # Circuit display
            with ui.row().classes('w-full'):
                for i in range(self.num_qubits):
                    with ui.card().classes('w-32'):
                        ui.label(f'Qubit {i}')
                        gate_select = ui.select(
                            options=self.gate_options,
                            value='I'
                        )
            
            # Run button
            ui.button('Run Circuit', on_click=self.run_circuit).props('color=positive')
            
            # Circuit visualization
            ui.label('Current Circuit:')
            circuit_str = ' → '.join([f"{s['gate']}({s['target']})" for s in self.circuit]) or 'Empty'
            ui.code(circuit_str).classes('w-full')


def add_tutorial_tab(board) -> ui.tab:
    """Add the tutorial tab to the main UI"""
    tutorial = QuantumTutorial(board)
    circuit = QuantumCircuitBuilder(board)
    
    with ui.tab('📚 Quantum Tutorials'):
        tutorial.render()
        ui.separator()
        circuit.render()
    
    return tutorial


# Demo function to test the module
def demo():
    """Demo function to show the tutorial in action"""
    class MockBoard:
        class device:
            class red_lasers:
                channels = [0, 1, 2, 3]
                def set_intensity(self, idx, intensity):
                    print(f"Laser {idx} set to {intensity}")
            class trap:
                def mode(self, m):
                    print(f"Trap mode: {m}")
    
    board = MockBoard()
    tutorial = QuantumTutorial(board)
    
    print("=== Quantum Tutorial Demo ===")
    for i, lesson in enumerate(tutorial.lessons):
        print(f"\nLesson {i+1}: {lesson['title']}")
        print(lesson['content'][:200] + "...")


if __name__ == '__main__':
    demo()
