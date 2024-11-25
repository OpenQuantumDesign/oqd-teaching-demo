from nicegui import ui
import threading
import atexit
import sys
import logging
sys.path.append("/home/oqd/outreach/")

from pancake.control.device import Device, RedLasers, BlueLaser, Trap
from pancake.nicegui.programs import digital_simple

from pancake.program import Program


class Board:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            logging.info("Creating new GpioControl instance")
            cls._instance = super(Board, cls).__new__(cls)
            cls._instance._initialize_gpio(*args, **kwargs)
        else:
            logging.info("Reusing existing Board instance")
        return cls._instance

    def _initialize_gpio(self):
        self.device = Device()
        logging.info(f"Device initialized")

    def cleanup(self):
        return
        # self.device.close()

# class DeviceThread(QThread):
#     task_done_signal = Signal()

#     def __init__(self, device: Device):
#         super().__init__()
#         self.device = device

#     def run(self):
#         # This will be executed in a separate thread
#         program = programs['test']  # todo: figure out how to pass in the program object
#         self.device.run(program=program)
#         self.task_done_signal.emit()



def control_card(board: Board):
    with ui.dialog() as control_dialog, ui.card():
        ui.label('Control Panel').style('color: #6E93D6; font-size: 200%; font-weight: 300')

        with ui.row().classes('fixed-center'):


            with ui.list().classes('w-32'):
                sliders = {}
                for i in range(5):
                    ui.label(f"Control Laser {i}")
                    slider = ui.slider(
                        min=0.0, max=1.0, step=0.01, value=0.5, 
                        # on_change=lambda value, idx=i: device.red_lasers_set_intensity(idx=idx, intensity=value)
                    ).props('color=red').on('change', lambda e, idx=i: board.device.red_lasers.set_intensity(idx=idx, intensity=e.args))
                    sliders[i] = slider
                    slider.value = 0.0

            with ui.card():
                toggle = ui.toggle(
                    {
                        'left': 'Left', 
                        'right': 'Right', 
                        'stop': 'Stop',
                        # 'shake': 'Shake', 
                    }, 
                    on_change=lambda e: board.device.trap.mode(e.value)
                )
                toggle.value = "stop"


            with ui.card().classes('w-full'):
                ui.image('http://172.31.60.59:5000/stream')#.classes('w-full h-auto')

        return control_dialog



# def run(program: Program):
    # DeviceThread


def digital_card(board: Board):
    with ui.dialog() as digital_dialog, ui.card():
        # ui.label('Digital').style('color: #6E93D6; font-size: 200%; font-weight: 300')


        with ui.column().classes('fixed-center'):
            ui.button('Quantum Circuit', on_click=lambda: board.device.run(digital_simple()))

            ui.button('Stop', on_click=lambda: board.device.stop())
        
    return digital_dialog
    

def main():

    board = Board()
    atexit.register(board.cleanup)

    

    control_dialog = control_card(board)
    digital_dialog = digital_card(board)



    # with ui.image('oqd-logo-text.png'):
    # with ui.image("https://github.com/OpenQuantumDesign/equilux/blob/9ed0c5380133e7d135121c44c3f4cdbcb8cf781b/docs/img/oqd-logo.png?raw=true"):
    with ui.column():
        with ui.row().classes('fixed-center'):
            ui.button('Control Panel', on_click=control_dialog.open)
            ui.button('Digital Interface', on_click=digital_dialog.open)
            ui.button('Analog Interface',)

        ui.image("https://github.com/OpenQuantumDesign/equilux/blob/9ed0c5380133e7d135121c44c3f4cdbcb8cf781b/docs/img/oqd-logo.png?raw=true").classes("w-32 h-32")



# Start the NiceGUI app
if __name__ in {"__main__", "__mp_main__"}:
    main()
    ui.run(
        title='Physics Demo Control',
        host='0.0.0.0',
        port=8080,
        reload=False,
        # favicon='oqd-logo.png',  # Optional favicon
        favicon="https://github.com/OpenQuantumDesign/equilux/blob/9ed0c5380133e7d135121c44c3f4cdbcb8cf781b/docs/img/oqd-logo.png?raw=true",
    )
