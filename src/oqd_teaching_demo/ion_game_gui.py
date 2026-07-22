import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import math
import json
from datetime import datetime
from nicegui import ui
import random
from modules.grover_engine import run_ion_engine

# --- STATE MANAGEMENT ---
game = {
    'stage': 1, 
    'ions': 2, 
    'target': '00', 
    'moves': [], 
    'ion_states': [], 
    'probs': {}, 
    'status': 'System Initialized.',
    'show_next': False,
    'finished': False,
    'history': []  
}

def update_ion_visuals():
    """Updates the binary display based on X-gate toggles."""
    states = [0] * game['ions']
    for move in game['moves']:
        if move.startswith('X'):
            idx = int(move[1:])
            if idx < game['ions']:
                states[idx] = 1 - states[idx]
    game['ion_states'] = states

def reset_level():
    """Generates a new target and clears the buffer."""
    game['target'] = format(random.randint(0, (2**game['ions']) - 1), f'0{game["ions"]}b')
    game['moves'] = []
    game['probs'] = {}
    game['show_next'] = False
    game['status'] = f"Mission: Isolate state |{game['target']}>"
    update_ion_visuals()

def add_move(move):
    """Adds a pulse to the buffer and refreshes the view."""
    game['moves'].append(move)
    game['status'] = f"Pulse {move} added to buffer."
    update_ion_visuals()
    gui_update.refresh()

def run_sequence():
    """Executes Grover Engine and uses 'Smart Threshold' to evaluate success."""
    win_prob, probs = run_ion_engine(game['ions'], game['target'], game['moves'])
    game['probs'] = probs
    
    # SMART THRESHOLD: Theoretical max for 1 Grover iteration on N states
    N = 2**game['ions']
    theta = math.asin(1 / math.sqrt(N))
    theoretical_max = math.sin(3 * theta)**2
    threshold = theoretical_max * 0.9 # Require 90% of theoretical peak
    
    if win_prob >= threshold:
        game['status'] = f"✨ QUANTUM CONVERGENCE! Signal: {win_prob*100:.1f}%"
        game['show_next'] = True  
        game['history'].append({
            'stage': game['stage'],
            'target': game['target'],
            'sequence': list(game['moves']),
            'prob': f"{win_prob*100:.1f}%"
        })
    else:
        game['status'] = f"❌ SIGNAL LOST. Peak: {win_prob*100:.1f}% (Need > {threshold*100:.1f}%)"
        game['show_next'] = False
    gui_update.refresh()

def next_stage():
    """Increments stage or triggers Mission Complete."""
    if game['stage'] >= 5: # Final Stage is 5 (6 ions)
        game['finished'] = True
    else:
        game['stage'] += 1
        game['ions'] += 1
        reset_level()
    gui_update.refresh()

def download_report():
    """Exports session history as a JSON file."""
    report = {
        'session_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'advocate': 'Noor',
        'results': game['history']
    }
    ui.download(json.dumps(report, indent=4).encode(), filename="OQD_Quantum_Report.json")

# --- UI LAYOUT ---

