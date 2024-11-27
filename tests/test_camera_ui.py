from PyQt5.QtWidgets import QApplication
from picamera2.previews.qt import QGlPicamera2
from picamera2 import Picamera2

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration())
app = QApplication([])
qpicamera2 = QGlPicamera2(picam2, width=800, height=600, keep_ar=False)
qpicamera2.setWindowTitle("Qt Picamera2 App")
picam2.start()
qpicamera2.show()
app.exec()