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
Mock version of the teaching demo GUI for development without hardware.

Run with: python -m oqd_teaching_demo.gui.main_mock
"""

from nicegui import ui
import atexit
import logging

from oqd_teaching_demo.control.mock import MockDevice

logging.basicConfig(level=logging.INFO)


class Board:
    """Singleton board controller using MockDevice for testing."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            logging.info("Creating new Board instance with MockDevice")
            cls._instance = super(Board, cls).__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        else:
            logging.info("Reusing existing Board instance")
        return cls._instance

    def _initialize(self):
        self.device = MockDevice()
        logging.info("MockDevice initialized")

    def cleanup(self):
        logging.info("Board cleanup")


def control_card(board: Board):
    """Control panel dialog for manual laser and trap control."""
    with ui.dialog() as control_dialog, ui.card().classes("w-96"):
        ui.label("Control Panel").style(
            "color: #6E93D6; font-size: 200%; font-weight: 300"
        )

        with ui.column().classes("w-full gap-4"):
            # Laser controls
            ui.label("Red Lasers").classes("text-lg font-bold")
            sliders = {}
            for i in range(len(board.device.red_lasers.channels)):
                with ui.row().classes("w-full items-center"):
                    ui.label(f"Laser {i}").classes("w-16")
                    slider = (
                        ui.slider(min=0.0, max=1.0, step=0.01, value=0.0)
                        .props("color=red label-always")
                        .classes("flex-grow")
                        .on(
                            "change",
                            lambda e, idx=i: board.device.red_lasers.set_intensity(
                                idx=idx, intensity=e.args
                            ),
                        )
                    )
                    sliders[i] = slider

            def all_on():
                for idx, slider in sliders.items():
                    slider.value = 1.0
                    board.device.red_lasers.set_intensity(idx=idx, intensity=1.0)

            def all_off():
                for idx, slider in sliders.items():
                    slider.value = 0.0
                    board.device.red_lasers.set_intensity(idx=idx, intensity=0.0)

            with ui.row().classes("gap-2"):
                ui.button("All On", on_click=all_on, color="red")
                ui.button("All Off", on_click=all_off)

            ui.separator()

            # Trap controls
            ui.label("Trap Control").classes("text-lg font-bold")
            toggle = ui.toggle(
                {"left": "Left", "stop": "Stop", "right": "Right", "shake": "Shake"},
                value="stop",
                on_change=lambda e: board.device.trap.mode(e.value),
            ).classes("w-full")

            ui.separator()

            # Blue laser
            ui.label("Blue Laser").classes("text-lg font-bold")
            with ui.row().classes("gap-2"):
                ui.button(
                    "On", on_click=lambda: board.device.blue_laser.on(), color="blue"
                )
                ui.button("Off", on_click=lambda: board.device.blue_laser.off())

    return control_dialog


def main():
    board = Board()
    atexit.register(board.cleanup)

    control_dialog = control_card(board)

    with ui.column().classes("w-full items-center p-8"):
        ui.label("OQD Teaching Demo").classes("text-3xl font-bold mb-4")
        ui.label("Mock Mode - No Hardware Required").classes(
            "text-lg text-gray-500 mb-8"
        )

        with ui.row().classes("gap-4"):
            ui.button(
                "Control Panel", on_click=control_dialog.open, color="primary"
            ).classes("text-lg")

        ui.label("Check your terminal for mock hardware output").classes(
            "text-sm text-gray-400 mt-8"
        )


if __name__ in {"__main__", "__mp_main__"}:
    main()
    ui.run(
        title="OQD Teaching Demo (Mock)",
        host="127.0.0.1",
        port=8080,
        reload=True,
    )