@ui.refreshable
def gui_update():
    # 1. MISSION COMPLETE SCREEN
    if game['finished']:
        with ui.column().classes('w-full items-center p-20 bg-black text-white h-screen'):
            ui.label('✨ MISSION COMPLETE ✨').classes('text-h2 text-yellow-400 font-bold mb-4')
            ui.label('All 5 Stages Clear. Trap Stability Verified.').classes('text-xl text-blue-300 mb-8')
            
            with ui.card().classes('bg-slate-900 p-8 border border-blue-500 shadow-2xl items-center w-full max-w-lg'):
                ui.label('QUANTUM LOG RECORDED').classes('text-xs text-slate-500 mb-2')
                ui.label('Noor, OQD Advocate').classes('text-h5 text-white uppercase tracking-widest')
                ui.separator().classes('bg-slate-700 my-4')
                ui.button('DOWNLOAD FINAL REPORT', on_click=download_report).classes('w-full h-12').props('color=blue-6 icon=download')
                ui.button('RESTART SIMULATION', on_click=lambda: (game.update({'stage':1, 'ions':2, 'finished':False}), reset_level(), gui_update.refresh())).props('flat color=slate-400 mt-4')
        return

    # 2. MAIN GAME UI
    with ui.column().classes('w-full items-center p-8 bg-slate-900 text-white font-mono'):
        with ui.row().classes('w-full justify-between items-center max-w-4xl'):
            ui.label('OQD ION-MAZE SUITE').classes('text-h3 text-blue-400 font-bold')
            ui.button('REPORT', on_click=download_report).props('flat color=slate-400 icon=description')

        # MISSION STATUS
        with ui.card().classes('bg-slate-800 p-6 w-full max-w-2xl border border-blue-900 shadow-2xl mt-4'):
            with ui.row().classes('justify-between w-full'):
                ui.label(f"STAGE {game['stage']}").classes('text-slate-400')
                ui.label(f"TARGET: |{game['target']}>").classes('text-xl text-yellow-400 font-bold')
            ui.label(game['status']).classes('text-sm text-blue-200 mt-2 italic')
            
            if game['moves']:
                ui.label("BUFFER: " + " -> ".join(game['moves'])).classes('text-xs text-orange-400 mt-4 font-bold border-t border-slate-700 pt-2')
        
        # ION TRAP VISUALS
        
        with ui.row().classes('m-6 p-10 border-2 border-blue-900 rounded-xl bg-black w-full justify-center shadow-inner'):
            for i in range(game['ions']):
                val = game['ion_states'][i] if i < len(game['ion_states']) else 0
                is_one = val == 1
                color = "text-yellow-400" if is_one else "text-slate-600"
                glow = "text-shadow: 0 0 20px #fbbf24;" if is_one else ""
                ui.label(f"Ion_{i}:|{val}>").classes(f'mx-4 text-xl font-bold {color}').style(glow)

        # CONTROLS
        with ui.row().classes('gap-4 mb-8'):
            with ui.button_group():
                for i in range(game['ions']):
                    ui.button(f"X{i}", on_click=lambda i=i: add_move(f"X{i}")).props('color=blue-grey-10')
            ui.button("LOCK", on_click=lambda: add_move("LOCK")).props('color=orange-10 icon=lock')
            ui.button("RESET", on_click=lambda: (reset_level(), gui_update.refresh())).props('color=red-10 flat icon=refresh')

        if not game['show_next']:
            ui.button("RUN EXPERIMENT", on_click=run_sequence).classes('w-72 h-16 text-lg').props('color=green-7 icon=play_arrow')
        else:
            ui.button("NEXT STAGE", on_click=next_stage).classes('w-72 h-16 text-lg animate-bounce').props('color=blue-6 icon=arrow_forward')

        # READOUT HISTOGRAM
        if game['probs']:
            ui.label('PHOTON PROBABILITY DENSITY').classes('mt-10 text-xs text-blue-400 tracking-tighter')
            with ui.column().classes('w-full max-w-lg bg-black p-6 rounded-lg border border-slate-800 shadow-2xl'):
                N_val = 2**game['ions']
                th_val = (math.sin(3 * math.asin(1/math.sqrt(N_val)))**2) * 0.9
                for s, p in sorted(game['probs'].items()):
                    is_target = s == game['target']
                    is_winner = is_target and p >= th_val
                    bar_color = "green-5" if is_winner else "yellow-7" if is_target else "blue-grey-9"
                    text_color = "text-green-400" if is_winner else "text-yellow-400" if is_target else "text-slate-500"
                    with ui.row().classes('items-center w-full mb-2'):
                        ui.label(f"|{s}>").classes(f'w-16 text-sm {text_color} font-mono')
                        ui.linear_progress(value=p).classes('flex-grow h-4 rounded').props(f'color={bar_color} stripe animate' if is_target else f'color={bar_color}')
                        ui.label(f"{p*100:4.1f}%").classes(f'w-16 text-right text-xs {text_color}')

# --- INIT ---
reset_level()
gui_update()
ui.run(title="OQD Ion-Maze", dark=True, port=8080)