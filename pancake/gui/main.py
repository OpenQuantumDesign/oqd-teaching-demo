import copy
import sys
import numpy as np
import pathlib
import matplotlib.pyplot as plt

import pyqtgraph as pg
from pyqtgraph.functions import mkPen

from PySide6 import Qt, QtCore, QtGui
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QTabWidget, QVBoxLayout, QGridLayout, QHBoxLayout
from PySide6.QtWidgets import QLineEdit, QLabel, QDoubleSpinBox, QSpinBox, QCheckBox, QButtonGroup, QRadioButton
from PySide6.QtWidgets import QPushButton, QFrame, QDockWidget, QScrollArea, QStatusBar, QComboBox
from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont, QColor
from PIL import ImageColor

# from control.trap import Trap
import sys
sys.path.append("/home/benjamin/Desktop/outreach/")
from pancake.control.trap import Trap
trap = Trap()

# Only stores settings for the utils, nothing for the experiment - that should be in the System class
ui_config = dict(

    # settings for the main window(s)
    WIDTH=1024,
    HEIGHT=600,
    COLORS=["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"],
    PLOT_BACKGROUND="#E6E6EA",
    PLOT_FOREGROUND="#434A42",

    # LOGO_PATH=str(pathlib.Path(__file__).parent.parent.parent.joinpath(r'qoqi\interfaces\themes').joinpath('iqc.png')),

    # interactivity settings
    REFRESH_TIME=300,
    NUMBER_POINTS_MEM=100,

    # font size to use for the photon count and power value number strings
    NUMERIC_FONT_SIZE=20,

    # number of SPD plots to have
    NUM_COUNT_PLOTS=3,

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

        # bar = self.menuBar()
        # system_menu = bar.addMenu('System')
        # init_connections = QAction('Initialize system connection', self)
        # system_menu.addAction(init_connections)
        # init_connections.triggered.connect(self.initialize_system_connections)

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

        layout = QHBoxLayout()

        button_shake = QPushButton(text="Bottom")

        
        button_shake.clicked.connect(trap.shake)
        layout.addWidget(button_shake)
        layout.addStretch()
        self.setLayout(layout)


# class QuickEquipmentControlTab(QWidget):

#     def __init__(self, parent):
#         super(QWidget, self).__init__(parent)

#         layout = QHBoxLayout()

#         self.quantum_state_control = QuantumStateControlPanel(self)
#         layout.addWidget(self.quantum_state_control)

#         layout.addStretch()
#         self.setLayout(layout)


# class RunMeasurementsTab(QWidget):
#     def __init__(self, parent):
#         super(QWidget, self).__init__(parent)

#         layout = QHBoxLayout()

#         layout.addWidget(RunMeasurementStateTomography(self))
#         layout.addWidget(RunMeasurementCrossCorrelationHistogram(self))

#         layout.addStretch()
#         self.setLayout(layout)


# class RunMeasurementStateTomography(QFrame):

#     def __init__(self, parent):
#         super(QWidget, self).__init__(parent)
#         self.setFrameShape(QFrame.StyledPanel)

#         layout = QVBoxLayout()

#         layout.addWidget(QLabel("State Tomography:"))

#         run_pushbutton = QPushButton("Run state tomography")
#         run_pushbutton.clicked.connect(self.run_measurement)
#         layout.addWidget(run_pushbutton)

#         # add spinbox for setting the integration time
#         self.int_time_sb = QDoubleSpinBox()
#         self.int_time_sb.setPrefix("Integ. Time: ")
#         self.int_time_sb.setSuffix(" s")
#         self.int_time_sb.setValue(system.config['STATE_TOMOGRAPHY_INTEG_TIME'])
#         self.int_time_sb.setMinimum(0.5)
#         layout.addWidget(self.int_time_sb)

#         # add dropdown menu for the target quantum state
#         self.target_state_dropdown = QComboBox()
#         self.target_state_dropdown.addItems(["phi+", "phi-", "psi+", "psi-", "HH", "HV", "VH", "VV"])
#         layout.addWidget(self.target_state_dropdown)

#         layout.addStretch()
#         self.setLayout(layout)

#     def run_measurement(self):
#         message = "Running state tomography"
#         print(message)
#         self.parent().parent().parent().parent().parent().update_message(message)  # print out info on bottom line

#         target = self.target_state_dropdown.currentText()
#         print(f"The target state is {self.target_state_dropdown.currentText()}")
#         (data, rho, metrics) = measure_state_tomography(system, io=system.io, target=target,
#                                                         integration_time=self.int_time_sb.value(), plot=True)

#         system.io.save_dataframe(data, filename='state_tomography_data.txt')
#         system.io.save_np_array(rho, filename='state_tomography_density_matrix.txt')
#         system.io.save_json(metrics, filename='state_tomography_metrics.txt')

#         plt.show()
#         return


# class RunMeasurementCrossCorrelationHistogram(QFrame):

#     def __init__(self, parent):
#         super(QWidget, self).__init__(parent)
#         self.setFrameShape(QFrame.StyledPanel)

#         layout = QVBoxLayout()

#         layout.addWidget(QLabel("Cross Correlation Histogram:"))

#         run_pushbutton = QPushButton("Run cross-correlation")
#         run_pushbutton.clicked.connect(self.run_measurement)
#         layout.addWidget(run_pushbutton)

#         # add spinbox for setting the integration time
#         self.meas_time = QDoubleSpinBox()
#         self.meas_time.setPrefix("Measurement Time: ")
#         self.meas_time.setSuffix(" s")
#         self.meas_time.setValue(5)
#         self.meas_time.setMinimum(0.2)
#         layout.addWidget(self.meas_time)

#         # add spinbox for which channel to use as Channel A
#         self.ch_a = QSpinBox()
#         self.ch_a.setPrefix("Channel A:")
#         self.ch_a.setValue(1)
#         self.ch_a.setMinimum(1)
#         self.ch_a.setMaximum(16)
#         layout.addWidget(self.ch_a)

#         # add spinbox for which channel to use as Channel B
#         self.ch_b = QSpinBox()
#         self.ch_b.setPrefix("Channel B: ")
#         self.ch_b.setValue(2)
#         self.ch_b.setMinimum(1)
#         self.ch_b.setMaximum(16)
#         layout.addWidget(self.ch_b)

#         # add spinbox for bin width
#         self.bin_width = QDoubleSpinBox()
#         self.bin_width.setPrefix("Bin Width: ")
#         self.bin_width.setSuffix(" ns")
#         self.bin_width.setValue(1)
#         self.bin_width.setMinimum(0.01)
#         layout.addWidget(self.bin_width)

#         # add spinbox for total histogram width
#         self.hist_width = QDoubleSpinBox()
#         self.hist_width.setPrefix("Hist. Width: ")
#         self.hist_width.setSuffix(" ns")
#         self.hist_width.setValue(50)
#         self.hist_width.setMinimum(0.1)
#         layout.addWidget(self.hist_width)

#         layout.addStretch()
#         self.setLayout(layout)

#     def run_measurement(self):
#         message = "Running cross-correlation"
#         print(message)
#         self.parent().parent().parent().parent().parent().update_message(message)  # print out info on bottom line

#         filename = 'time-tags'
#         system.timetagger.save_tags(io=system.io, filename=filename,
#                                     measurement_time=self.meas_time.value(), convert=True)
#         system.timetagger.switch_logic()

#         tags = system.io.load_timetags(filename=filename + ".txt")

#         hist, hist_x, hist_norm = cross_correlation_histogram(tags=tags, ch_a=self.ch_a.value(), ch_b=self.ch_b.value(),
#                                                               bin_width=self.bin_width.value(),
#                                                               hist_width=self.hist_width.value())

#         fig, ax = plt.subplots(1, 1)
#         ax.plot(hist_x, hist)
#         ax.set(xlabel="Time (ns)", ylabel="Counts")
#         system.io.save_figure(fig=fig, filename=f"cross_correlation_ch{self.ch_a.value()}_ch{self.ch_b.value()}.png")
#         plt.show()
#         return


# class ControlPanelLaser(QFrame):

#     def __init__(self, parent):
#         super(QWidget, self).__init__(parent)
#         self.setFrameShape(QFrame.StyledPanel)

#         layout = QVBoxLayout()

#         layout.addWidget(QLabel("Laser Control:"))
#         self.update_button = QPushButton("Update instrument")
#         self.update_button.clicked.connect(self.update_instrument)
#         layout.addWidget(self.update_button)

#         self.emission_checkbox = QCheckBox("Emission")
#         layout.addWidget(self.emission_checkbox)
#         self.power_edit = SliderWithEdit(self, min=0, max=30, step=0.5, unit='mW')
#         self.power_edit.setValue(system.config['LASER_POWER'])

#         layout.addWidget(self.power_edit)

#         layout.addStretch()
#         self.setLayout(layout)

#     def update_instrument(self):
#         message = "Update laser | "
#         if self.emission_checkbox.isChecked():
#             message += "Turn emission on"
#             system.laser.on()
#             system.laser.set_power(self.power_edit.value())
#         else:
#             message += "Turn emission off"
#             system.laser.off()

#         self.parent().parent().parent().parent().parent().update_message(message)
#         print(message)


# class ControlPanelTimeTag(QFrame):

#     def __init__(self, parent):
#         super(QWidget, self).__init__(parent)
#         self.setFrameShape(QFrame.StyledPanel)

#         layout = QVBoxLayout()

#         layout.addWidget(QLabel("Time Tagger Control:"))
#         self.update_button = QPushButton("Update instrument")
#         self.update_button.clicked.connect(self.update_instrument)
#         layout.addWidget(self.update_button)

#         # spinbox for setting the coincidence window of the time tagger
#         self.coinc_window_sb = QDoubleSpinBox()
#         self.coinc_window_sb.setValue(system.config['COINCIDENCE_WINDOW_NS'])  # set to current default from config
#         self.coinc_window_sb.setPrefix("Coinc. Window: ")
#         self.coinc_window_sb.setSuffix(" ns")
#         self.coinc_window_sb.setMaximum(10.0)
#         self.coinc_window_sb.setMinimum(0.25)
#         layout.addWidget(self.coinc_window_sb)

#         scroll = QScrollArea(self)
#         scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
#         scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
#         scroll.setWidgetResizable(True)

#         container = QWidget()
#         scroll.setWidget(container)
#         scroll.layout = QGridLayout(container)

#         scroll.layout.addWidget(QLabel(""), 0, 0)
#         scroll.layout.addWidget(QLabel("Delay (ns)"), 0, 1)
#         scroll.layout.addWidget(QLabel("Threshold (V)"), 0, 2)
#         self.delay_spinboxes = []
#         self.threshold_spinboxes = []
#         for i in range(16):
#             scroll.layout.addWidget(QLabel(f"Ch{i + 1}"), i + 1, 0)

#             sb = QDoubleSpinBox(self)
#             sb.setValue(system.config['TIMETAGGER_CHANNEL_DELAYS'][i])  # set to current default from config
#             self.delay_spinboxes.append(sb)
#             scroll.layout.addWidget(sb, i + 1, 1)

#             sb = QDoubleSpinBox(self)
#             sb.setValue(system.config['TIMETAGGER_CHANNEL_THRESHOLDS'][i])  # set to current default from config
#             sb.setMaximum(4.0)
#             sb.setMinimum(-4.0)
#             self.threshold_spinboxes.append(sb)
#             scroll.layout.addWidget(sb, i + 1, 2)

#         # set layout after adding scroll bar
#         layout.addWidget(scroll)
#         self.setLayout(layout)

#     def update_instrument(self):
#         delays = [delay_spinbox.value() for delay_spinbox in self.delay_spinboxes]
#         thresholds = [threshold_spinbox.value() for threshold_spinbox in self.threshold_spinboxes]
#         window = self.coinc_window_sb.value()

#         system.set_timetagger_window(window)
#         system.set_timetagger_delays(delays)
#         system.set_timetagger_thresholds(thresholds)

#         message = "Update time tagger | "
#         self.parent().parent().parent().parent().parent().update_message(message)
#         print(message)


# class ControlPanelWaveplate(QFrame):

#     def __init__(self, parent):
#         super(QWidget, self).__init__(parent)
#         self.setFrameShape(QFrame.StyledPanel)

#         layout = QVBoxLayout()

#         layout.addWidget(QLabel("Waveplate Control:"))
#         self.update_button = QPushButton("Update instrument")
#         self.update_button.clicked.connect(self.update_instrument)
#         layout.addWidget(self.update_button)

#         wps = {
#             'ALICE_HWP': dict(prefix='Alice HWP: ', suffix=' deg', min=0.0, max=360.0, widget=None),
#             'ALICE_QWP': dict(prefix='Alice QWP: ', suffix=' deg', min=0.0, max=360.0, widget=None),
#             'BOB_HWP': dict(prefix='Bob HWP: ', suffix=' deg', min=0.0, max=360.0, widget=None),
#             'BOB_QWP': dict(prefix='Bob QWP: ', suffix=' deg', min=0.0, max=360.0, widget=None),
#         }

#         for (key, val) in wps.items():
#             sb = QDoubleSpinBox(self)
#             sb.setPrefix(val['prefix'])
#             sb.setSuffix(val['suffix'])
#             sb.setMaximum(val['max'])
#             sb.setMinimum(val['min'])
#             val['widget'] = sb
#             layout.addWidget(sb)
#         self.wps = wps

#         layout.addStretch()
#         self.setLayout(layout)

#     def update_instrument(self):
#         message = "Update waveplates"
#         self.parent().parent().parent().parent().parent().update_message(message)

#         system.set_alice_hwp_angle(float(self.wps['ALICE_HWP']['widget'].value()))
#         system.set_alice_qwp_angle(float(self.wps['ALICE_QWP']['widget'].value()))
#         system.set_bob_hwp_angle(float(self.wps['BOB_HWP']['widget'].value()))
#         system.set_bob_qwp_angle(float(self.wps['BOB_QWP']['widget'].value()))

#         print(message)


# class ControlPanelFunctionGenerator(QFrame):

#     def __init__(self, parent):
#         super(QWidget, self).__init__(parent)
#         self.setFrameShape(QFrame.StyledPanel)

#         layout = QVBoxLayout()

#         layout.addWidget(QLabel("Function Generator Control:"))
#         self.update_button = QPushButton("Update instrument")
#         self.update_button.clicked.connect(self.update_instrument)
#         layout.addWidget(self.update_button)

#         ch1 = {
#             'FREQ': dict(prefix='Frequency: ', suffix=' kHz', min=0.0, max=10.0, widget=None),
#             'AMP': dict(prefix='Voltage: ', suffix=' V', min=0.0, max=3.0, widget=None),
#             'DUTY': dict(prefix='Duty: ', suffix=' %', min=0.0, max=100.0, widget=None),
#             'PHASE': dict(prefix='Phase: ', suffix=' deg', min=0.0, max=360.0, widget=None),
#         }
#         ch2 = copy.deepcopy(ch1)

#         # set all the default values
#         ch1['FREQ']['val'] = system.config['FGEN_SETTINGS']['CH1']['FREQ']
#         ch1['AMP']['val'] = system.config['FGEN_SETTINGS']['CH1']['AMP']
#         ch1['DUTY']['val'] = system.config['FGEN_SETTINGS']['CH1']['DUTY']
#         ch1['PHASE']['val'] = system.config['FGEN_SETTINGS']['CH1']['PHASE']

#         ch2['FREQ']['val'] = system.config['FGEN_SETTINGS']['CH2']['FREQ']
#         ch2['AMP']['val'] = system.config['FGEN_SETTINGS']['CH2']['AMP']
#         ch2['DUTY']['val'] = system.config['FGEN_SETTINGS']['CH2']['DUTY']
#         ch2['PHASE']['val'] = system.config['FGEN_SETTINGS']['CH2']['PHASE']

#         hlayout = QHBoxLayout()
#         for (ch, label) in zip([ch1, ch2], ("Ch. 1", "Ch. 2")):
#             channel_layout = QVBoxLayout()
#             for (key, info) in ch.items():
#                 sb = QDoubleSpinBox(self)
#                 sb.setValue(info['val'])
#                 sb.setPrefix(info['prefix'])
#                 sb.setSuffix(info['suffix'])
#                 sb.setMaximum(info['max'])
#                 sb.setMinimum(info['min'])
#                 info['widget'] = sb

#                 channel_layout.addWidget(sb)

#             output_checkbox = QCheckBox("Output")
#             channel_layout.addWidget(output_checkbox)
#             ch['OUTPUT'] = {'widget': output_checkbox}

#             hlayout.addLayout(channel_layout)

#         self.ch1 = ch1
#         self.ch2 = ch2

#         layout.addLayout(hlayout)
#         layout.addStretch()
#         self.setLayout(layout)

#     def update_instrument(self):
#         system.fgenerator.ch1.set_function("SIN")

#         system.fgenerator.ch1.set_frequency(float(self.ch1['FREQ']['widget'].value()) * 1e3, unit="Hz")
#         system.fgenerator.ch1.set_amplitude(float(self.ch1['AMP']['widget'].value()))
#         if self.ch1['OUTPUT']['widget'].isChecked():
#             system.fgenerator.ch1.set_output_state("ON")
#         else:
#             system.fgenerator.ch1.set_output_state("OFF")

#         system.fgenerator.ch2.set_frequency(float(self.ch2['FREQ']['widget'].value()) * 1e3, unit="Hz")
#         system.fgenerator.ch2.set_amplitude(float(self.ch2['AMP']['widget'].value()))
#         if self.ch2['OUTPUT']['widget'].isChecked():
#             system.fgenerator.ch2.set_output_state("ON")
#         else:
#             system.fgenerator.ch2.set_output_state("OFF")

#         # print(system.fgenerator.get_settings())
#         message = "Update function generator"

#         self.parent().parent().parent().parent().parent().update_message(message)
#         print(message)


# class QuantumStateControlPanel(QFrame):

#     def __init__(self, parent):
#         super(QWidget, self).__init__(parent)
#         self.setFrameShape(QFrame.StyledPanel)

#         layout = QVBoxLayout()

#         layout.addWidget(QLabel("Quantum State Control:"))
#         analyzers_layout = QHBoxLayout()

#         alice_group_layout = QVBoxLayout()
#         alice_group_layout.addWidget(QLabel("Alice"))
#         alice_group = QButtonGroup(self)
#         alice_group.buttonClicked.connect(self.set_projection_alice)
#         for j, proj in enumerate(('H', 'V', 'D', 'A', 'L', 'R')):
#             button = QRadioButton(proj)
#             button.proj = proj
#             alice_group.addButton(button, j)
#             alice_group_layout.addWidget(button)
#         self.alice_group = alice_group

#         bob_group_layout = QVBoxLayout()
#         bob_group_layout.addWidget(QLabel("Bob"))
#         bob_group = QButtonGroup(self)
#         bob_group.buttonClicked.connect(self.set_projection_bob)
#         for j, proj in enumerate(('H', 'V', 'D', 'A', 'L', 'R')):
#             button = QRadioButton(proj)
#             button.proj = proj
#             bob_group.addButton(button, j)
#             bob_group_layout.addWidget(button)
#         self.bob_group = bob_group

#         analyzers_layout.addLayout(alice_group_layout)
#         analyzers_layout.addLayout(bob_group_layout)

#         layout.addLayout(analyzers_layout)
#         layout.addStretch()
#         self.setLayout(layout)

#     def set_projection_alice(self):
#         id = self.alice_group.checkedId()
#         proj = self.alice_group.button(id).proj
#         system.set_alice_projection(proj=proj)
#         return

#     def set_projection_bob(self):
#         id = self.bob_group.checkedId()
#         proj = self.bob_group.button(id).proj
#         system.set_bob_projection(proj=proj)
#         return


# class PlotOpticalPower(QWidget):

#     def __init__(self, parent, powermeter=None, ui_config=None):
#         super(QWidget, self).__init__(parent)
#         self.powermeter = powermeter
#         self.ui_config = ui_config

#         self.timer = QTimer(self)
#         self.timer.setInterval(ui_config['REFRESH_TIME'])  # in milliseconds
#         self.timer.start()
#         self.timer.timeout.connect(self.onNewData)

#         layout = QVBoxLayout()
#         # layout.setColumnStretch(1, 1)
#         # layout.setRowStretch(1, 1)

#         # add row of checkboxes to set pattern
#         self.count_value = QLabel(str(0))
#         self.count_value.setFont(QFont('Arial', ui_config["NUMERIC_FONT_SIZE"]))
#         layout.addWidget(self.count_value)

#         # plot initialization
#         self.plot = pg.PlotWidget()
#         self.plot.setLabel('left', 'Optical Power (mW)')
#         self.plot.time = [0]
#         self.plot.data = [0]
#         self.plot.getAxis('bottom').setTicks([])

#         YLIM = [0, 0.1]
#         self.ylim = YLIM

#         self.data = {'x': list(np.linspace(-10, 0, self.ui_config['NUMBER_POINTS_MEM'])),
#                      'y': list(np.zeros(self.ui_config['NUMBER_POINTS_MEM']))}
#         self.line = self.plot.plot(self.data['x'], self.data['y'], pen=mkPen(color=self.ui_config['COLORS'][1]))
#         layout.addWidget(self.plot)

#         self.setLayout(layout)

#     def onNewData(self):

#         new_count_value = self.powermeter.get_power() * 1000  # W -> mW

#         # set the label text to the current value
#         self.count_value.setText("Current power: {:.5f} mW".format(new_count_value))

#         # add the current count value to the plot
#         if new_count_value > self.ylim[1]:
#             self.ylim[1] = new_count_value
#         self.plot.setYRange(self.ylim[0], self.ylim[1])

#         # update with the most recent count value
#         self.update_array(self.data['y'], new_count_value, self.ui_config['NUMBER_POINTS_MEM'])
#         self.line.setData(self.data['x'], self.data['y'])
#         return

#     @staticmethod
#     def update_array(array, new_value, size):
#         array.append(new_value)
#         if len(array) >= size:
#             array.pop(0)
#         return


# class FileInputOuputPanel(QWidget):

#     def __init__(self, parent):
#         super(QWidget, self).__init__(parent)

#         layout = QVBoxLayout()
#         options = QHBoxLayout()
#         paths = QHBoxLayout()
#         layout.addWidget(QLabel("Save path:"))

#         self.default_top_path = QLineEdit(f"{IO.default_path}")
#         paths.addWidget(self.default_top_path)

#         self.parent_path = QLineEdit("data")
#         paths.addWidget(self.parent_path)

#         layout.addLayout(paths)

#         self.disable_paths = QCheckBox("Edit folder path")
#         self.disable_paths.toggled.connect(self.disable_path_edits)
#         options.addWidget(self.disable_paths)

#         self.include_date = QCheckBox("Include date?")
#         self.include_date.toggled.connect(self.update_io)
#         options.addWidget(self.include_date)

#         self.include_uuid = QCheckBox("Include unique ID?")
#         self.include_uuid.toggled.connect(self.update_io)

#         options.addWidget(self.include_uuid)
#         options.addStretch()

#         self.path = QLabel("")
#         layout.addWidget(self.path)

#         layout.addLayout(options)
#         layout.addStretch()
#         self.setLayout(layout)

#         # set the defaults of whether to include the date and/or unique ID string
#         # self.include_uuid.toggle()
#         self.include_date.toggle()

#     def update_io(self):
#         io = IO.create_new_save_folder(path=self.default_top_path.text(),
#                                        folder=self.parent_path.text(),
#                                        include_date=self.include_date.isChecked(),
#                                        include_uuid=self.include_uuid.isChecked(), )
#         self.path.setText(str(io.path))
#         print(str(io.path))
#         system.io = io
#         return

#     def disable_path_edits(self):
#         self.default_top_path.setEnabled(self.disable_paths.isChecked())
#         self.parent_path.setEnabled(self.disable_paths.isChecked())


if __name__ == '__main__':
    # from qoqi.interfaces.themes import palette

    app = QApplication(sys.argv)

    # custom_font = QFont()
    # custom_font.setWeight(18)
    # app.setFont(custom_font, "QLabel")
    # app.setStyleSheet("QLabel{font-size: 18pt;}")

    app.setStyle("Fusion")
    # app.setPalette(palette)

    main = LabInterfaceApp()
    main.show()
    sys.exit(app.exec())
