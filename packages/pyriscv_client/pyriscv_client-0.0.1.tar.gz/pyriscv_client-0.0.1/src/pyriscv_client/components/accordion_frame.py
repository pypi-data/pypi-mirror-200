import tkinter as tk
from tkinter import ttk
 
class Accordion(ttk.Frame): 
    def __init__(self, parent, expanded_text ="Collapse <<",
                               collapsed_text ="Expand >>"):
 
        ttk.Frame.__init__(self, parent)
        
        self.parent = parent
        self._expanded_text = expanded_text
        self._collapsed_text = collapsed_text

        self.columnconfigure(1, weight = 1)
 
        self._variable = tk.IntVar()
        
        self._button = ttk.Checkbutton(self, variable = self._variable,
                            command = self._activate, style ="TButton")
        self._button.grid(row = 0, column = 0)
 
        self._separator = ttk.Separator(self, orient ="horizontal")
        self._separator.grid(row = 0, column = 1, sticky ="we")
 
        self.frame = ttk.Frame(self)
        
        self._activate()
 
    def _activate(self):
        if not self._variable.get():
 
            # As soon as button is pressed it removes this widget
            # but is not destroyed means can be displayed again
            self.frame.grid_forget()
 
            # This will change the text of the checkbutton
            self._button.configure(text = self._collapsed_text)
 
        elif self._variable.get():
            self.frame.grid(row = 1, column = 0, columnspan = 2)
            self._button.configure(text = self._expanded_text)
 
    def toggle(self):
        """Switches the label frame to the opposite state."""
        self._variable.set(not self._variable.get())
        self._activate()
