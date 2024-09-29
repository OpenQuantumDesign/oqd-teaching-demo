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
from PySide6.QtWidgets import QPushButton, QFrame, QDockWidget, QScrollArea, QStatusBar, QComboBox
from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont, QColor
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit

import sys
sys.path.append("/home/oqd/outreach/")

from pancake.control.device import Device
from pancake.control.trap import Trap
from pancake.control.lasers import RedLasers
from pancake.program import Program
from pancake.gui.programs import programs
from pancake.gui.tab_device import TabDevice
from pancake.gui.tab_program import TabProgram
from pancake.gui.thread_device import DeviceThread, device

from pancake.gui.style import dark_mode_style_sheet, ui_config





class DemoOQD(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.device = device

        self.title = 'Open Quantum Design'
        self.left = 100
        self.top = 100
        self.width = ui_config['WIDTH']
        self.height = ui_config['HEIGHT']
        # self.setWindowIcon(QtGui.QIcon(ui_config['LOGO_PATH']))

        layout = QVBoxLayout()

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.tab_widget = TabManager()
        # self.tab_widget = TabManager(device=self.device)
        self.setCentralWidget(self.tab_widget)

        self.setLayout(layout)

        self.show()



class TabManager(QWidget):
    def __init__(
            self, 
            # device: Device
        ):
        super(TabManager, self).__init__()

        # self.device = device

        layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        # self.tabs.currentChanged.connect(self.on_tab_change)

        self.tab1 = TabProgram()
        # self.tab1 = TabProgram(device=self.device)
        self.tabs.addTab(self.tab1, "Trap Control")
        # self.tabs.setCurrentIndex(0)

        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def on_tab_change(self):
        return





if __name__ == '__main__':

    app = QApplication(sys.argv)

    main = DemoOQD()
    app.setStyleSheet(dark_mode_style_sheet)

    main.show()
    sys.exit(app.exec())
