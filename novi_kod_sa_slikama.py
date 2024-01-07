import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

class MemoryGame:
    def __init__(self, master, rows, columns):
        self.master = master
        self.rows = rows
        self.columns = columns
        self.buttons = []
        self.images = self.load_images()
        self.board = self.create_board()
        self.revealed = [[False] * columns for _ in range(rows)]
        self.first_click = None
        self.second_click = None
        self.allow_click = True

        for i in range(rows):
            for j in range(columns):
                btn = tk.Button(master, width=15, height=10, relief=tk.FLAT, command=lambda i=i, j=j: self.on_click(i, j))
                btn.grid(row=i, column=j, padx=2, pady=2)  # Dodano postavljanje razmaka između gumba
                self.buttons.append(btn)

    def load_images(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_dir = os.path.join(current_dir, "images")
        image_files = ["image_1.jpg", "image_2.jpg", "image_3.jpg", "image_4.jpg", "image_5.jpg", "image_6.jpg", "image_7.jpg", "image_8.jpg"]
        images = [ImageTk.PhotoImage(Image.open(os.path.join(image_dir, file)).resize((15, 10))) for file in image_files]
        return images

    def create_board(self):
        image_indices = list(range(0, (self.rows * self.columns) // 2)) * 2
        random.shuffle(image_indices)
        return [image_indices[i:i+self.columns] for i in range(0, len(image_indices), self.columns)]

    def on_click(self, row, col):
        if not self.revealed[row][col] and self.allow_click:
            self.revealed[row][col] = True
            self.buttons[row * self.columns + col].config(image=self.images[self.board[row][col]])

            if self.first_click is None:
                self.first_click = (row, col)
            elif self.second_click is None:
                self.second_click = (row, col)
                self.allow_click = False  # Onemoguci klikanje
                self.master.after(1000, self.check_match)
                
    def check_match(self):
        row1, col1 = self.first_click
        row2, col2 = self.second_click

        if self.board[row1][col1] == self.board[row2][col2]:
            if self.is_game_over():
                messagebox.showinfo("Memory Game", "Congratulations! You won!")
                self.master.quit()
        else:
            self.cover_tiles()

        self.first_click = None
        self.second_click = None
        self.allow_click = True  # Omoguci klikanje nakon zavrsene provjere

    def cover_tiles(self):
        row1, col1 = self.first_click
        row2, col2 = self.second_click

        self.revealed[row1][col1] = False
        self.revealed[row2][col2] = False

        self.buttons[row1 * self.columns + col1].config(image="")
        self.buttons[row2 * self.columns + col2].config(image="")

    def is_game_over(self):
        for row in self.revealed:
            if False in row:
                return False
        return True

def main():
    root = tk.Tk()
    root.title("Memory Game")

    rows, columns = 4, 4
    game = MemoryGame(root, rows, columns)

    # Postavljanje pozadinske boje na zelenu
    root.configure(bg="green")

    root.mainloop()

if __name__ == "__main__":
    main()
