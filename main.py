import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
import content

app = QApplication(sys.argv)

# Set window icon
app_icon = QIcon("content/FranktorioScannerIcon.ico")
app.setWindowIcon(app_icon)

# Initialize tray icon
content.scanner_utils.init_tray_icon(app)

# Create UI window instance
window = content.app.PressureScannerUI()

# Create signal instance and connect it to UI
signals = content.app.UISignals()
signals.log_message.connect(window.add_console_line)

# Pass them to scanner_utils
content.scanner_utils.ui_window = window
content.scanner_utils.signals = signals

# Bind the buttons
window.start_btn.clicked.connect(content.scanner_utils.start_scan)
window.stop_btn.clicked.connect(content.scanner_utils.stop_scan)

window.show()
sys.exit(app.exec_())
