import sys
from PyQt5.QtWidgets import QApplication
import content


app = QApplication(sys.argv)

# Create UI window instance from content.app
window = content.app.PressureScannerUI()


# Connect the UI window instance to scanner_functions
content.scanner_functions.ui_window = window

# Bind the buttons
window.start_btn.clicked.connect(content.scanner_functions.start_scan)


window.show()
sys.exit(app.exec_())
