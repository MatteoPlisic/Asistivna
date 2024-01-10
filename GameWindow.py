import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os
import time
from cheatsheet import cheatsheet
import numpy as np
#from StartWindow import StartWindow

class GameWindow:
    image_height = 152
    image_width = 109
    root_width = 800
    root_height = 700
    cheatsheet2 = cheatsheet()
    button_font = ("Comic Sans MS", 12, "roman")
    button_color = "#ee484c"
    button_width = 15
    button_height = 3

    def __init__(self, master, rows, columns,title):

        self.master = master
        if columns % 2 == 1:
            rows,columns = columns,rows
        self.rows = rows
        self.columns = columns


        self.buttons = []
        self.pitanja = []
        self.odgovori = []
        self.images = self.load_images()
        self.board = self.create_board()

        self.revealed = [[False] * columns for _ in range(rows)]
        self.first_click = None
        self.second_click = None
        self.allow_click = True
        master.title(title)
        self.row_labels = [tk.Label(master, bg=master.cget("background")) for _ in range(rows)]

        self.button_height_without_image = 10
        self.button_width_without_image = 15


        self.level_sizes = [(2, 2), (3, 2), (4, 2), (3, 4), (4, 4)]


        for i in range(rows):
            #self.row_labels[i].grid(row=i, column=0, padx=2, pady=2, sticky="nsew")
            self.row_labels[i].columnconfigure(0, weight=1)  # Make the column expand

            for j in range(columns):
                btn = tk.Button(self.row_labels[i], borderwidth=0, width=self.button_width_without_image, height=self.button_height_without_image, relief=tk.FLAT, command=lambda i=i, j=j: self.on_click(i, j))
                btn.grid(row=0, column=j, padx=2, pady=2, ipadx=0, ipady=0,sticky="nsew")  # Dodano postavljanje razmaka između gumba
                self.buttons.append(btn)

                btn.bind("<Enter>", lambda event, button=btn, row=i, col=j: self.on_button_hover(event, button, row, col))

                button_width = btn.winfo_reqwidth()
                button_height = btn.winfo_reqheight()
                print(f"Button {i}, {j} dimensions: {button_width} x {button_height}")

        self.master.update_idletasks()  # Force update before querying size
            
        py = (self.root_height - rows*self.row_labels[1].winfo_reqheight())/2
        px = (self.root_width - rows*self.image_width)/2
        
        self.ys = [py, py + self.row_labels[1].winfo_reqheight(), py + 2*self.row_labels[1].winfo_reqheight(), py + 3*self.row_labels[1].winfo_reqheight()]

        for i in range(rows):
            self.row_labels[i].place(x=(self.root_width - self.row_labels[1].winfo_reqwidth())/2, y=self.ys[i])
        
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

        images_pitanja = []
        for i in range(1, 101):
            filename = f"{i}.jpg"
            file_path = os.path.join("pitanja", filename)
            if os.path.exists(file_path):
                image = Image.open(file_path)
                images_pitanja.append(image)
        images_odgovori = []
        for i in range(1, 101):
            filename = f"{i}.jpg"
            file_path = os.path.join("odgovori", filename)
            if os.path.exists(file_path):
                image = Image.open(file_path)
                images_odgovori.append(image)

        dupli_indexi = []

        images= []

        for i in range(self.rows):
            imagetmp = []
            for j in range(self.columns//2):
                random_broj = np.random.randint(1,100)
                while(dupli_indexi.__contains__(random_broj)):
                    random_broj = np.random.randint(1,100)
                dupli_indexi.append(random_broj)
                filename = f"{random_broj}.jpg"
                file_path = os.path.join("odgovori", filename)
                image = Image.open(file_path)
                self.odgovori.append(filename)
                imagetmp.append(image.resize((109,152)))
                #imagetmp.append(self.Resize_Image(image, (119, 162)))
                file_path = os.path.join("pitanja", filename)
                image = Image.open(file_path)
                self.pitanja.append(filename)
                imagetmp.append(image.resize((109,152)))
                #imagetmp.append(self.Resize_Image(image, (119, 162)))
                
            images.append(imagetmp)
        ##images[1][1].show()
        print(self.rows,self.columns)

        flattened_images = [image for row in images for image in row]

        # Shuffle the flattened list
        np.random.shuffle(flattened_images)

        # Reshape the shuffled list back into a 2D array
        images = [flattened_images[i:i + len(images[0])] for i in
                              range(0, len(flattened_images), len(images[0]))]

       # images = [ImageTk.PhotoImage(self.Resize_Image(Image.open(os.path.join(image_dir, file)), (self.image_width, self.image_height))) for file in image_files]
        return images

    def create_board(self):
        image_indices = list(range(0, (self.rows * self.columns) // 2)) * 2
        random.shuffle(image_indices)
        return [image_indices[i:i + self.columns] for i in range(0, len(image_indices), self.columns)]

    def on_click(self, row, col):
        if not self.revealed[row][col] and self.allow_click:
            self.revealed[row][col] = True
            tk_image = ImageTk.PhotoImage(self.images[row][col])
            print(self.images[row][col])
            self.buttons[row * self.columns + col].config(image=tk_image,height=tk_image.height(),width=tk_image.width())
            self.buttons[row * self.columns + col].image = tk_image

            if self.first_click is None:
                self.first_click = (row, col)
            elif self.second_click is None:
                self.second_click = (row, col)
                self.allow_click = False  # Onemoguci klikanje
                self.master.after(1000, self.check_match)

    def check_match(self):
        row1, col1 = self.first_click
        row2, col2 = self.second_click
        image1 = self.images[row1][col1]
        image2 = self.images[row2][col2]

        pitanje = ""
        odgovor = ""
        folder_path = 'pitanja'
        for filename in self.pitanja:
            file_path = os.path.join(folder_path, filename)
            y = Image.open(file_path).resize((109,152))
            if image1 == y:
                pitanje = filename
            if image2 == y:
                pitanje = filename
        folder_path = 'odgovori'
        for filename in self.odgovori:
            file_path = os.path.join(folder_path, filename)
            y = Image.open(file_path).resize((109,152))
            print(filename)
            if image1 == y:
                odgovor = filename
            if image2 == y:
                odgovor = filename

        odgovor = odgovor[:-4]
        pitanje = pitanje[:-4]
        found = False
        if pitanje != "" and odgovor != "":
            file_path = "odgovori/"
            tocni_odgovor =   Image.open(file_path+odgovor+".jpg")
            for i in self.cheatsheet2[int(pitanje)]:


                if int(i) == int(odgovor):
                    print(i,odgovor)

                    found = True
                    if self.is_game_over():
                        index = self.level_sizes.index((self.rows, self.columns))
                        print("index=", index)
                        if index == len(self.level_sizes) - 1:
                            main_menu_button = tk.Button(self.master, text=f"Povratak na izbornik", command=self.return_to_menu, font=self.button_font, bg=self.button_color, width=self.button_width, height=self.button_height)
                            main_menu_button.grid(row=0, column=1, padx=10, sticky="w")
                            main_menu_button.bind("<Enter>", lambda event, button=main_menu_button, rows=4, cols=3: self.on_button_hover(event, button, rows, cols))
                            main_menu_button.bind("<Leave>", lambda event: main_menu_button.config(bg=self.button_color))
                        else: 
                            r, c = self.level_sizes[index + 1]
                            next_level_button = tk.Button(self.master, text=f"Sljedeći level", command=lambda rows=r, cols=c: self.start_game(rows, cols), font=self.button_font, bg=self.button_color, width=self.button_width, height=self.button_height)
                            next_level_button.grid(row=0, column=1, padx=10, sticky="w")
                            next_level_button.bind("<Enter>", lambda event, button=next_level_button, rows=r, cols=c: self.on_button_hover(event, button, rows, cols))
                            next_level_button.bind("<Leave>", lambda event: next_level_button.config(bg=self.button_color))


                        self.master.quit()

                else:
                    try:
                        if tocni_odgovor == Image.open(file_path+str(i)+".jpg"):
                            found = True
                            print(pitanje,i)
                            if self.is_game_over():
                                messagebox.showinfo("Memory Game", "Congratulations! You won!")
                                self.master.quit()
                    except:
                        print("error")
                        continue


        if not found:
            self.cover_tiles()

        # if self.images[row1][col1] == self.images[row2][col2]:
        #     if self.is_game_over():
        #         messagebox.showinfo("Memory Game", "Congratulations! You won!")
        #         self.master.quit()
        # else:
        #     self.cover_tiles()

        self.first_click = None
        self.second_click = None
        self.allow_click = True  # Omoguci klikanje nakon zavrsene provjere

    def return_to_menu(self):
        from StartWindow import StartWindow  # Import unutar funkcije
        for widget in self.master.winfo_children():
            widget.destroy()    
        StartWindow(self.master)

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
    
    def start_game(self, rows, cols):
        # Destroy the current window (StartWindow)
        self.master.destroy()
        print(rows, cols)

        # Create an instance of the BlankWindow class as a Toplevel window
        root = tk.Tk()

        game_window = GameWindow(root, columns=int(cols), rows=int(rows), title = "Game window")

        root.mainloop()  # Start the main loop for the new Tk instance
