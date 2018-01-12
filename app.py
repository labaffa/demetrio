from classes.data_holder import DataHolder
from classes.calendar_app import CalendarApp
from calendar_classic.utils.checkers import proportion_to_screen_size, \
    proportion_to_screen_string
try:
    import Tkinter as tk
    import tkFont
except ImportError: # python 3
    import tkinter as tk
    import tkinter.font as tkFont


class Home_screen(tk.Tk):
    """The Home screen of the app"""
    def __init__(self, **kw):
        tk.Tk.__init__(self, **kw)
        # Place Calendar_classic in window
        screen = CalendarApp(self)
        screen.action = screen.get_day # action for left click on days 
        screen.grid(row=0, column=0, sticky='news')
        # Make the calendar strechable
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        # Set dimensions
        self.default_size()
        self.minimum_size()

    def default_size(self, w=3, h=2):
        """
        Set size of the window at launch proportioned to screen's size.
        w, h = 1,1 to launch in fullscreen mode
        """
        default_size = proportion_to_screen_string(self, w, h)
        self.geometry(default_size)

    def minimum_size(self, w=5, h=3):
        """
        Set minimum size of the window proportioned to screen's size
        """
        min_width, min_height = proportion_to_screen_size(self, w, h)
        self.minsize(min_width, min_height)



if __name__ == '__main__':
    root = Home_screen()
    # root.default_size(w=1, h=1) # fullscreen at launch
    root.mainloop()
