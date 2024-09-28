import copy
import sys
import numpy as np
import pathlib
# import matplotlib.pyplot as plt

# import pyqtgraph as pg
# from pyqtgraph.functions import mkPen

from PySide6 import QtCore, QtGui
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QTabWidget, QVBoxLayout, QGridLayout, QHBoxLayout
from PySide6.QtWidgets import QLineEdit, QLabel, QDoubleSpinBox, QSpinBox, QCheckBox, QButtonGroup, QRadioButton
from PySide6.QtWidgets import QPushButton, QFrame, QDockWidget, QScrollArea, QStatusBar, QComboBox
from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont, QColor

# from PyQt5.QtCore import QThread
# from PyQt5.QtCore import pyqtSignal as Signal
# from PIL import ImageColor

import sys
sys.path.append("/home/oqd/outreach/")

from pancake.control.device import Device
from pancake.control.trap import Trap
from pancake.control.lasers import RedLasers



class DeviceThread(QThread):
    task_done_signal = Signal()

    def __init__(self, device):
        super().__init__()
        self.device = device

    def run(self):
        # This will be executed in a separate thread
        self.device.perform_task()
        self.task_done_signal.emit()

    # def laser_show(self):
    #     ts = np.arange(30)
    #     dt = 0.05                
    #     intensities = np.stack(
    #         [
    #             0.2 * (np.sin(0.3 * ts + i) + 1) for i, channel in enumerate(self.device.red_lasers.channels)
    #         ], axis=1
    #     )
    #     self.device.red_lasers.waveform(intensities=intensities, dt=dt)
    #     self.task_done_signal.emit()


    # def trap_shake(self):
    #     self.device.trap.shake()
    #     self.task_done_signal.emit()
        

_device = Device(
    trap=Trap(period=0.9),
    red_lasers=RedLasers(),
)

# Only stores settings for the utils, nothing for the experiment - that should be in the System class
ui_config = dict(
    # settings for the main window(s)
    WIDTH=1024,
    HEIGHT=600,
    COLORS=["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"],
    PLOT_BACKGROUND="#E6E6EA",
    PLOT_FOREGROUND="#434A42",
    # LOGO_PATH=str(pathlib.Path(__file__).parent.parent.parent.joinpath(r'qoqi\interfaces\themes').joinpath('iqc.png')),
)


class LabInterfaceApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = 'Open Quantum Design'
        self.left = 100
        self.top = 100
        self.width = ui_config['WIDTH']
        self.height = ui_config['HEIGHT']
        # self.setWindowIcon(QtGui.QIcon(ui_config['LOGO_PATH']))

        layout = QVBoxLayout()

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.tab_widget = TabManager(self)
        self.setCentralWidget(self.tab_widget)

        self.setLayout(layout)

        self.show()



class TabManager(QWidget):
    def __init__(self, *args, **kwargs):
        super(TabManager, self).__init__()
        layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        # self.tabs.currentChanged.connect(self.on_tab_change)

        self.tab1 = TrapControlTab()
        self.tabs.addTab(self.tab1, "Trap Control")

        # self.tabs.setCurrentIndex(0)

        # Add tabs to widget
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def on_tab_change(self):
        return



class TrapControlTab(QWidget):

    def __init__(self):
        super(TrapControlTab, self).__init__()

        self.layout = QHBoxLayout()

        # self.button_shake = QPushButton(text="Shake Ions")
        # self.button_shake.clicked.connect(self.start_shake_trap)
        # self.layout.addWidget(self.button_shake)

        # self.button_lasers = QPushButton(text="Analog Laser")
        # self.button_lasers.clicked.connect(self.start_laser_show)
        # self.layout.addWidget(self.button_lasers)


        self.start_button = QPushButton("Start Device Task", self)
        self.start_button.setGeometry(50, 50, 200, 50)
        self.start_button.clicked.connect(self.start_device_task)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Device Task", self)
        self.stop_button.setGeometry(50, 120, 200, 50)
        self.stop_button.clicked.connect(self.stop_device_task)
        self.stop_button.setEnabled(False)  # Disabled until a task is started
        self.layout.addWidget(self.stop_button)

        self.layout.addStretch()
        self.setLayout(self.layout)

    def start_device_task(self):
        # Create and start the worker thread
        _device._stop_event.clear()  # Clear any previous stop requests
        self.device_thread = DeviceThread(_device)
        self.device_thread.task_done_signal.connect(self.on_task_done)
        self.device_thread.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_device_task(self):
        # Safely interrupt the task running on the device
        _device.stop_task()
        self.stop_button.setEnabled(False)

    def on_task_done(self):
        print("Task completed or interrupted!")
        self.start_button.setEnabled(True)

    # """ Laser show """
    # def start_laser_show(self):
    #     self.device_thread = DeviceThread(device)
    #     self.device_thread.task_done_signal.connect(self.finish_laser_show)
    #     self.device_thread.start()

    # def finish_laser_show(self):
    #     print("Task completed!")
    #     self.button_lasers.setEnabled(True)  # Re-enable the button when task is done

    # """ Shake trap show """
    # def start_shake_trap(self):
    #     self.device_thread = DeviceThread(device)
    #     self.device_thread.task_done_signal.connect(self.finish_shake_trap)
    #     self.device_thread.start()

    # def finish_shake_trap(self):
    #     print("Task completed!")
    #     self.button_shake.setEnabled(True)  # Re-enable the button when task is done


  

if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyle("Fusion")
    # app.setPalette(palette)

    main = LabInterfaceApp()
    main.show()
    sys.exit(app.exec())
