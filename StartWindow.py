import tkinter as tk
from LevelWindow import LevelWindow
from BlankWindow import BlankWindow

from GameWindow import GameWindow
from PIL import Image, ImageTk

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
    root_width = 850
    root_height = 750
    button_width = 30
    button_height = 7

    def __init__(self, root):
        self.root = root
        self.root.title("Igra memory")
        self.should_create_level_window = True

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        background_image_path = "background_image2.png"  # Replace with the path to your image file
        original_image = Image.open(background_image_path)
        # Resize the image to fit the Canvas
        resized_image = original_image.resize((self.root_width, self.root_height), Image.LANCZOS)

        # Convert the resized image to PhotoImage
        self.background_image = ImageTk.PhotoImage(resized_image)

        # Create a Canvas widget with the image dimensions
        self.canvas = tk.Canvas(root, width=self.root_width, height=self.root_height, bd=0, highlightthickness=0)
        self.canvas.place(x=0, y=0)  # Cover the entire window

        # Set the background image
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

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
        root.config(bg=self.root_color)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x = (screen_width - self.root_width) // 2
        y = (screen_height - self.root_height) // 2
        root.geometry(f"{self.root_width}x{self.root_height}+{x}+{y}")
        
        background_image_path = "background_image2.png"  # Replace with the path to your image file
        original_image = Image.open(background_image_path)

        # Resize the image to fit the window
        resized_image = original_image.resize((self.root_width, self.root_height), Image.LANCZOS)

        # Convert the resized image to PhotoImage
        self.background_image = ImageTk.PhotoImage(resized_image)

        # Create a Canvas widget with the image dimensions
        self.canvas = tk.Canvas(root, width=self.root_width, height=self.root_height, bd=0, highlightthickness=0)
        self.canvas.place(x=0, y=0)  # Cover the entire window

        # Set the background image
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

        game_window = GameWindow(root, columns=2, rows=2, title = "Game window")

        root.mainloop()  # Start the main loop for the new Tk instance

    def choose_level(self):
        self.root.destroy()
        # Check the flag before creating the level window
        if self.should_create_level_window:
            root = tk.Tk()
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            x = (screen_width - self.root_width) // 2
            y = (screen_height - self.root_height) // 2
            root.geometry(f"{self.root_width}x{self.root_height}+{x}+{y}")
        
            # Set the flag to False to prevent the small Tkinter window from appearing
            self.should_create_level_window = False

            # Create a new Toplevel window for level selection
            level_window = LevelWindow(root,title = "Level window")

            # Set the width and height of the level window
            

            # Add labels and buttons for level selection
            #label = tk.Label(level_window, text="Odaberi nivo:", font=self.label_font, bg=self.root_color)
            
            # Assuming you want levels from 1 to 5
            """for level in range(1, 6):
                level_button = tk.Button(level_window, text=f"Nivo {level}", command=lambda l=level: self.start_game_with_level(l), font=self.button_font, bg=self.choose_level_button_color, width=15, height=3)
                level_button.pack(side=tk.LEFT, padx=10)  # Pack buttons horizontally with some padding

            # Pack widgets to the level_window
            label.pack(pady=20)"""

            root.mainloop()


    def start_game_with_level(self, selected_level):
        # Create an instance of the BlankWindow class as a Toplevel window
        root = tk.Tk()

        # Assuming you want to pass the selected level to the GameWindow
        game_window = GameWindow(root, columns=4, rows=4, title=f"Game window - Level {selected_level}")

        root.mainloop()  # Start the main loop for the new Tk instance

        
        
        

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