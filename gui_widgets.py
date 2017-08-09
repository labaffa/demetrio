import calendar
import datetime
import ttk
from time import sleep
import classes as cl #FIX: find a commmon import

try:
    import Tkinter as tk
    import tkFont
except ImportError: # py3k
    import tkinter as tk
    import tkinter.font as tkFont



# TODOLIST:
# - rearrange (tidly) configuration of frames and widgets (bg,fg,fonts)
# - preload of calendar_widget--> slow when starting
# - size of header based on the longest month's name (September maybe)
# - find a way to get the longest month's name' and its width
# - toggle to eng-ita language swap (maybe more langs in future)
# - connect calendar's dates with hotel objects (Day,Room,...)
# - menu bar (over hframe if possible)
# - update() function to auto-change today() when app is running
# - scrolling bar
# - try to use Date_widget Class just if in the Hotel App.
#   in the Standalone Calendar object use tk.Label (Stefano)



# returns a calendar in a given (locale) language if
# a 'locale' argument is passed. Else an english calendar

def get_calendar(locale, fwday):
    # instantiate proper calendar class
    if locale is None:
        return calendar.TextCalendar(fwday)#english
    else:
        return calendar.LocaleTextCalendar(fwday, locale)#locale

#italiano = 'it_IT.utf8'   #locale of italiano 


class Date_widget(tk.Label):# a Label class extended 
    def __init__(self, master=None, **kw):
        tk.Label.__init__(self,master,**kw)
        self._date=None # a date is bound to every day-label of calendar
        
        
class Calendar(tk.Frame):
    # TODO: use selectforeground and background to get all tidy
    #! - changed calendar.datetime.datetime to calendar.datetime.date
    #    and now() to today() due to compatibility with Day class
    
    datetime = calendar.datetime.date
    timedelta = calendar.datetime.timedelta

    def __init__(self, master=None, **kw):
        #!!! Widget options 
        #
        #  locale, firstweekday, year, month,
        #  selectbackground, selectforeground
        #
        #!!!

        
        # remove custom options from kw
        # before initializating ttk.Frame
        fwday = kw.pop('firstweekday', calendar.MONDAY)
        year = kw.pop('year', self.datetime.today().year)
        month = kw.pop('month', self.datetime.today().month)
        today = kw.pop('today', self.datetime.today().day)
        locale = kw.pop('locale', None)
        sel_bg = kw.pop('selectbackground', '#ecffc4')
        sel_fg = kw.pop('selectforeground', '#05640e')

        # Interesting how they are assigned
        # (Calendar_widget does not inherit from datetime or calendar)
        self._today = self.datetime(year,month,today) # added by me
        self._date = self.datetime(year, month, 1) # first of month
        self._selection = None # no date selected
        print(type(self._today),type(self._date))
        
        tk.Frame.__init__(self, master, **kw) # inheritance

        self._cal = get_calendar(locale,fwday) # a calendar
        self.w_list=[] # labels with days of weekdays
        self.dates_ls=[] # grid of dates month
        self._place_widgets() # pack or grid widgets
        self._conf_calendar() # setup colors, size etc.. (dont know)
        self._build_calendar() # insert data in the month calendar

        
    # special methods
    def __setitem__(self, item, value):
        pass

    def __getitem__(self, item):
        pass

    def _conf_calendar(self):
        pass
    
    def _place_widgets(self):
        myfont=tkFont.Font(family='Helvetica',
                                  size=10,
                                 weight=tkFont.BOLD)
        
        #! FIX: header size bases on longest month
        
        # place and size of the frames in Calendar
        self.columnconfigure(0,weight=1) #fill X
        self.grid_rowconfigure(0,weight=0) #hframe row position
        self.rowconfigure(1,weight=0) #wframe row position
        self.rowconfigure(2,weight=1) #cframe row position (stretchable)
        
        # header frame and its widgets
        hframe = tk.Frame(self,
                          bg='#DEE1DB') # buttons and header(month,year)

        
        lbtn = tk.Button(hframe, text='<',
                          bg='white',
                         highlightthickness=2,
                         highlightbackground='#F6E8FF',
                          command=self._prev_month) # prev month
        lbtn.config(font=myfont)

        
        rbtn = tk.Button(hframe, text='>',
                         bg='white',
                         highlightthickness=2,
                         highlightbackground='#F6E8FF',
                          command=self._next_month) # next month
        rbtn.config(font=myfont)

        
        self._header = tk.Label(hframe,
                                bg='#DEE1DB',
                                 anchor='center') # header
        self._header.config(font=myfont)

        # the calendar (changed from Treeview object)
        # now two frames: day-names (fixed size, or nearly)
        #                 dates (size grows with the object)

        wframe = tk.Frame(self,bg='#DEE1DB') # day-names frame
        cframe = tk.Frame(self) # dates frame


        # Pack/grid frames and widgets

        #hframe and its widgets
        hframe.grid(row=0,
                    column = 0,sticky='we',
                    ipadx=2,ipady=2) # check for stickiness
        
        
        
        lbtn.grid(row=0,column=0,sticky='e')# button
        hframe.columnconfigure(0,weight=1)# left
        
        
        self._header.grid(row=0,
                          column=1,
                          sticky='news',
                          ipadx=15,ipady=15)#header
        hframe.columnconfigure(1,minsize=150,weight=0)#header
        
        
        rbtn.grid(row=0, column=2,sticky='w')   #button
        hframe.columnconfigure(2,weight=1) #right

        
        #wframe
        wframe.grid(row=1,
                    column=0,
                    sticky='we',
                    ipady=5)  
        # inserting names
        names = self._cal.formatweekheader(3).split()
        for i, name in enumerate(names):
            self.w_list.append(tk.Label(wframe,
                                         text=name,
                                         bg='#DEE1DB',
                                         anchor='center'))
            wframe.columnconfigure(i,weight=1)
            self.w_list[i].grid(row=0,
                                column=i,
                                sticky='news')

            
        #cframe
        cframe.grid(row=2,
                    column=0,
                    sticky='news') 
        # grid of 6x7 labels for future filling
        for week in range(6): #over max number of weeks
            cframe.rowconfigure(week,
                                weight=1) # weighting rows
            for day in range(7): #over 7 days of weeks
                cframe.columnconfigure(day,
                                        weight=1)# weighting cols
                self.dates_ls.append(Date_widget(cframe,
                                               text='',
                                          highlightthickness=1,
                                          highlightbackground='#EEEEEC',
                                              takefocus=True,
                                               anchor='center'))
                self.dates_ls[-1].grid(row=week,
                                       column=day,
                                       sticky='news')

    def _build_calendar(self):
        # year and month to visualize
        year,month = self._date.year, self._date.month

        # update header (month, year)
        header = self._cal.formatmonthname(year, month, 0)
        self._header['text'] = header.title()

    
        
        # update dates
        fday = calendar.monthrange(year, month)[0] #weekday of the first
        ndays = calendar.monthrange(year,month)[1] #days in the month
        
        for i,date in enumerate(self.dates_ls):
            shift=i-fday
            day=self._date + self.timedelta(days=shift)
            date._date = day
            date['text']=str(day.day)
            date['fg'] = 'black' if shift in range(ndays) else '#D3D7CF'
            date['bg'] = '#F6E8FF' if day==self._today else 'white'
        
            
    def _prev_month(self):
        self._date = self._date - self.timedelta(days=1)
        self._date = self.datetime(self._date.year, self._date.month, 1)
        self._build_calendar() # reconstuct calendar


    def _next_month(self):
        year,month = self._date.year, self._date.month 
        self._date = self._date + self.timedelta(
            days=calendar.monthrange(year, month)[1] + 1)
        self._date = self.datetime(self._date.year, self._date.month, 1)
        self._build_calendar() # reconstruct calendar



