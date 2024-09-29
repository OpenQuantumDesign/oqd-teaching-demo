import copy
import sys
import numpy as np
import pathlib

# import pyqtgraph as pg
# from pyqtgraph.functions import mkPen

from PySide6 import QtCore, QtGui
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QTabWidget, QVBoxLayout, QGridLayout, QHBoxLayout
from PySide6.QtWidgets import QLineEdit, QLabel, QDoubleSpinBox, QSpinBox, QCheckBox, QButtonGroup, QRadioButton
from PySide6.QtWidgets import QPushButton, QWidget, QPushButton, QFrame, QDockWidget, QScrollArea, QStatusBar, QComboBox
from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont, QColor
from PySide6.QtWidgets import QApplication, QVBoxLayout, QLabel, QLineEdit

import sys
sys.path.append("/home/oqd/outreach/")

from pancake.control.device import Device
from pancake.program import Program




class TabDevice(QWidget):

    def __init__(self):
        super(TabDevice, self).__init__()

        # self.device = device

        self.layout = QHBoxLayout()

        # self.start_button = QPushButton("Start Device Task", self)
        # self.start_button.setGeometry(50, 50, 200, 50)
        # self.start_button.clicked.connect(self.start_device_task)
        # self.layout.addWidget(self.start_button)

        # self.stop_button = QPushButton("Stop Device Task", self)
        # self.stop_button.setGeometry(50, 120, 200, 50)
        # self.stop_button.clicked.connect(self.stop_device_task)
        # self.stop_button.setEnabled(False)  # Disabled until a task is started
        # self.layout.addWidget(self.stop_button)

        self.layout.addStretch()
        self.setLayout(self.layout)

    # def start_device_task(self):
    #     # Create and start the worker thread
    #     _device._stop_event.clear()  # Clear any previous stop requests
    #     self.device_thread = DeviceThread(_device)
    #     self.device_thread.task_done_signal.connect(self.on_task_done)
    #     self.device_thread.start()
    #     self.start_button.setEnabled(False)
    #     self.stop_button.setEnabled(True)

    # def stop_device_task(self):
    #     # Safely interrupt the task running on the device
    #     _device.stop_task()
    #     self.stop_button.setEnabled(False)

    # def on_task_done(self):
    #     print("Task completed or interrupted!")
    #     self.start_button.setEnabled(True)

