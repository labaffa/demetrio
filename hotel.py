from classes import *
from functions import *
from Tkinter import *

import calendar
#import datetime

'''
root=Tk()
theLabel=Label(root, text='I am LaBaffa')
theLabel.pack()
root.mainloop()
'''

#Formo la lista delle stanze 
names=[("22",2),("23",2),("24",3),("25",4),("26",3),("Res",2),("Kappa",1),("8",2),("Alby",2)]
rooms_list=[Room(id,*names) for id,names in enumerate(names)]
rooms_number=len(rooms_list)

for room in rooms_list: print(room.name)

#lista di date e prenotazioni
dates_list=[]
reservations_list=[]
#dates_list.append(Day.today())



#prova di una prenotazione, una prenotazione non possibile, una seconda prenotazione. Stampiamo qualcosa
newBooking(0, 'laBaffa', 'laBaffetti',2, Day.today(), Day(2017,7,23), 'Booking', dates_list, reservations_list)
newBooking(0, 'laBaffa', 'laBaffettoni', 2, Day.today(), Day(2017,7,23), 'Booking', dates_list, reservations_list)
newBooking(8, 'Pinco', 'Pallino', 4, Day.today(), Day(2017,7,21), 'Booking', dates_list, reservations_list)

for element in dates_list: 
	print('Giorno', element, 'le camere libere sono:',element.getFree_names(rooms_list), 'le camere occupate:',element.getBusy_names(rooms_list))
for element in reservations_list: print(element.first_name, element.pax)




