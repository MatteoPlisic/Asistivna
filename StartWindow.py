import tkinter as tk
from BlankWindow import BlankWindow
from GameWindow import GameWindow
class StartWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Igra memory")

        # Create labels and buttons
        label = tk.Label(root, text="Dobrodošli u igru memory!", font=("Helvetica", 16))
        start_button = tk.Button(root, text="Start Game", command=self.start_game)
        choose_level_button = tk.Button(root, text="Odaberi nivo", command=self.choose_level)

        # Pack widgets to the window
        label.pack(pady=30)
        start_button.pack(pady=10)
        choose_level_button.pack(pady=10)

    def start_game(self):
        # Destroy the current window (StartWindow)
        self.root.destroy()

        # Create an instance of the BlankWindow class as a Toplevel window
        root = tk.Tk()
        game_window = GameWindow(root, columns=4, rows=4,title = "Game window")
        root.mainloop()  # Start the main loop for the new Tk instance
        print("Starting the game!")

    def choose_level(self):
        print("Choose level")


