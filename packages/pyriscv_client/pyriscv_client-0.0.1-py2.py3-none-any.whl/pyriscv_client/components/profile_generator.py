import tkinter as tk

from PIL import Image, ImageTk
from tkinter import ttk

def shape_image(image_location: str, x: int, y: int):
    img = Image.open(image_location)
    img = img.resize((x,y), Image.ANTIALIAS)
    return ImageTk.PhotoImage(img)
    
def get_image(image_location: str):
    img = Image.open(image_location)
    return ImageTk.PhotoImage(img)
    
variables = {}

def generate_profile_frame(root, image_variable_name: str, heading: dict, sub_heading: dict, content: dict, contact_information: dict):
    profile_frame = ttk.Frame(root, padding=5)
    
    profile_picture = tk.Label(profile_frame, image = variables[image_variable_name])
    profile_picture.grid(row=0, column=0, padx=(10,10), pady=(20,20))
    
    def make_label(information: dict, _row: int, _col: int, _padx: tuple = (5, 5), _pady: tuple = (5, 5), foreground_color: str = "black", background_color: str = "#ffffff"):
        temp_label = tk.Label(profile_frame, text=information['text'], font=(information['font_family'], information['font_size']), bg=background_color, fg=foreground_color)
        temp_label.grid(row=_row, column=_col, padx=_padx, pady=_pady)
    
    make_label(heading, 1, 0)
    make_label(sub_heading, 2, 0)
    make_label(content, 3, 0)
    make_label(contact_information, 4, 0, foreground_color = "white", background_color = "black")
    
    return profile_frame
