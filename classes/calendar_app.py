from calendar_classic import Calendar_classic
from classes.data_holder import DataHolder
from settings.constants import rooms
import calendar
from datetime import timedelta, date


class CalendarApp(Calendar_classic):
    
    def __init__(self, master=None, **kw):
        self.source = kw.pop('source', DataHolder('default.dat'))
        self.action = kw.pop('action', self.default_action)
        Calendar_classic.__init__(self, master, **kw)
        self.display_availability()
        
        # bind callbacks to boxes. TODO: create function to do this
        boxes = self.table.date_boxes
        for box in boxes:
            box.bind('<Button-1>', self.callback)


    def callback(self, event):
        self.action(event)


    def default_action(self, event):
        """Action performed if 'action' attribute was not inserted"""
        print('Pass a function to this object to execute it')


    def get_day(self, event):
        """ Print busy rooms during the clicked day """
        try:
            print(self.source.busy_days[event.widget.date])
        except KeyError:
            print(rooms)
   

    def display_availability(self):
        """ Tell if hotel is full for all displayed days """
        
        for date_box in self.table.date_boxes:
            # check for free rooms
            free_rooms = list(rooms.keys())
            try: # if at least one is busy (key in busy_dict exist)
                busy_rooms = self.source.busy_days[date_box.date]
                for room in busy_rooms:
                    free_rooms.remove(room)
            except KeyError: # all rooms are free
                pass
            if date_box.date >= date.today():
                free = 'Free' if free_rooms else 'Full'
            else:
                free = ''
            # overwrite with availability indication
            date_box.configure(text=str(date_box.date.day) +
                               '\n ' + free)
            self.table.label_config(date_box, date_box.date)


    def prev_month(self):
        super(CalendarApp, self).prev_month()
        self.display_availability()
        # self.display_free_rooms()


    def next_month(self):
        super(CalendarApp, self).next_month()
        self.display_availability()
        # self.display_free_rooms()


    def display_free_rooms(self):
        """
        Configure text of each Date_box with a list of free rooms
        (still not usable due to layout problems)
 
        TODO: fix layout: options ->
        - use tk.Canvas instead of tk.Label 
        - use tk.Text to display free rooms
        - divide Date_box in upper-part to display the day, and a 
          lower-part where display day-specific infos

        TODO: in calendar_classic repo make widgets not strechable or 
        resizable when a text is too long. (should be a parameter)

        """

        for date_box in self.table.date_boxes:
            # check for free rooms
            free_rooms = list(rooms.keys())
            try: # if at least one is busy (key in busy_dict exist)
                busy_rooms = self.source.busy_days[date_box.date]
                for room in busy_rooms:
                    free_rooms.remove(room)
            except KeyError: # all rooms are free
                pass
            if date_box.date >= date.today():
                free = free_rooms
            else:
                free = ''
            free = ' '.join(free) # blank separated in same row
            # overwrite with availability indication
            date_box.configure(text=str(date_box.date.day) +
                               '\n ' + free)
            self.table.label_config(date_box, date_box.date)
