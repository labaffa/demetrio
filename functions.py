from classes import *

#calcola il numero di giorni tra due date
def diff_dates(date1, date2):
    return abs(date2-date1).days



#verifica se una camera è libera tra le eventuali date di checkin e di checkout
def isAvailable(room_id,cin, cout, dates_list):
	for i in range(diff_dates(cout,cin)):
		if (cin+datetime.timedelta(i)) in dates_list:
			for element in dates_list:
				if room_id in element.busy:
					print('Room is not available') 
					return False
	print('Room is available')
	return True 
	

#aggiunge una stanza alla lista delle stanze occupate durante i giorni indicati tra gli argomenti cin, cout
def addRoom(room_id, cin, cout, dates_list):
	for i in range(diff_dates(cout,cin)):
		current_day=cin + datetime.timedelta(i)
		inside=False
		## Questo for potrebbe essere sostituito dalla funzione next()
		for pos, date in enumerate(dates_list):
			if (date==current_day):
				dates_list[pos].busy.append(room_id)
				dates_list[pos].free.remove(room_id)
				inside=True
				break	
		if not inside:
			dates_list.append(Day(current_day.year,current_day.month,current_day.day))	
			dates_list[len(dates_list)-1].busy.append(room_id)
			dates_list[len(dates_list)-1].free.remove(room_id)
	return dates_list



#abbozzo di nuova prenotazione. verifica disponibilità e aggiunge le camere ai giorni durante checkin e checkout. aggiunge alla classe Reservation
def newBooking(room_id, f, l, pax, cin, cout, mode, dates_list,reservations_list):
	if isAvailable(room_id, cin, cout, dates_list):
		addRoom(room_id, cin,cout,dates_list)
		reservations_list.append(Reservation(room_id, f, l, pax, cin, cout, mode))	
		return dates_list, reservations_list	
	else: print('Room can not be booked')
	return False

























'''
		if (next((date for date in dates_list if (date.year==cin_year and date.month==cin_month and date.day==cin_day)), None))!=None:
			dates_list[dates_list.index(date)].busy.append(room_id)			
			dates_list.append(Day(cin_year,cin_month, cin_day))
			dates_list[len(dates_list)+1].busy.append(room_id)
		else: 
			dates_list.append(Day(cin_year,cin_month, cin_day))
			dates_list[len(dates_list)+1].busy.append(room_id)
'''
	
	
	
		
	
	
	
