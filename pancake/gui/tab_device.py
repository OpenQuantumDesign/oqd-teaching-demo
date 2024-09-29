import copy
import sys
import numpy as np
import pathlib

# import pyqtgraph as pg
# from pyqtgraph.functions import mkPen

from PySide6.QtCore import Qt
from PySide6 import QtCore, QtGui
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QTabWidget, QVBoxLayout, QGridLayout, QHBoxLayout
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSlider
from PySide6.QtWidgets import QLineEdit, QLabel, QDoubleSpinBox, QSpinBox, QCheckBox, QButtonGroup, QRadioButton
from PySide6.QtWidgets import QPushButton, QWidget, QPushButton, QFrame, QDockWidget, QScrollArea, QStatusBar, QComboBox
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont, QColor
from PySide6.QtWidgets import QApplication, QVBoxLayout, QLabel, QLineEdit


from picamera2.previews.qt import QGlPicamera2, QPicamera2

import sys
sys.path.append("/home/oqd/outreach/")

from pancake.control.device import Device
from pancake.program import Program
from pancake.gui.thread_device import DeviceThread, device




class TabDevice(QWidget):

    def __init__(self):
        super(TabDevice, self).__init__()

        self.layout = QHBoxLayout()

        self.panel_red_lasers = PanelRedLasers()
        self.layout.addWidget(self.panel_red_lasers)

        self.panel_trap_position = PanelTrapPosition()
        self.layout.addWidget(self.panel_trap_position)

        self.panel_camera = PanelCamera()
        # QGlPicamera2(picam2=device.camera._camera)
        # self.panel_camera = QGlPicamera2(picam2=device.camera._camera)
        # self.panel_camera = QPicamera2(device.camera._camera)
        self.layout.addWidget(self.panel_camera)

        self.layout.addStretch()
        self.setLayout(self.layout)


class PanelRedLasers(QWidget):
    def __init__(self, num_slides=5):
        super().__init__()
        self.num_slides = num_slides

        layout = QVBoxLayout()

        # Create sliders and labels using list comprehension
        self.sliders = [self.create_slider(i, layout) for i in range(self.num_slides)]

        # Set the layout for the panel
        # layout.addStretch()
        self.setLayout(layout)


    def create_slider(self, i: int, layout: QVBoxLayout):
        # Create a label for the slider

        sublayout = QVBoxLayout()
        label = QLabel(f"Red Laser {i+1}", self)
        sublayout.addWidget(label)

        # Create a slider and configure it for PWM range (0-1)
        slider = QSlider(Qt.Horizontal, self)
        # slider.setFixedHeight(40 * 8)

        slider.setRange(0, 100)  # PWM value between 0-100 (we'll scale this to 0-1)
        slider.setValue(0.5)       # Default to 0
        slider.valueChanged.connect(lambda value, idx=i: self.update_pwm_value(idx, value))
        
        sublayout.addWidget(slider)
        sublayout.addStretch()

        # layout.addWidget(sublayout)
        layout.addLayout(sublayout)

        return slider

    def update_pwm_value(self, idx: int, value):
        # Scale slider value to PWM range (0.0 - 1.0)
        pwm_value = value / 100
        print(f"Slide{idx+1} PWM Value: {pwm_value}")
        # Here you would add the code to set the PWM pin value for the corresponding GPIO pin

        device.red_lasers.set_intensity(idx=idx, intensity=pwm_value)



class PanelTrapPosition(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the layout
        layout = QVBoxLayout()

        # Label to show the current direction
        self.label = QLabel("Stopped", self)
        layout.addWidget(self.label)

        # Create a slider limited to -1, 0, and 1
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(-1)
        self.slider.setMaximum(1)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)  # Only allows -1, 0, and 1
        self.slider.setSingleStep(1)    # Step size is 1 for snapping
        self.slider.setValue(0)         # Default to "Stop" at 0
        self.slider.valueChanged.connect(self.update_label)
        layout.addWidget(self.slider)

        # Set the layout for the widget
        self.setLayout(layout)

    def update_label(self, value):
        # Update the label based on the slider value
        if value == -1:
            self.label.setText("Left")
        elif value == 0:
            self.label.setText("Stopped")
        elif value == 1:
            self.label.setText("Right")





######

class PanelCamera(QWidget):
    def __init__(self, parent=None):
        # super().__init__()
        super().__init__(parent)
        
        # Initialize the Picamera2
        # self.camera = Picamera2()
        # self.camera_config = self.camera.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)})
        # self.camera.configure(self.camera_config)

        # Create a timer for updating the live feed
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        layout = QVBoxLayout()

        # Layout setup  
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(640, 480)

        self.live_button = QPushButton("Start Live Feed", self)
        self.live_button.clicked.connect(self.toggle_live_feed)

        self.capture_button = QPushButton("Capture Image", self)
        self.capture_button.clicked.connect(self.capture_image)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_camera)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.live_button)
        layout.addWidget(self.capture_button)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

        # State to track
        self.is_live = False

    def toggle_live_feed(self):
        if not self.is_live:
            self.is_live = True
            device.camera._camera.start()
            # self.camera.start()
            self.timer.start(30)  # Update every 30 ms (approx 33 fps)
            self.live_button.setText("Stop Live Feed")
        else:
            self.is_live = False
            self.timer.stop()
            device.camera._camera.stop()
            # self.camera.stop()
            self.live_button.setText("Start Live Feed")

    def capture_image(self):
        if self.is_live:
            image = device.camera._camera.capture_array()
            # image = self.camera.capture_array()
            self.show_image(image)
        else:
            print("Camera is not live. Can't capture.")

    def stop_camera(self):
        self.timer.stop()
        device.camera._camera.stop()
        # self.camera.stop()
        self.is_live = False

    # def update_frame(self):
    #     # Capture an image as a numpy array
    #     frame = device.camera._camera.capture_image()
    #     self.image_label.setPixmap(QPixmap.fromImage(qt_image))
    #     qt_image = QImage(frame.data, QImage.Format_RGB888)

    #     # Ensure the image is in RGB format, if necessary convert here
    #     # # Picamera2 captures in RGB888 format by default, so no conversion needed
    #     # if frame is not None:
    #     #     # Convert the numpy array to a QImage
    #     #     height, width, channel = frame.shape
    #     #     bytes_per_line = 3 * width  # 3 bytes per pixel for RGB888
    #     #     qt_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)

    #     #     # Display the QImage on the QLabel
    #     #     self.image_label.setPixmap(QPixmap.fromImage(qt_image))


    def update_frame(self):
        if self.is_live:
            # image = self.camera.capture_array()
            image = device.camera._camera.capture_array()
            # image = device.camera._camera.capture_image()
            self.show_image(image)

    def show_image(self, image):
        # Convert the numpy array to QImage
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        qt_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        self.image_label.setPixmap(pixmap)

