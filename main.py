import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
import content

base_dir = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(base_dir, "content", "FranktorioScannerIcon.ico")

app = QApplication(sys.argv)
app.setApplicationName("Franktorio Scanner")
app.setApplicationDisplayName("Franktorio Scanner")

app_icon = QIcon(icon_path)
app.setWindowIcon(app_icon)

content.scanner_utils.init_tray_icon(app)

window = content.app.PressureScannerUI()

window.setWindowIcon(app_icon)

signals = content.app.UISignals()
signals.log_message.connect(window.add_console_line)
signals.update_players_signal.connect(window.update_players)
signals.update_server_location_signal.connect(window.update_server_location)
signals.update_uptime_signal.connect(window.update_uptime)

content.scanner_utils.ui_window = window
content.scanner_utils.signals = signals

window.start_btn.clicked.connect(content.scanner_utils.start_scan)
window.stop_btn.clicked.connect(content.scanner_utils.stop_scan)

window.show()

sys.exit(app.exec_())
