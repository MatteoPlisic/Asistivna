import tkinter as tk
import time
import random

class BlankWindow:
    def __init__(self, root, title="Blank Window", width=400, height=300):
        self.root = root
        self.root.title(title)

        # Set window size and position
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")

        # Create a 4x4 grid of tiles
        self.create_tiles()

    def create_tiles(self):
        numbers = list(range(1, 9))  # Numbers from 1 to 8
        random.shuffle(numbers)
        
        # Create a 4x4 grid of tiles
        for i in range(2):
            for j in range(4):
                tile_text = f"{i * 4 + j + 1}"  # Text for the tile, ranging from 1 to 8
                tile_number = numbers.pop() # Number for the tile

                # Create a tile with the specified text and number
                tile_button = tk.Button(
                    self.root,
                    text=f"{tile_text}",
                    width=5,  # Set the width of the button
                    height=2,  # Set the height of the button
                    command=lambda text=tile_text, number=tile_number: self.tile_clicked(text, number, tile_button)
                )

                # Bind mouse events
                tile_button.bind("<Enter>", lambda event, button=tile_button: self.mouse_enter(event, button))
                tile_button.bind("<Leave>", lambda event, button=tile_button: self.mouse_leave(event, button))

                # Grid layout
                tile_button.grid(row=i, column=j, padx=5, pady=5)

    def tile_clicked(self, text, number, button):
        # Update the button text to show the number after clicking
        button["text"] = f"{number}"
        print(f"Tile Clicked! Text: {text}, Number: {number}")

    def mouse_enter(self, event, button):
        # Set a callback to be executed after 2000 milliseconds (2 seconds)
        button.after_id = button.after(2000, lambda: self.simulate_click(button))

    def mouse_leave(self, event, button):
        # Cancel the callback when the mouse leaves the button
        button.after_cancel(button.after_id)

    def simulate_click(self, button):
        # Simulate a click when the button has been hovered for more than 2 seconds
        button.event_generate("<Button-1>")
        print("Clicked tile ")

