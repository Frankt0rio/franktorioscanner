# Franktorio scanner [scanner]
# Author: Franktorio
# May 6th 2025

import subprocess
import sys
import os
from objects import global_vals

# Install plyer if it's not installed yet
try:
    import plyer
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "plyer"])
    import plyer  # Try again after installing


def get_script_dir():
    """Gets the working directory of the program"""
    if getattr(sys, 'frozen', False):
        # PyInstaller: use the directory of the .exe
        return os.path.dirname(sys.executable)
    else:
        # Normal script mode
        return os.path.dirname(os.path.abspath(__file__))
    

def send_notification(text):
    """Sends a notification with the text given."""
    if global_vals.send_notifications:
        plyer.notification.notify(
            title = f"=== Franktorio's Pressure Scanner {global_vals.version} ===",
            message = text,
            app_icon = None,
            timeout = 1,
        )


def get_latest_log(logs_folder=global_vals.logs_folder, return_file_name=False):
    """
    Retrieves the latest modified log file in the given folder
    Args:
        (str) logs_folder: File path to a folder
        (bool) return_file_name: Whether to return the file name or just the file path
    
    returns a file path or a tuple of (file_path, file_name)
    """
    latest_file_path = None
    latest_file = None

    for file in os.listdir(logs_folder):
        if not file.endswith(".log"):
            continue  # Skip non-log files

        file_path = os.path.join(logs_folder, file)

        # Compare modification times to find the latest file
        if latest_file is None or os.path.getmtime(latest_file_path) < os.path.getmtime(file_path):
            latest_file_path = file_path
            latest_file = file

    return (latest_file_path, latest_file) if return_file_name else latest_file_path


