import tkinter as tk
from BlankWindow import BlankWindow

from GameWindow import GameWindow

import os
import time


class StartWindow:
    # Define fonts and colors
    root_color = "#2eb4c6"
    label_font = ("Helvetica", 16, "roman")
    start_button_color = "#49f86d"
    start_button_color_hover = "#02cf2c"
    choose_level_button_color = "#ee484c" 
    choose_level_button_color_hover = "#f2050b" 
    button_font = ("Comic Sans MS", 14, "roman bold")

    # define sizes
    root_width = 800
    root_height = 650
    button_width = 30
    button_height = 7

    def __init__(self, root):
        self.root = root
        self.root.title("Igra memory")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x = (screen_width - self.root_width) // 2
        y = (screen_height - self.root_height) // 2
        root.geometry(f"{self.root_width}x{self.root_height}+{x}+{y}")

        icon_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "icon.ico")
        self.root.iconbitmap(icon_path)

        self.root.config(bg=self.root_color)

        # Create labels and buttons
        label = tk.Label(root, text="Dobrodošli u igru memory!", font=self.label_font, bg=self.root_color)
        start_button = tk.Button(root, text="Započni igru", command=self.start_game, font=self.button_font, bg=self.start_button_color, width=self.button_width, height=self.button_height)
        choose_level_button = tk.Button(root, text="Odaberi nivo", command=self.choose_level, font=self.button_font, bg=self.choose_level_button_color, width=self.button_width, height=self.button_height)

        # Bind mouse events
        start_button.bind("<Enter>", lambda event, button=start_button: self.on_button_hover(event, button))
        choose_level_button.bind("<Enter>", lambda event, button=choose_level_button: self.on_button_hover(event, button))
        start_button.bind("<Leave>", lambda event: start_button.config(bg=self.start_button_color))
        choose_level_button.bind("<Leave>", lambda event: choose_level_button.config(bg=self.choose_level_button_color))

        # Pack widgets to the window
        label.pack(pady=30)
        start_button.pack(pady=20)
        choose_level_button.pack(pady=20)
        hover_start_time = 0

    def start_game(self):
        # Destroy the current window (StartWindow)
        self.root.destroy()

        # Create an instance of the BlankWindow class as a Toplevel window
        root = tk.Tk()
        root.config(bg="green")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x = (screen_width - self.root_width) // 2
        y = (screen_height - self.root_height) // 2
        root.geometry(f"{self.root_width}x{self.root_height}+{x}+{y}")
        
        game_window = GameWindow(root, columns=4, rows=4, title = "Game window")

        root.mainloop()  # Start the main loop for the new Tk instance

    def choose_level(self):
        print("Choose level")

    def on_button_hover(self, event, button):
        global hover_start_time
        hover_start_time = time.time()

        if button.cget('text') == "Započni igru":
            button.config(bg=self.start_button_color_hover)
        else:
            button.config(bg=self.choose_level_button_color_hover)

        self.check_hover(button)

    def check_hover(self, button):
        current_mouse_x = self.root.winfo_pointerx() - self.root.winfo_rootx()
        current_mouse_y = self.root.winfo_pointery() - self.root.winfo_rooty()
        
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
                self.delayed_function(button)
                return
        else:
            # Stop checking if the mouse is no longer over the button
            return
        
        button.after(100, lambda: self.check_hover(button))  # Check every 100 milliseconds


    def delayed_function(self, button):
        if button.cget('text') == "Započni igru":
            self.start_game()
        else:
            self.choose_level()