# coding=utf-8

from classes import *



# calcola il numero di giorni tra due date

def diff_dates(date1, date2):
    return abs(date2-date1).days



##############################################################################
# controlla se una camera disponibile tra i giorni di checkin e checkout     #
# errore nel ciclo "for element in dates_list" va iterato solo tra cin e cout#
# e non in tutta la dates_list                                               #
##############################################################################

def isAvailable(room_id,cin, cout, dates_list):
	for i in range(diff_dates(cout,cin)):
		if (cin+datetime.timedelta(i)) in dates_list:
			for element in dates_list:
				if room_id in element.busy:
					#print('Room is not available')
					return False
	#print('Room is available')
	return True


###############################################################
# stessa funzione di isAvailable ma implementata con lo slice #
# inoltre presente fix sul ciclo for di isAvailable           #
###############################################################

def isAvailable_2(room_id,cin, cout, dates_list):
        #########################################################################
	# adding Day objects if some/all days of the new booking are not present#
	# in dates_list                                                         #
	#########################################################################
	if (cin<dates_list[0] and cout > dates_list[-1]):
		print('Reservation too long, try again')
		return False

	# if reservation days are in days in the past (just for backup reasons)
	if cin < dates_list[0]:
		while cin not in dates_list: add_days(dates_list, 365,2)

	# if reservation days are after last day of dates_list --> append 1 year
	elif cout > dates_list[-1]:
		while cout not in dates_list: add_days(dates_list,365)

	start=dates_list.index(cin)
	for date in dates_list[start:start + diff_dates(cout,cin)]:
		if room_id in date.busy: return False
	return True






#############################################################
# aggiunge una stanza alla lista delle stanze occupate      #
# durante i giorni indicati tra gli argomenti cin, cout e   #
# aggiunge id della reservation al Day.reservation[]        #
#############################################################

def addRoom(room_id, reservation_id, cin, cout, dates_list):
	for i in range(diff_dates(cout,cin)):
		current_day=cin + datetime.timedelta(i)
		inside=False
		## Questo for potrebbe essere sostituito dalla funzione next()
		for pos, date in enumerate(dates_list):
			if (date==current_day):
				dates_list[pos].busy.append(room_id)
				dates_list[pos].free.remove(room_id)
				dates_list[pos].reservations.append(reservation_id)
				inside=True
				break
		if not inside:
			dates_list.append(Day(current_day.year,current_day.month,current_day.day))
			dates_list[len(dates_list)-1].busy.append(room_id)
			dates_list[len(dates_list)-1].free.remove(room_id)
			dates_list[len(dates_list)-1].reservations.append(reservation_id)
	return dates_list


############################################################################
# stessa funzione di addRoom, ma agisce su una lista di date statica      ##
# inizializzata al principio.I giorni sono tutti sequenziali nella lista  ##
############################################################################

def addRoom_2(room_id, reservation_id, cin, cout, dates_list):
	start=dates_list.index(cin)
	for i in range(diff_dates(cout,cin)):
		dates_list[start+i].busy.append(room_id)
		dates_list[start+i].free.remove(room_id)
		dates_list[start+i].reservations.append(reservation_id)
	return dates_list








#########################################################
# adds n days to a days list.                           #
# (check if argument is a Day object list to be done)   #
#########################################################

def add_days(dates_list, n,*args):
	way=1

	########################################################################
	# Check if dates_list is empty (should never once program completed)
	# and ,if not, append one year starting from Day.today()
 	# (guess it's a deprecated part of code, check again)

	if not dates_list:
		start=datetime.date.today()
		for i in range(n):
				current_day= start + datetime.timedelta(i*way)
				dates_list.append(Day(current_day.year, current_day.month, current_day.day))

	############################################################################
	# If a optional argument is present the 'way' variable is reversed (1-->-1)
	# Day objects are inserted at the beginning of dates_list instead of end.
	# (used if a booking, especially during an initial backup phase, contains
	# days in the past)

	if args:
		way=-1
		start=dates_list[0] + datetime.timedelta(1*way)
		for i in range(n):
			current_day= start + datetime.timedelta(i*way)
			dates_list.insert(0, Day(current_day.year, current_day.month, current_day.day))
	else:
		start=dates_list[-1] + datetime.timedelta(1*way)
		for i in range(n):
			current_day= start + datetime.timedelta(i*way)
			dates_list.append(Day(current_day.year, current_day.month, current_day.day))
	return dates_list







