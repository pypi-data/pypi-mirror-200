import tkinter as tk
from tkinter import ttk

class BulletLabel(tk.Label):
    def __init__(self, master, *args, **kwargs):
        text = kwargs.pop('text', '')
        kwargs['text'] = self.bulletise(text)
        tk.Label.__init__(self, master, *args, **kwargs)

    def bulletise(self, text):
        if len(text) == 0:
            return ''
        lines = text.split('\n')
        parts = []
        for line in lines:
            parts.extend(['\u2022', line, '\n'])
        return ''.join(parts)

    def configure(self, *args, **kwargs):
        text = kwargs.pop('text', '')
        if text != '':
            kwargs['text'] = self.bulletise(text)
        tk.Label.configure(*args, **kwargs)

class BulletFrame:
    def __init__(self, root):
        self.labels = []
        self.problems = []
        self.counter = 0
        
        self.bullet_frame = ttk.Frame(root, padding=10)
        
    def add_bullet(self, _text, _foreground="green", _font=("Ubuntu", 14)):
        self.labels.append(tk.Label(self.bullet_frame, text=_text, cursor="hand2", foreground=_foreground, font=_font))
        
        self.problems.append(self.counter)
        
        self.labels[-1].grid(row=self.counter, column=0)        
        self.labels[-1].bind("<Button-1>", lambda e, i=self.counter: self.open_problem(i))
        
        self.counter += 1
    
    def open_problem(self, bullet_number):
        print(bullet_number)
        
    def set_grid(self, _row: int = 0, _column: int = 0):
        self.bullet_frame.grid(row=_row, column=_column)
