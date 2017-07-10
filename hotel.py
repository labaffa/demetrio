from demetrio import Room
from demetrio import Day
from Tkinter import *

import calendar
#import datetime


root=Tk()
theLabel=Label(root, text='Ma che fai?')
theLabel.pack()
root.mainloop()

names=[("22",2),("23",2),("24",3),("25",4),("26",3),("Res",2),("Kappa",1),("8",2),("Alby",2)]


rooms=[Room(id+1,*names) for id,names in enumerate(names)]
rooms_number=len(rooms)


#for room in rooms: print (room.id, room.name, room.beds)
#cal = calendar.Calendar(firstweekday=0)
#for i in cal.iterweekdays():print(i)

today=Day.today()
today.add(1,rooms_number)
today.add(6,rooms_number)

#print(today.busy[1])

today.get_busy()
today.get_busy_name(rooms)
today.get_free_name(rooms)
#print (len(today.busy))




