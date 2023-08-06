import tkinter as tk

from tkinter import ttk
from itertools import cycle
from Tomel.components.profile_generator import shape_image

class Slideshow:
    def __init__(self, root, timing: int = 1500, picture_locations: list[str] = []):
        self.picture_locations = picture_locations
        self.timing = timing
        
        self.slideshow_frame = ttk.Frame(root, padding=10)
        
        self.display_canvas = tk.Label(self.slideshow_frame)
        self.display_canvas.grid(row=0, column=0)
        
        self.configured = False
        
    def add_picture_location(self, picture_location):
        self.picture_locations.append(picture_location)
        
    def reconfigure(self):
        self.photos = cycle(shape_image(image, 250, 250) for image in self.picture_locations)
        self.configured = True
        
    def display_show(self):
        if not self.configured:
            self.reconfigure()
            
        img = next(self.photos)
        self.display_canvas.config(image=img)      
        self.slideshow_frame.after(self.timing, self.display_show)
        
    def set_grid(self, _row: int = 0, _column: int = 0):
        self.slideshow_frame.grid(row=_row, column=_column)
