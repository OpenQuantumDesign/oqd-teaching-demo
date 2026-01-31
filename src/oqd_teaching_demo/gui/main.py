from nicegui import ui
import threading
import atexit
import sys
import logging

from oqd_teaching_demo.program import Program

# For development & testing (i.e., unitaryDESIGN participants!), set this MOCK = True
MOCK = True

if MOCK:
    from oqd_teaching_demo.control.mock import MockDevice as Device
else:
    from oqd_teaching_demo.control.device import Device as Device
    

stream_ip = 'http://127.0.0.1:5000/stream'

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


def control_card(board: Board):
    with ui.dialog() as control_dialog, ui.card():
        ui.label('Control Panel').style('color: #6E93D6; font-size: 200%; font-weight: 300')

        with ui.row().classes('fixed-center'):


            with ui.list().classes('w-32'):
                sliders = {}
                for i in range(len(board.device.red_lasers.channels)):
                    ui.label(f"Control Laser {i}")
                    slider = ui.slider(
                        min=0.0, max=1.0, step=0.01, value=0.5, 
                        # on_change=lambda value, idx=i: device.red_lasers_set_intensity(idx=idx, intensity=value)
                    ).props('color=red').on('change', lambda e, idx=i: board.device.red_lasers.set_intensity(idx=idx, intensity=e.args))
                    sliders[i] = slider
                    slider.value = 0.0
                
                def all_on():
                    for idx, slider in sliders.items():
                        slider.value = 1.0
                        board.device.red_lasers.set_intensity(idx=idx, intensity=1.0)

                def all_off():
                    for idx, slider in sliders.items():
                        slider.value = 0.0
                        board.device.red_lasers.set_intensity(idx=idx, intensity=0.0)

            with ui.card():
                ui.button('Lasers On', on_click=all_on)
                ui.button('Lasers Off', on_click=all_off)


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
                ui.image(stream_ip)#.classes('w-full h-auto')

        return control_dialog



def digital_card(board: Board):
    with ui.dialog() as digital_dialog, ui.card():
        with ui.row().classes('fixed-center'):
            with ui.list():
                ui.button("Shor's Algorithm", on_click=lambda: board.device.run(digital_shor())).props('border p-33')
                ui.button("Random Circuit", on_click=lambda: board.device.run(digital_random())).props('border p-3')

            with ui.card().classes('w-full'):
                ui.image(stream_ip)

    return digital_dialog
    

def analog_card(board: Board):
    with ui.dialog() as analog_dialog, ui.card():
        with ui.row().classes('fixed-center'):
            with ui.list():
                ui.button("Nearest Neighbours Ising", on_click=lambda: board.device.run(analog_ising()))
                ui.button("All-to-All Interactions", on_click=lambda: board.device.run(analog_all_to_all()))


            with ui.card().classes('w-full'):
                ui.image(stream_ip)

    return analog_dialog


def main():

    board = Board()
    atexit.register(board.cleanup)

    

    control_dialog = control_card(board)
    digital_dialog = digital_card(board)
    analog_dialog = analog_card(board)

    with ui.column():
        with ui.row().classes('fixed-center'):
            ui.button('Control Panel', on_click=control_dialog.open)
            ui.button('Digital Interface', on_click=digital_dialog.open)
            ui.button('Analog Interface', on_click=analog_dialog.open)

        ui.image("https://github.com/OpenQuantumDesign/equilux/blob/9ed0c5380133e7d135121c44c3f4cdbcb8cf781b/docs/img/oqd-logo.png?raw=true").classes("w-32 h-32")



# Start the NiceGUI app
if __name__ in {"__main__", "__mp_main__"}:
    main()
    ui.run(
        title='Physics Demo Control',
        host='0.0.0.0',
        port=8080,
        reload=False,
        favicon="https://github.com/OpenQuantumDesign/equilux/blob/9ed0c5380133e7d135121c44c3f4cdbcb8cf781b/docs/img/oqd-logo.png?raw=true",
    )