# abbozzo di nuova prenotazione. verifica disponibilit e aggiunge le camere
# ai giorni durante checkin e checkout. aggiunge alla classe Reservation

def newBooking(room_id, f, l, pax, cin, cout, mode, dates_list,reservations_list):

	#########################################################################
	# adding Day objects if some/all days of the new booking are not present#
	# in dates_list                                                         #
	#########################################################################
	if (cin<dates_list[0] and cout > dates_list[-1]):
		print('Reservation too long, try again')
		return False

	# if reservation days are in days in the past (just for backup reasons)
	if cin < dates_list[0]:
		while cin not in dates_list: add_days(dates_list, 365,2)

	# if reservation days are after last day of dates_list --> append 1 year
	elif cout > dates_list[-1]:
		while cout not in dates_list: add_days(dates_list,365)


	####################################################################
	# check if room is bookable and then create Reservation object and #
	# add room to busy within cin and cout                             #
	####################################################################

	if isAvailable_2(room_id, cin, cout, dates_list):
		new_reserve=Reservation(len(reservations_list), room_id, f, l, pax, cin, cout, mode)
		reservations_list.append(new_reserve)
		addRoom(room_id, new_reserve.id, cin,cout,dates_list)
		return dates_list, reservations_list
	else: print('Room can not be booked')
	return False





# restituisce tutte le date, come oggetti datetime.date, tra i giorni star_date
# e end_date

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)





# stampa la lista degli id delle camere libere giorno per giorno tra le date
# start_date e end_date (non penso serva a molto)

def show_days(start_date, end_date, dates_list):
	start=dates_list.index(start_date)
	#next(day for day in dates_list if day==start_date)
	for i in range(diff_dates(start_date, end_date)):
		print(dates_list[start+i].free)






# restituisce la lista delle camere prenotabili tra start_date e end_date
# possibile scegliere condizioni(numero letti, culla, balcone ecc.)

def what_available(start_date, end_date,dates_list, rooms_list, **kwargs):

	# condizione sui parametri delle camere chiedere a Stefano
	available_list=[]

	# se presenti argomenti opzionali
	if kwargs:
		filter_rooms=[]
		for kwarg in kwargs:
			# se il kwarg è tra gli attributi della classe Room
			# (in teoria sempre, ma non si sa in futuro)
			if kwarg in rooms_list[0].__dict__.keys():
				# controlla quali camere hanno lo stesso valore
				# per l'attributo corrispondente a kwarg e lo aggiunge alla
				# lista di camere adatte
				#### Condizioni meno stringenti (se beds=4 prendere anche <4)
				for room in rooms_list:
					if getattr(room, kwarg)==kwargs[kwarg]:
						filter_rooms.append(room)

	# se non sono presenti argomenti opzionali (i.e. vanno bene tutte le camere)
	else: filter_rooms=rooms_list

	# crea la lista delle camere prenotabili tra due date e corrispondenti
	# a eventuali criteri inseriti
	for room in filter_rooms:
			if isAvailable_2(room.id, start_date, end_date, dates_list):
				available_list.append(room.name)
	return available_list



















'''
		if (next((date for date in dates_list if (date.year==cin_year and date.month==cin_month and date.day==cin_day)), None))!=None:
			dates_list[dates_list.index(date)].busy.append(room_id)
			dates_list.append(Day(cin_year,cin_month, cin_day))
			dates_list[len(dates_list)+1].busy.append(room_id)
		else:
			dates_list.append(Day(cin_year,cin_month, cin_day))
			dates_list[len(dates_list)+1].busy.append(room_id)
'''
