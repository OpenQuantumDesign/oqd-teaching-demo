
ui_config = dict(
    # settings for the main window(s)
    WIDTH=1024,
    HEIGHT=600,
    COLORS=["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"],
    PLOT_BACKGROUND="#E6E6EA",
    PLOT_FOREGROUND="#434A42",
    # LOGO_PATH=str(pathlib.Path(__file__).parent.parent.parent.joinpath(r'qoqi\interfaces\themes').joinpath('iqc.png')),
)





dark_mode_style_sheet = """
/* Set the background color for the main window */
QWidget {
    background-color: #333333;
}

/* Set the font and text color for all widgets */
* {
    font-family: Arial, sans-serif;
    color: #ffffff;
}

/* Set the style for QPushButton */
QPushButton {
    padding: 8px 16px;
    border: none;
    background-color: #4CAF50;
    color: #ffffff;
    border-radius: 5px;
}

QPushButton:hover {
    background-color: #45a049;
}

QPushButton:pressed {
    background-color: #3d8b3d;
}

/* Set the style for QLineEdit */
QLineEdit {
    padding: 6px;
    border: 1px solid #888888;
    border-radius: 5px;
}

/* Set the style for QComboBox */
QComboBox {
    padding: 6px;
    border: 1px solid #888888;
    border-radius: 5px;
}

/* Set the style for QSpinBox and QDoubleSpinBox */
QSpinBox,
QDoubleSpinBox {
    padding: 6px;
    border: 1px solid #888888;
    border-radius: 5px;
}

/* Set the style for QCheckBox and QRadioButton */
QCheckBox,
QRadioButton {
    spacing: 2px;
}

/* Set the style for QProgressBar */
QProgressBar {
    text-align: center;
}

QProgressBar::chunk {
    background-color: #4CAF50;
}

/* Set the style for QSlider */
QSlider::groove:horizontal {
    height: 6px;
    border-radius: 3px;
    background-color: #888888;
}

QSlider::handle:horizontal {
    width: 14px;
    margin: -4px 0;
    border-radius: 7px;
    background-color: #4CAF50;
}

/* Set the style for QTabWidget */
QTabWidget::pane {
    border: 1px solid #888888;
    border-radius: 5px;
}

QTabWidget::tab-bar {
    left: 5px; /* move the tabs to the right */
}

QTabBar::tab {
    padding: 8px 16px;
    border: 1px solid #888888;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
}

QTabBar::tab:selected {
    background-color: #4CAF50;
    color: #ffffff;
}

/* Set the style for QListView and QTreeView */
QListView,
QTreeView {
    border: 1px solid #888888;
    border-radius: 5px;
    background-color: #444444;
    show-decoration-selected: 1; /* show the selection in QListWidget and QTreeWidget */
}

QListView::item:selected,
QTreeView::item:selected {
    background-color: #4CAF50;
    color: #ffffff;
}

/* Set the style for QMenuBar and QMenu */
QMenuBar,
QMenu {
    background-color: #333333;
}

QMenuBar::item {
    padding: 6px 12px;
}

QMenu::item {
    padding: 8px 24px;
}

QMenu::item:selected {
    background-color: #4CAF50;
    color: #ffffff;
}
"""