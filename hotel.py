# coding=utf-8

#import classes_gui as gui
from classes import *
from functions import *
import pickle
from  io_functions import *
import calendar
import gui_widgets as gui
try:
    import Tkinter as tk
    import tkFont
except ImportError: # py3k
    import tkinter as tk
    import tkinter.font as tkFont


# todolist:
# - create as much Day obj as datetime of calendar
# - create obj for root 


#########################
#########################
#  		        #
#   Test part on GUI    #
#                       #
#########################
#########################


root=tk.Tk()
#root.attributes('-alpha',0.0)  #attempt to preload 
#root.withdraw()                # ''     ''   ''
#root.after(2000,root.deiconify)# ''     ''   ''

root.rowconfigure(0, #row of calendar in master
                  minsize=200,#minsize of calendar height
                  weight=1)#root-row streches with window
root.columnconfigure(0, #col of calendar in master
                     minsize=200, #minsize of the calendar
                     weight=1)#root-col streches with window

root.minsize(width=200,height=0) #minsize of window


tkcal = gui.Calendar(root,
                  width=300, #starting width
                  height=350)#starting height

tkcal.grid(row=0,column=0,sticky='news')#sticked with root
tkcal.grid_propagate(False) #prevent ttkcal initial propagation



#root.after(0, root.attributes, "-alpha", 1.0) # attempt to preload
#root.after(2000,root.deiconify)               #    ''   ''    ''
root.tk.mainloop()


#####################
#####################
#                   #
#   Test part on    #
#   Functions	    #
#		    #
#####################
#####################

#Rooms list
names=[("22",2),("23",2),("24",3),("25",4),("26",3),("Res",2),("Kappa",1),("8",2),("Alby",2)]
rooms_list=[Room(id,*names) for id,names in enumerate(names)]
rooms_number=len(rooms_list)

for room in rooms_list: print(room.name)

#Days and Reservation lists
dates_list=[]
reservations_list=[]


# creazione lista di oggetti Day per un anno a partire da oggi
# (what about Day before today?)
start=datetime.date.today()
for i in range(365):
	current_day= start + datetime.timedelta(i)
	dates_list.append(Day(current_day.year, current_day.month, current_day.day))

#print(rooms_list[0].__dict__.keys(), getattr(rooms_list[0], 'beds'))


#prova di una prenotazione, una prenotazione non possibile, una seconda prenotazione. Stampiamo qualcosa
newBooking(0, 'laBaffa', 'laBaffetti',2, Day.today(), Day(2017,7,27), 'Booking', dates_list, reservations_list)
newBooking(0, 'laBaffa', 'laBaffettoni', 2, Day.today(), Day(2017,7,27), 'Booking', dates_list, reservations_list)
newBooking(8, 'Pinco', 'Pallino', 4, Day(2017,7, 29), Day(2019,7,28), 'Booking', dates_list, reservations_list)

print(len(dates_list), dates_list[0])
#show_days(datetime.date.today(), datetime.date.today()+datetime.timedelta(3),dates_list)

print(isAvailable_2(8, Day(2017,7,30), Day(2017, 7, 31), dates_list))
print(what_available(Day(2017,8,2), Day(2017, 8,7), dates_list, rooms_list))


'''
save_data(rooms_list, "rooms.txt")
print(load_data("rooms.txt"))
'''
print(getattr(rooms_list[0], 'name'))
#for room in rooms_list: pickle.dump(rooms_list,open( "rooms_1.txt", "a"))

pickle.dump(rooms_list,open( "rooms_1.txt", "wb"))


#pickle.dump(rooms_list,open( "rooms.txt", "a"))
rooms_2_list = pickle.load(open("rooms_1.txt", 'rb'))

for room in rooms_2_list: print(room.name)
print(rooms_2_list[5].name)

write(rooms_list)
rooms_file=read(rooms_list)

for room in rooms_file:print(room.id)

print(calendar.day_name[dates_list[0].weekday()])


'''
for date in dates_list:
	print('Giorno', date, 'le camere libere sono:',date.getFree_names(rooms_list), 'le camere occupate:',date.getBusy_names(rooms_list))
	date.getRes_info(reservations_list)
for element in reservations_list: print(element.first_name, element.pax)
'''


#print(diff_dates(Day.today(), Day.today()+datetime.timedelta(5)))

#now=Day.today()
#for o in rooms: print(o.name)
#print(now.year, now.month, now.day)



#now.getFree(rooms_list)
#today=Day.today()

#print(now.getFree(rooms_list))
#print(now.getBusy(rooms_list))

#print(now.free)
#for rooms in rooms: print(rooms.name)
#marga=Reservation('Laura','Silvestro', 3, 2018,7,7, 3)
#print(date.getFree(rooms_list))
