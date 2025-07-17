# Franktorio scanner [objects]
# Author: Franktorio
# May 6th 2025

import time
import sys
import os
import json


class GlobalValues:
    """
    Keeps track of these values everywhere where they are needed
    """
    def __init__(self):
        # Get file paths to user data
        SCRIPT_DIR = self._get_script_dir()
        SCANNER_LOGS = os.path.join(SCRIPT_DIR, "franktorio_rooms1.json")
        FRANKTORIO_SCANNER_USER = os.path.join(SCRIPT_DIR, "franktorio_scanner_user_data.json")


        # Make a file for room, flicker and scanned logs
        if os.path.exists(SCANNER_LOGS):
            with open(SCANNER_LOGS, "r") as data:
                self.scanner_logs = json.load(data)
        else:
            self.scanner_logs = {
                "scanned_files": [],
                "logged_rooms": {},
                "flicker_logs": []
            }


        # Make a file that has user data
        if os.path.exists(FRANKTORIO_SCANNER_USER):
            with open(FRANKTORIO_SCANNER_USER, "r") as data:
                self.user_data = json.load(data)
        else:
            self.user_data = {
                "username": None,
                "password": None
            }
        

        self.run_id = 0
        if len(self.scanner_logs["flicker_logs"]) > 0:
            self.run_id = self.scanner_logs["flicker_logs"][-1]["RunID"]
        

        self.logs_folder = os.path.join(os.getenv("LOCALAPPDATA"), "Roblox", "logs")

        
        # Initialize constant variables
        self.VERSION = "2.0.0"
        self.SKIPPED_ROOMS = ["start", "room100", "1ridgestart"]
        self.DISCONNECT_NOTIFS_COOLDOWN = 5
        self.MAX_LATEST_ROOMS = 5

        # Initialize game data
        self.latest_rooms = [None]

        # Initialize scanner settings
        self.send_notifications = True

        # Initialize server information variables
        self.time_connected = "N/A"
        self.player_count = "N/A"
        self.server_ip = "N/A"
        
        self.disconnections = []

        # Temporal timers
        self.last_disconnect_notify = 0
    
    def _get_script_dir():
        """Gets the working directory of the program"""
        if getattr(sys, 'frozen', False):
            # PyInstaller: use the directory of the .exe
            return os.path.dirname(sys.executable)
        else:
            # Normal script mode
            return os.path.dirname(os.path.abspath(__file__))
    
global_vals = GlobalValues()



class Timers:
    """
    Makes a timer object that contains multiple timers

    Node-Timer: Starts after door 1 is opened, increased by 24 every door that opens
    In-game timer: Starts after door 1 is opened, doesnt change until end of run
    Don's timer: Start at door 19, increases by 24 by every door opened and stops when the first late flicker happens

    Temp-timer: Used for cooldowns
    """

    def __init__(self):

        # Initialize timer variables
        self.node_timer = None # None as these only begin at specific points
        self.in_game_timer = None
        self.dons_timer = None

        # Variable that keeps track if it has late flickered or not
        self.late_flickered = False

        self.temp_timer = time.perf_counter() # Timer used to standardize the increment of the timers


    def update(self):
        """
        Updates the timers, takes doors as an argument to increase the times without affecting the real variable

        Returns nothing
        """

        # Increase all timers by one second if one second has passed
        if time.perf_counter() - self.temp_timer > 1:

            if self.in_game_timer != None:
                self.in_game_timer += 1
            
            if self.node_timer != None:
                self.node_timer += 1
            
            if self.dons_timer != None and not self.late_flickered:
                self.dons_timer += 1
            
            # Reset temporal timer
            self.temp_timer = time.perf_counter()

    
    def start_node_timer(self):
        """Makes the node timer int 0 instead of None"""

        if self.node_timer == None:
            self.node_timer = 0

    
    def start_ingame_timer(self):
        """Makes the ingame timer int 0 instead of None"""

        if self.in_game_timer == None:
            self.in_game_timer = 0
    

    def start_dons_timer(self):
        """Makes the dons timer int 0 instead of None"""

        if self.dons_timer == None:
            self.dons_timer = 0
    

    def door_opened(self):
        """
        Called when a door opens, increases the node timer by 24

        Returns nothing
        """

        if self.node_timer != None:
            self.node_timer += 24

        if self.dons_timer != None and not self.late_flickered:
            self.dons_timer += 24


    def reset(self):
        """
        Resets the timers to None

        Returns nothing
        """

        self.node_timer = None
        self.in_game_timer = None
        self.dons_timer = None

        self.late_flickered = False

    
    def mins_secs(self, seconds):
        """
        Turns the seconds into minutes and seconds

        E.g.
        int 96 -> str 1:36
        """

        converted_minutes = seconds // 60
        converted_seconds = seconds % 60


        return f"{converted_minutes}:{converted_seconds:02}"
