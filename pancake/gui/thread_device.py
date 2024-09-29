
import sys

# import pyqtgraph as pg
# from pyqtgraph.functions import mkPen

from PySide6.QtCore import QThread, Signal

import sys
sys.path.append("/home/oqd/outreach/")

from pancake.control.device import Device
from pancake.control.trap import Trap
from pancake.control.lasers import RedLasers
from pancake.program import Program
from pancake.gui.programs import programs


class DeviceThread(QThread):
    task_done_signal = Signal()

    def __init__(self, device: Device):
        super().__init__()
        self.device = device

    def run(self):
        # This will be executed in a separate thread
        program = programs['test']  # todo: figure out how to pass in the program object
        self.device.run(program=program)
        self.task_done_signal.emit()


device = Device(
    # trap=Trap(period=0.9),
    red_lasers=RedLasers(channels=[2, 6, 13, 19, 26]),
)