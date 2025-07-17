# Franktorio scanner [app gui]
# Author: Franktorio
# May 6th 2025



import tkinter as tk
from tkinter import ttk
import sv_ttk


PADX = 5
BTN_WIDTH = 14



class FranktorioGUI:
    def __init__(self, root, version="1.0"):
        self.root = root
        self.version = version
        # Initialize line counters
        self._timer_snapshot_count = 0
        self._console_log_count = 0
        self._room_log_count = 0
        self._setup_window()
        self._setup_widgets()
        sv_ttk.use_dark_theme()

    def _setup_window(self):
        self.root.title(f"Franktorio's Pressure Scanner {self.version}: Idle")
        self.root.columnconfigure(0, weight=1, minsize=50)
        self.root.columnconfigure(1, weight=2, minsize=50)
        self.root.rowconfigure(0, weight=1, minsize=150)
        self.root.rowconfigure(1, weight=2)
        self.root.rowconfigure(2, weight=0)

    def _setup_widgets(self):
        # Node Timer Frame
        self.node_timer_frame = ttk.LabelFrame(self.root, text="Node Timer")
        self.node_timer_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.node_timer_frame.columnconfigure(0, weight=1)
        self.node_timer_frame.rowconfigure(1, weight=1)

        # Timer Labels
        self.azr_timer_label = ttk.Label(self.node_timer_frame, text="Node-Timer: -:--", font=("Consolas", 20))
        self.azr_timer_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.don_timer_label = ttk.Label(self.node_timer_frame, text="Frequency: -:--", font=("Consolas", 20))
        self.don_timer_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        # Frame to hold Timer Logs and Server Info side-by-side
        self.additional_timer_frame = ttk.Frame(self.node_timer_frame)
        self.additional_timer_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.additional_timer_frame.columnconfigure(0, weight=1)
        self.additional_timer_frame.columnconfigure(1, weight=1)
        self.additional_timer_frame.rowconfigure(0, weight=1)

        # Timer Logs
        self.timer_snapshots_frame = ttk.LabelFrame(self.additional_timer_frame, text="Timer Logs", padding=(10,5))
        self.timer_snapshots_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.timer_snapshots_frame.columnconfigure(0, weight=1)
        self.timer_snapshots_frame.rowconfigure(0, weight=1)

        self.timer_snapshots_text = tk.Text(self.timer_snapshots_frame, wrap="word", font=("Consolas",10))
        self.timer_snapshots_text.grid(row=0, column=0, sticky="nsew")
        self.timer_snapshots_scroll = ttk.Scrollbar(self.timer_snapshots_frame, command=self.timer_snapshots_text.yview)
        self.timer_snapshots_scroll.grid(row=0, column=1, sticky="ns")
        self.timer_snapshots_text.config(yscrollcommand=self.timer_snapshots_scroll.set)

        # Server Info Panel (always visible)
        self.server_info_frame = ttk.LabelFrame(self.additional_timer_frame, text="Server Info", padding=(10,5))
        self.server_info_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.server_info_frame.columnconfigure(0, weight=1)
        self.server_info_frame.rowconfigure((0,1,2), weight=1)

        self.server_name_label = ttk.Label(self.server_info_frame, text="Server:\nN/A\nN/A\nN/A", font=("Consolas", 14))
        self.server_name_label.grid(row=0, column=0, sticky="w", pady=2, padx=5)
        self.player_count_label = ttk.Label(self.server_info_frame, text="Players: 0", font=("Consolas", 14))
        self.player_count_label.grid(row=1, column=0, sticky="w", pady=2, padx=5)
        self.uptime_label = ttk.Label(self.server_info_frame, text="Uptime: 0h 0m", font=("Consolas", 14))
        self.uptime_label.grid(row=2, column=0, sticky="w", pady=2, padx=5)

        # Timer Controls
        self.timer_controls_frame = ttk.Frame(self.node_timer_frame)
        self.timer_controls_frame.grid(row=2, column=0, pady=5, padx=5, sticky="w")
        self.timer_controls_frame2 = ttk.Frame(self.node_timer_frame)
        self.timer_controls_frame2.grid(row=3, column=0, pady=5, padx=5, sticky="w")

        # Flicker Buttons
        self.flicker_documenting_ctrls = ttk.Frame(self.node_timer_frame)
        self.flicker_documenting_ctrls.grid(row=2, column=0, pady=5, padx=(0,30), sticky="e")
        self.late_flicker_btn = ttk.Button(self.flicker_documenting_ctrls, text="Late flicker", state=tk.DISABLED, width=BTN_WIDTH)
        self.late_flicker_btn.grid(row=2, column=0, padx=PADX)
        self.normal_flicker_btn = ttk.Button(self.flicker_documenting_ctrls, text="Normal flicker", state=tk.DISABLED, width=BTN_WIDTH)
        self.normal_flicker_btn.grid(row=2, column=1, padx=PADX)

        # Node Timer Adjustment
        self.reset_timer_btn = ttk.Button(self.timer_controls_frame, text="Reset Node-timer", width=BTN_WIDTH)
        self.reset_timer_btn.grid(row=2, column=0, padx=PADX)
        self.pop_timers_btn = ttk.Button(self.timer_controls_frame, text="Pop-out timers", width=BTN_WIDTH)
        self.pop_timers_btn.grid(row=2, column=1, padx=PADX)

        self.log_first_late_btn = ttk.Button(self.timer_controls_frame2, text="First Late-Flicker", state=tk.DISABLED, width=BTN_WIDTH)
        self.log_first_late_btn.grid(row=3, column=0, padx=PADX)
        self.add_minute_btn = ttk.Button(self.timer_controls_frame2, text="+1 minute", state=tk.DISABLED, width=BTN_WIDTH)
        self.add_minute_btn.grid(row=3, column=1, padx=PADX)
        self.remove_minute_btn = ttk.Button(self.timer_controls_frame2, text="-1 minute", state=tk.DISABLED, width=BTN_WIDTH)
        self.remove_minute_btn.grid(row=3, column=2, padx=PADX)

        # Other Console Logs
        self.other_console_logs_frame = ttk.LabelFrame(self.root, text="Other Console Logs")
        self.other_console_logs_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0,10))
        self.other_console_logs_frame.columnconfigure(0, weight=1)
        self.other_console_logs_frame.rowconfigure(0, weight=1)
        self.other_console_logs = tk.Text(self.other_console_logs_frame, wrap="word")
        self.other_console_logs.grid(row=0, column=0, sticky="nsew")
        self.other_console_scroll = ttk.Scrollbar(self.other_console_logs_frame, command=self.other_console_logs.yview)
        self.other_console_scroll.grid(row=0, column=1, sticky="ns")
        self.other_console_logs.config(yscrollcommand=self.other_console_scroll.set)

        # Room Logs
        self.room_log_frame = ttk.LabelFrame(self.root, text="Room Logs")
        self.room_log_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=(0,10), pady=10)
        self.room_log_frame.columnconfigure(0, weight=1)
        self.room_log_frame.rowconfigure(0, weight=1)
        self.room_log_text = tk.Text(self.room_log_frame, wrap="word")
        self.room_log_text.grid(row=0, column=0, sticky="nsew")
        self.room_log_scroll = ttk.Scrollbar(self.room_log_frame, command=self.room_log_text.yview)
        self.room_log_scroll.grid(row=0, column=1, sticky="ns")
        self.room_log_text.config(yscrollcommand=self.room_log_scroll.set)

        # Bottom Buttons
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.grid(row=2, column=0, columnspan=2, pady=(0,10), padx=50)
        self.start_rt_btn = ttk.Button(self.button_frame, text="Real-Time Scan", width=BTN_WIDTH)
        self.stop_btn = ttk.Button(self.button_frame, text="Stop Scanner", state=tk.DISABLED, width=BTN_WIDTH)
        self.scan_all_btn = ttk.Button(self.button_frame, text="Scan Every Log", width=BTN_WIDTH)
        self.toggle_notifs_btn = ttk.Button(self.button_frame, text="Notifications: True", width=BTN_WIDTH)
        self.clear_btn = ttk.Button(self.button_frame, text="Clear", width=BTN_WIDTH, command=self._clear_all)
        self.start_rt_btn.grid(row=0, column=0, padx=PADX)
        self.stop_btn.grid(row=0, column=1, padx=PADX)
        self.scan_all_btn.grid(row=0, column=2, padx=PADX)
        self.toggle_notifs_btn.grid(row=0, column=3, padx=PADX)
        self.clear_btn.grid(row=0, column=4, padx=PADX)

    def bind_actions(self,
                     start_rt=None,
                     stop=None,
                     scan_all=None,
                     toggle_notifs=None,
                     pop_timers=None,
                     reset_timer=None,
                     log_first_late=None,
                     add_minute=None,
                     remove_minute=None,
                     late_flicker=None,
                     normal_flicker=None):
        
        if start_rt: self.start_rt_btn.config(command=start_rt)
        if stop: self.stop_btn.config(command=stop)
        if scan_all: self.scan_all_btn.config(command=scan_all)
        if toggle_notifs: self.toggle_notifs_btn.config(command=toggle_notifs)
        if pop_timers: self.pop_timers_btn.config(command=pop_timers)
        if reset_timer: self.reset_timer_btn.config(command=reset_timer)
        if log_first_late: self.log_first_late_btn.config(command=log_first_late)
        if add_minute: self.add_minute_btn.config(command=add_minute)
        if remove_minute: self.remove_minute_btn.config(command=remove_minute)
        if late_flicker: self.late_flicker_btn.config(command=late_flicker)
        if normal_flicker: self.normal_flicker_btn.config(command=normal_flicker)

    # Private clear-all
    def _clear_all(self):
        """Clears all three log areas and resets their counters."""
        self.clear_timer_snapshots()
        self.clear_console()
        self.clear_room_logs()

    # Timer update methods
    def update_node_timer(self, minutes, seconds):
        """Updates the node timer label."""
        self.azr_timer_label.config(text=f"Node-Timer: {minutes}:{seconds:02d}")

    def update_frequency(self, minutes, seconds):
        """Updates the frequency timer label."""
        self.don_timer_label.config(text=f"Frequency: {minutes}:{seconds:02d}")
    
    # Server information updating methods
    def update_server_location(self, server_location):
        """Updates the server location label"""
        self.server_name_label.config(text=f"Server: {server_location}")
    
    def update_player_count(self, player_count):
        """Updates the player count label."""
        self.player_count_label.config(text=f"Players: {player_count}")
    
    def update_uptime(self, uptime):
        """Updates the uptime label."""
        self.uptime_label.config(text=f"Uptime: {uptime}")

    # Update methods with line counters
    def log_timer_snapshot(self, text):
        """Logs a timer snapshot with a line counter."""
        self._timer_snapshot_count += 1
        prefix = f"[{self._timer_snapshot_count:04d}] "
        self.timer_snapshots_text.insert(tk.END, prefix + text + "\n")
        self.timer_snapshots_text.see(tk.END)

    def clear_timer_logs(self):
        """Removes all the text in the timer logs"""
        self._timer_snapshot_count = 0
        self.timer_snapshots_text.delete("1.0", tk.END)

    def add_console_log(self, text):
        """Adds a log in the console logs"""
        self._console_log_count += 1
        prefix = f"[{self._console_log_count:04d}] "
        self.other_console_logs.insert(tk.END, prefix + text + "\n")
        self.other_console_logs.see(tk.END)

    def clear_console_logs(self):
        """Removes all the text in the console logs"""
        self._console_log_count = 0
        self.other_console_logs.delete("1.0", tk.END)

    def add_room_log(self, text):
        """Adds a log in the room logs"""
        self._room_log_count += 1
        prefix = f"[{self._room_log_count:04d}] "
        self.room_log_text.insert(tk.END, prefix + text + "\n")
        self.room_log_text.see(tk.END)

    def clear_room_logs(self):
        """Removes all the text in the room logs"""
        self._room_log_count = 0
        self.room_log_text.delete("1.0", tk.END)