# A Calendar class with dates that are linked to app-specific stuff
class App_cal(Calendar):
    def __init__(self, master=None, **kw):
        Calendar.__init__(self, master,**kw)
        self._bind_labels() #binds events to all dates labels
        self._bg_var=None #bg of widgets stored for mouse focus events
        self._ls = cl.List() #list object of Day, Room, Reservation
        self._toggle=False # a toggle

        
    def _bind_labels(self):    
        for date in self.dates_ls:
            date.bind("<Button-1>", self._callback)
            date.bind("<Enter>", self._mouse_on)
            date.bind("<Leave>",self._mouse_off)
            date.bind("<Button-3>",self._popup)
            
    def show_free(self,day):#shows free rooms of day 'day'
        for date in self._ls._day:
            if date == day: 
                print(date.free)
                break


    
    #CALLBACKS
    def _mouse_on(self,event):
        self._bg_var=event.widget['bg'] #saves bg before entering
        event.widget.config(bg='#D3D7CF')
        
        
    def _mouse_off(self,event):
        event.widget.config(bg=self._bg_var)#sets bg as before 

        
    def _callback(self,event):# too complex. try to get it simpler
        day = event.widget._date #day in datetime.date format
        self.show_free(day)

    def _popup(self,event):
        #if self._toggle: # already a popup in there
        popup = tk.Label(self, text='Ciao',bg='green')
        date_pos = (event.widget.winfo_rootx(),
                    event.widget.winfo_rooty())  
        date_size = (event.widget.winfo_width(),
                     event.widget.winfo_height())
        x=date_pos[0]# + date_size[0]/2
        y=date_pos[1]#+date_size[1]/2
        print(x,y) 
        popup.place(x=x,y=y)

class popup(tk.Label):
    pass


        
        
