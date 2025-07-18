import os
import sys
import threading
from PyQt5.QtWidgets import QSystemTrayIcon
from PyQt5.QtGui import QIcon

ui_window = None
signals = None
cancel_scan = False

logs_folder = os.path.join(os.getenv("LOCALAPPDATA"), "Roblox", "logs")

tray_icon = None

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def init_tray_icon(app):
    global tray_icon
    if tray_icon is None:
        tray_icon = QSystemTrayIcon(app)
        icon_path = resource_path("content/FranktorioScannerIcon.ico")
        tray_icon.setIcon(QIcon(icon_path))
        tray_icon.setVisible(True)

def send_notification(title, message, timeout=5000):
    if tray_icon:
        tray_icon.showMessage(title, message, QSystemTrayIcon.Information, timeout)


def get_latest_log(logs_folder=logs_folder, return_file_name=False):
    latest_file_path = None
    latest_file = None

    for file in os.listdir(logs_folder):
        if not file.endswith(".log"):
            continue

        file_path = os.path.join(logs_folder, file)
        if latest_file is None or os.path.getmtime(latest_file_path) < os.path.getmtime(file_path):
            latest_file_path = file_path
            latest_file = file

    return (latest_file_path, latest_file) if return_file_name else latest_file_path


def start_scan():
    global cancel_scan
    if ui_window is None:
        return

    cancel_scan = False
    version = getattr(ui_window, "VERSION", "v?")

    ui_window.setWindowTitle(f"Franktorio's Research Scanner {version}: Real-Time Scanning")
    ui_window.add_console_line(f"Franktorio's Research Scanner {version}: Scanning Real-Time")

    ui_window.start_btn.setEnabled(False)
    ui_window.stop_btn.setEnabled(True)

    file_path, filename = get_latest_log(return_file_name=True)
    threading.Thread(target=stalk_real_time, args=(file_path, filename), daemon=True).start()


def stop_scan():
    global cancel_scan
    if ui_window is None:
        return

    cancel_scan = True
    ui_window.setWindowTitle("Franktorio's Research Scanner")
    if signals:
        signals.log_message.emit("Real-time scan stopped.")

    ui_window.start_btn.setEnabled(True)
    ui_window.stop_btn.setEnabled(False)


def stalk_real_time(file_path, filename):
    global cancel_scan

    try:
        while not cancel_scan:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                if signals:
                    signals.log_message.emit(f"Scanning {filename}")
                while not cancel_scan:
                    line = file.readline()
                    if line:
                        check_line(line)
                    else:
                        latest_path, latest_name = get_latest_log(return_file_name=True)
                        if latest_path != file_path:
                            file_path = latest_path
                            filename = latest_name
                            if signals:
                                signals.log_message.emit(f"New log file found.")
                            break
    except Exception as e:
        if signals:
            signals.log_message.emit(f"Error reading file: {e}")


def check_line(line):
    pass
