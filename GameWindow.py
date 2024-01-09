import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os
import time

class GameWindow:
    image_height = 152
    image_width = 109
    def __init__(self, master, rows, columns,title):

        self.master = master
        self.rows = rows
        self.columns = columns
        self.buttons = []
        self.images = self.load_images()
        self.board = self.create_board()
        print(self.board)
        self.revealed = [[False] * columns for _ in range(rows)]
        self.first_click = None
        self.second_click = None
        self.allow_click = True
        master.title(title)
        self.row_labels = [tk.Label(master, bg="green") for _ in range(rows)]

        self.button_height_without_image = 10
        self.button_width_without_image = 15
        
        

        for i in range(rows):
            self.row_labels[i].grid(row=i, column=0, padx=2, pady=2, sticky="nsew")

            for j in range(columns):
                btn = tk.Button(self.row_labels[i], width=self.button_width_without_image, height=self.button_height_without_image, relief=tk.FLAT, command=lambda i=i, j=j: self.on_click(i, j))
                btn.grid(row=0, column=j, padx=2, pady=2, sticky="nsew")  # Dodano postavljanje razmaka između gumba
                self.buttons.append(btn)
    
                btn.bind("<Enter>", lambda event, button=btn, row=i, col=j: self.on_button_hover(event, button, row, col))

    def on_button_hover(self, event, button, row, col):
        global hover_start_time
        hover_start_time = time.time()

        self.check_hover(button, row, col)

    def check_hover(self, button, row, col):
        current_mouse_x = self.master.winfo_pointerx() - self.master.winfo_rootx()
        current_mouse_y = self.master.winfo_pointery() - self.master.winfo_rooty()
        
        button_x = button.winfo_rootx() - self.master.winfo_rootx()
        button_y = button.winfo_rooty() - self.master.winfo_rooty()

        button_absolute_x = button.winfo_rootx() - self.master.winfo_rootx()
        button_absolute_y = button.winfo_rooty() - self.master.winfo_rooty()

        button_width = button.winfo_reqwidth()
        button_height = button.winfo_reqheight()

        if (
            button_x <= current_mouse_x <= button_x + button_width and
            button_y <= current_mouse_y <= button_y + button_height
        ):
            elapsed_time = time.time() - hover_start_time
            if elapsed_time >= 1:  # 1 second
                self.on_click(row, col)
                return
        else:
            # Stop checking if the mouse is no longer over the button
            return
        
        button.after(100, lambda: self.check_hover(button, row, col))  # Check every 100 milliseconds

    def Resize_Image(self, image, maxsize):
        r1 = image.size[0] / maxsize[0]  # width ratio
        r2 = image.size[1] / maxsize[1]  # height ratio
        ratio = max(r1, r2)
        #newsize = (int(image.size[0] / ratio), int(image.size[1] / ratio))
        #image = image.resize(newsize, Image.LANCZOS)
        image = image.resize((maxsize), Image.LANCZOS)
        return image

    def load_images(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_dir = os.path.join(current_dir, "images")
        image_files = ["image_1.jpg", "image_2.jpg", "image_3.jpg", "image_4.jpg", "image_5.jpg", "image_6.jpg", "image_7.jpg", "image_8.jpg"]
        
        images = [ImageTk.PhotoImage(self.Resize_Image(Image.open(os.path.join(image_dir, file)), (self.image_width, self.image_height))) for file in image_files]
        return images

    def create_board(self):
        image_indices = list(range(0, (self.rows * self.columns) // 2)) * 2
        random.shuffle(image_indices)
        return [image_indices[i:i+self.columns] for i in range(0, len(image_indices), self.columns)]

    def on_click(self, row, col):
        if not self.revealed[row][col] and self.allow_click:
            self.revealed[row][col] = True
            self.buttons[row * self.columns + col].config(image=self.images[self.board[row][col]], width=self.image_width, height=self.image_height)

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

        self.buttons[row1 * self.columns + col1].config(image="", width=self.button_width_without_image, height=self.button_height_without_image)
        self.buttons[row2 * self.columns + col2].config(image="", width=self.button_width_without_image, height=self.button_height_without_image)

    def is_game_over(self):
        for row in self.revealed:
            if False in row:
                return False
        return True
