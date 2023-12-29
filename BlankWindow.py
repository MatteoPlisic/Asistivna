import tkinter as tk

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

        # Create widgets or add additional setup as needed
        label = tk.Label(root, text="This is a blank window.")
        label.pack(pady=20)