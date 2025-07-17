# Franktorio scanner [main]
# Author: Franktorio
# May 6th 2025

import tkinter as tk
import os
import json

import objects
import app_gui
import scanner_functions


# Set-up Tkinter window
root = tk.Tk()
application = app_gui.FranktorioGUI(root, objects.global_vals.version)

root.mainloop()
