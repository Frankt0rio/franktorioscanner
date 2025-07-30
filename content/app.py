import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QTextEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QSizePolicy
)
from PyQt5.QtCore import Qt, QByteArray
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import pyqtSignal, QObject

RESIZE_MARGIN = 6

class UISignals(QObject):
    log_message = pyqtSignal(str)
    update_players_signal = pyqtSignal(int)
    update_server_location_signal = pyqtSignal(str)
    update_uptime_signal = pyqtSignal(int)

class SquareImageBox(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("No Image Loaded")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet(
            """
            background-color: #2a2a2a;
            border: 2px dashed #555;
            color: #777;
            border-radius: 8px;
            font-size: 16px;
            """
        )
        self.label.setScaledContents(True)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def setPixmap(self, pixmap):
        self.label.setPixmap(pixmap)
        if pixmap.isNull():
            self.label.setText("No Image Loaded")
        else:
            self.label.setText("")


class PressureScannerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("Franktorio's Research Scanner")
        self.resize(1200, 800)

        self.VERSION = "1.0.0"
        self.index = 0

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)


        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(35)
        self.title_bar.setStyleSheet("""
            background-color: #1e1e1e;
            border-bottom: 1px solid #444;
        """)
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(10, 0, 10, 0)
        title_layout.setSpacing(8)

        self.title_label = QLabel("  Franktorio's Research Scanner")
        self.title_label.setStyleSheet("color: #ccc; font-weight: bold; font-size: 14px;")
        self.title_label.setAlignment(Qt.AlignVCenter)

        self.min_btn = QPushButton("—")
        self.min_btn.setFixedSize(25, 25)
        self.min_btn.setStyleSheet("color: #ccc; background: transparent; border: none;")
        self.min_btn.clicked.connect(self.showMinimized)

        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(25, 25)
        self.close_btn.setStyleSheet("color: #ccc; background: transparent; border: none;")
        self.close_btn.clicked.connect(self.close)

        self.min_btn.setStyleSheet("""
            QPushButton {
                color: #ccc;
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QPushButton:pressed {
                background-color: #333;
            }
        """)

        self.close_btn.setStyleSheet("""
            QPushButton {
                color: #ccc;
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: red;
                color: white;
            }
            QPushButton:pressed {
                background-color: darkred;
            }
        """)


        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        title_layout.addWidget(self.min_btn)
        title_layout.addWidget(self.close_btn)


        self.content_widget = QWidget()
        grid = QGridLayout(self.content_widget)
        grid.setSpacing(12)

        self.base_timer_label = QLabel("Base Timer: 00:00")
        self.node_timer_label = QLabel("Node Timer: 00:00")
        timer_style = "font-size: 20px; font-weight: bold; color: #ddd;"
        self.base_timer_label.setStyleSheet(timer_style)
        self.node_timer_label.setStyleSheet(timer_style)

        self.server_info_container = QWidget()
        server_grid = QGridLayout()
        server_grid.setContentsMargins(10, 10, 10, 10)
        server_grid.setSpacing(10)

        label_style = "color: #aaa; font-weight: bold; font-size: 14px;"
        value_style = "color: #ccc; font-size: 14px;"

        players_label = QLabel("Players:")
        players_label.setStyleSheet(label_style)
        players_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.players_value = QLabel("N/A")
        self.players_value.setStyleSheet(value_style)
        self.players_value.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        server_label = QLabel("Server:")
        server_label.setStyleSheet(label_style)
        server_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.server_value = QLabel("Locating...")
        self.server_value.setStyleSheet(value_style)
        self.server_value.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        uptime_label = QLabel("Uptime:")
        uptime_label.setStyleSheet(label_style)
        uptime_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.uptime_value = QLabel("00:00:00")
        self.uptime_value.setStyleSheet(value_style)
        self.uptime_value.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        server_grid.addWidget(players_label, 0, 0)
        server_grid.addWidget(self.players_value, 0, 1)
        server_grid.addWidget(server_label, 1, 0)
        server_grid.addWidget(self.server_value, 1, 1)
        server_grid.addWidget(uptime_label, 2, 0)
        server_grid.addWidget(self.uptime_value, 2, 1)

        self.late_flicker_btn = QPushButton("Late Flicker")
        self.door_flicker_btn = QPushButton("Door Flicker")

        flicker_btn_style = """
            QPushButton {
                background-color: #444;
                color: #eee;
                border: 1.5px solid #666;
                border-radius: 6px;
                padding: 6px 16px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #555;
                border-color: #999;
            }
            QPushButton:pressed {
                background-color: #333;
            }
        """

        self.late_flicker_btn.setStyleSheet(flicker_btn_style)
        self.door_flicker_btn.setStyleSheet(flicker_btn_style)

        flicker_btn_layout = QHBoxLayout()
        flicker_btn_layout.setSpacing(10)
        flicker_btn_layout.addWidget(self.late_flicker_btn)
        flicker_btn_layout.addWidget(self.door_flicker_btn)

        server_grid.addLayout(flicker_btn_layout, 3, 0, 1, 2)
        server_grid.setColumnStretch(0, 0)
        server_grid.setColumnStretch(1, 1)

        self.server_info_container.setLayout(server_grid)
        self.server_info_container.setStyleSheet("""
            background-color: #2a2a2a;
            border: 1px solid #444;
            border-radius: 6px;
        """)

        left_top_container = QWidget()
        left_top_layout = QVBoxLayout()
        left_top_layout.setContentsMargins(10, 10, 10, 10)
        left_top_layout.setSpacing(12)
        left_top_layout.addWidget(self.base_timer_label)
        left_top_layout.addWidget(self.node_timer_label)
        left_top_layout.addWidget(self.server_info_container)
        left_top_container.setLayout(left_top_layout)
        left_top_container.setStyleSheet(
            "border: 1px solid #555; border-radius: 8px; background-color: #1e1e1e;"
        )

        grid.addWidget(left_top_container, 0, 0)

        self.console_log = QTextEdit()
        self.console_log.setReadOnly(True)
        self.console_log.setPlaceholderText("Console logs will appear here...")
        self.console_log.setStyleSheet("""
            background-color: #1e1e1e;
            color: #ddd;
            border: 1px solid #444;
            border-radius: 6px;
            padding: 8px;
            font-family: Consolas, monospace;
            font-size: 13px;
        """)
        grid.addWidget(self.console_log, 1, 0)

        self.start_btn = QPushButton("Start Scanner")
        self.stop_btn = QPushButton("Stop Scanner")
        button_style = """
            QPushButton {
                background-color: #333;
                color: #eee;
                border: 1.5px solid #555;
                border-radius: 6px;
                padding: 8px 18px;
                font-weight: bold;
            }
            QPushButton:hover:!disabled {
                background-color: #444;
                border-color: #888;
            }
            QPushButton:pressed:!disabled {
                background-color: #222;
            }
            QPushButton:disabled {
                background-color: #222;
                color: #666;
                border-color: #444;
            }
        """
        self.start_btn.setStyleSheet(button_style)
        
        self.stop_btn.setStyleSheet(button_style)
        self.stop_btn.setEnabled(False)


        left_buttons_layout = QHBoxLayout()
        left_buttons_layout.setSpacing(12)
        left_buttons_layout.addWidget(self.start_btn)
        left_buttons_layout.addWidget(self.stop_btn)
        left_buttons_container = QWidget()
        left_buttons_container.setLayout(left_buttons_layout)
        left_buttons_container.setStyleSheet("padding-top: 8px;")
        grid.addWidget(left_buttons_container, 2, 0)

        image_section_layout = QVBoxLayout()
        image_section_layout.setSpacing(8)
        image_section_layout.setContentsMargins(0, 0, 0, 0)

        self.room_name_label = QLabel("Room name: ")
        self.room_name_label.setAlignment(Qt.AlignCenter)
        self.room_name_label.setStyleSheet("color: #ccc; font-size: 16px; font-weight: bold;")
        image_section_layout.addWidget(self.room_name_label)


        self.image_grid_container = QWidget()
        image_grid_layout = QGridLayout()
        image_grid_layout.setSpacing(8)
        image_grid_layout.setContentsMargins(0, 0, 0, 0)

        self.image_boxes = []
        for r in range(2):
            for c in range(2):
                box = SquareImageBox()
                box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.image_boxes.append(box)
                image_grid_layout.addWidget(box, r, c)

        self.image_grid_container.setLayout(image_grid_layout)
        self.image_grid_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_grid_container.setStyleSheet(
            "background-color: #2a2a2a; border-radius: 8px; border: 2px solid #444;"
        )

        image_section_layout.addWidget(self.image_grid_container)

        image_section_widget = QWidget()
        image_section_widget.setLayout(image_section_layout)
        grid.addWidget(image_section_widget, 0, 1)


        self.notes_box = QTextEdit()
        self.notes_box.setPlaceholderText("Notes about the image...")
        self.notes_box.setStyleSheet("""
            background-color: #1e1e1e;
            color: #ddd;
            border: 1px solid #444;
            border-radius: 6px;
            padding: 8px;
            font-size: 14px;
        """)
        grid.addWidget(self.notes_box, 1, 1)

        self.notifications_btn = QPushButton("Notifications: ON")
        self.notifications_btn.setCheckable(True)
        self.notifications_btn.setChecked(True)
        self.see_info_btn = QPushButton("See Info")

        self.notifications_btn.setStyleSheet(button_style)
        self.see_info_btn.setStyleSheet(button_style)

        right_buttons_layout = QHBoxLayout()
        right_buttons_layout.setSpacing(10)
        right_buttons_layout.addWidget(self.notifications_btn)
        right_buttons_layout.addWidget(self.see_info_btn)

        right_buttons_container = QWidget()
        right_buttons_container.setLayout(right_buttons_layout)
        right_buttons_container.setStyleSheet("padding-top: 8px;")
        grid.addWidget(right_buttons_container, 2, 1)

        grid.setRowStretch(0, 4)
        grid.setRowStretch(1, 2)
        grid.setRowStretch(2, 0)
        grid.setColumnStretch(0, 2)
        grid.setColumnStretch(1, 3)

        self.setLayout(grid)
        self.setStyleSheet("background-color: #121212;")

        self.notifications_btn.toggled.connect(self.toggle_notifications)

        main_layout.addWidget(self.title_bar)
        main_layout.addWidget(self.content_widget)
        self.setLayout(main_layout)


    def toggle_notifications(self, checked):
        self.notifications_btn.setText("Notifications: ON" if checked else "Notifications: OFF")

    def update_base_timer(self, seconds: int):
        minutes = seconds // 60
        secs = seconds % 60
        self.base_timer_label.setText(f"Base Timer: {minutes:02}:{secs:02}")

    def update_node_timer(self, seconds: int):
        minutes = seconds // 60
        secs = seconds % 60
        self.node_timer_label.setText(f"Node Timer: {minutes:02}:{secs:02}")

    def update_uptime(self, seconds: int):
        hrs = seconds // 3600
        mins = (seconds % 3600) // 60
        secs = seconds % 60
        self.uptime_value.setText(f"{hrs:02}:{mins:02}:{secs:02}")

    def update_players(self, count: int):
        self.players_value.setText(str(count))

    def update_server_location(self, location: str):
        self.server_value.setText(location)

    def add_console_line(self, message: str):
        self.console_log.append(f"[{self.index:03}] {message}")
        self.index += 1

    def update_room_title(self, name: str):
        self.room_name_label.setText(f"Room name: {name}")

    def update_image_text(self, index: int, text: str):
        if 0 <= index < len(self.image_boxes):
            self.image_boxes[index].label.setText(text)

    def update_image_from_url(self, index: int, url: str):
        if not (0 <= index < len(self.image_boxes)):
            return

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            image_data = response.content

            image = QImage()
            if not image.loadFromData(QByteArray(image_data)):
                self.image_boxes[index].label.setText("No Image Loaded")
                self.image_boxes[index].label.setPixmap(QPixmap())
                return

            pixmap = QPixmap.fromImage(image)
            self.image_boxes[index].setPixmap(pixmap)
        except Exception as e:
            self.image_boxes[index].label.setText("No Image Loaded")
            self.image_boxes[index].label.setPixmap(QPixmap())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.title_bar.geometry().contains(event.pos()):
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and hasattr(self, 'drag_position'):
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def pop_out(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.show()
        self.raise_()
        self.activateWindow()

    def normal_window(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.show()

