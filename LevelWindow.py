import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from GameWindow import GameWindow
import random
import os
import time


class LevelWindow:
    image_height = 152
    image_width = 109
    button_width = 15
    button_height = 3
    button_font = ("Comic Sans MS", 12, "roman")
    button_color = "#ee484c" 
    button_color_hover = "#f2050b" 
    window_color = "#2eb4c6"
    def __init__(self, master,title):

        self.master = master
        master.geometry("920x600")
        master.title(title)
        master.config(bg=self.window_color)
        polje = ["3x2", "3x3", "4x2", "4x3", "4x4"]
        for i in range(0, 5):
            rows, cols = polje[i].split("x")
            level_button = tk.Button(master, text=f"Level {polje[i]}", command = lambda rows = rows, cols = cols: self.start_game(rows, cols), font=self.button_font, bg=self.button_color, width=self.button_width, height=self.button_height)
            level_button.pack(side=tk.LEFT, padx=10)
            # Bind mouse events
            level_button.bind("<Enter>", lambda event, button=level_button, rows = rows, cols = cols: self.on_button_hover(event, button, rows, cols))
            level_button.bind("<Leave>", lambda event: level_button.config(bg=self.button_color))

    def start_game(self, rows, cols):
        # Destroy the current window (StartWindow)
        self.master.destroy()
        print(rows, cols)

        # Create an instance of the BlankWindow class as a Toplevel window
        root = tk.Tk()

        game_window = GameWindow(root, columns=4, rows=4,title = "Game window")

        root.mainloop()  # Start the main loop for the new Tk instance


    def on_button_hover(self, event, button, rows, cols):
        global hover_start_time
        hover_start_time = time.time()

        self.check_hover(button, rows, cols)

    def check_hover(self, button, rows, cols):
        current_mouse_x = self.master.winfo_pointerx() - self.master.winfo_rootx()
        current_mouse_y = self.master.winfo_pointery() - self.master.winfo_rooty()
        
        button_x, button_y = button.winfo_geometry().split('+')[1:]
        button_x, button_y = int(button_x), int(button_y)

        button_width = button.winfo_reqwidth()
        button_height = button.winfo_reqheight()

        if (
            button_x <= current_mouse_x <= button_x + button_width and
            button_y <= current_mouse_y <= button_y + button_height
        ):
            elapsed_time = time.time() - hover_start_time
            if elapsed_time >= 1:  # 1 second
                self.start_game(rows, cols)
                return
        else:
            # Stop checking if the mouse is no longer over the button
            return
        
        button.after(100, lambda: self.check_hover(button, rows, cols))  # Check every 100 milliseconds