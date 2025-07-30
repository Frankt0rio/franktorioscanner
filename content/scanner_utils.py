import os
import sys
import threading
from . import server_utils

from PyQt5.QtWidgets import QSystemTrayIcon
from PyQt5.QtGui import QIcon

ui_window = None
signals = None

logs_folder = os.path.join(os.getenv("LOCALAPPDATA"), "Roblox", "logs")

tray_icon = None


cancel_scan = False
players = 0
uptime = 0

server_location = ""
client_disconnected = False



def resource_path(relative_path):
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
        icon_path = resource_path("content/FranktorioScannerIcon.ico")
        icon = QIcon(icon_path)
        tray_icon.setIcon(icon)
        tray_icon.showMessage(title, message, icon, timeout)


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
    global cancel_scan, players, uptime, server_location, client_disconnected
    if ui_window is None:
        return

    cancel_scan = True
    players = 0
    uptime = 0
    server_location = ""
    client_disconnected = False
    
    ui_window.setWindowTitle("Franktorio's Research Scanner")
    if signals:
        signals.log_message.emit("Real-time scan stopped.")
        signals.update_players_signal.emit(players)
        signals.update_server_location_signal.emit(server_location)

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


def update_server_info():
    if signals:
        signals.update_players_signal.emit(players)
        signals.update_server_location_signal.emit(server_location)

def check_line(line):
    global players, uptime, server_location, client_disconnected


    if not hasattr(check_line, 'disconnect_buffer'):
        check_line.disconnect_buffer = []
        check_line.buffer_timer = None

    u_line = line.lower()

    if "player added" in u_line:
        players += 1
        update_server_info()
        if signals:
            signals.log_message.emit(f"Player joined: {line.split()[-2]}, ID: {line.split()[-1]}")

    elif "player removed" in u_line:
        players -= 1
        update_server_info()
        check_line.disconnect_buffer.append(line.split()[-2])
        if signals:
            signals.log_message.emit(f"Player left: {line.split()[-2]}, ID: {line.split()[-1]}")

        if check_line.buffer_timer:
            check_line.buffer_timer.cancel()

        def send_buffered_notification():
            count = len(check_line.disconnect_buffer)
            if count == 1:
                message = f"Player left: {check_line.disconnect_buffer[0]}"
            else:
                message = f"{count} players disconnected"
            send_notification(title="Franktorio's Research Scanner", message=message)
            check_line.disconnect_buffer.clear()

        check_line.buffer_timer = threading.Timer(3.0, send_buffered_notification)
        check_line.buffer_timer.start()

    if "target player" in u_line:
        player_name = line.split()[-3]
        if signals:
            signals.log_message.emit(f"Player {player_name} got in void locker.")
        send_notification("Franktorio Scanner", f"Player {player_name} got in void locker.")

    if "[flog::network] client:disconnect" in u_line:
        if not client_disconnected:
            players = 0
            uptime = 0
            server_location = "Locating..."
            if ui_window:
                ui_window.late_flicker_btn.setEnabled(False)
                ui_window.door_flicker_btn.setEnabled(False)
            client_disconnected = True
            update_server_info()
            signals.log_message.emit("Client disconnected.")
        else:
            client_disconnected = False
    
    if "udmux address" in u_line:
        server_inf = server_utils.get_server_location_from_log(u_line)
        if server_inf:
            server_location = server_inf
            update_server_info()
            signals.log_message.emit(server_location)
        else:
            signals.log_message.emit("Failed to retrieve server location.")


