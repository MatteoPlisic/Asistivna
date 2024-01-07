import tkinter as tk
from tkinter import messagebox
import random

class MemoryGame:
    def __init__(self, master, rows, columns):
        self.master = master
        self.rows = rows
        self.columns = columns
        self.buttons = []
        self.board = self.create_board()
        self.revealed = [[False] * columns for _ in range(rows)]
        self.first_click = None

        for i in range(rows):
            for j in range(columns):
                btn = tk.Button(master, text=" ", width=8, height=4, command=lambda i=i, j=j: self.on_click(i, j))
                btn.grid(row=i, column=j)
                self.buttons.append(btn)

    def create_board(self):
        numbers = list(range(1, (self.rows * self.columns) // 2 + 1)) * 2
        random.shuffle(numbers)
        return [numbers[i:i+self.columns] for i in range(0, len(numbers), self.columns)]

    def on_click(self, row, col):
        if not self.revealed[row][col]:
            self.revealed[row][col] = True
            self.buttons[row * self.columns + col].config(text=str(self.board[row][col]))
            
            if self.first_click is None:
                self.first_click = (row, col)
            else:
                second_click = (row, col)
                if self.board[self.first_click[0]][self.first_click[1]] == self.board[second_click[0]][second_click[1]]:
                    if self.is_game_over():
                        messagebox.showinfo("Memory Game", "Congratulations! You won!")
                        self.master.quit()
                else:
                    self.master.after(1000, self.cover_tiles, self.first_click, second_click)

                self.first_click = None

    def cover_tiles(self, first_click, second_click):
        row1, col1 = first_click
        row2, col2 = second_click

        self.revealed[row1][col1] = False
        self.revealed[row2][col2] = False

        self.buttons[row1 * self.columns + col1].config(text=" ")
        self.buttons[row2 * self.columns + col2].config(text=" ")

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

    root.mainloop()

if __name__ == "__main__":
    main()
