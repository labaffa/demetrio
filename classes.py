import datetime


class Room:
	def __init__(self, id, name, beds):
		self.id=id
		self.name=name
		self.beds=beds

	#def __getitem__(self, key): return self.name[key]


'''
class Date(object):
	def __init__(self, year, month, day):
		self.year=year
		self.month=month
		self.day=day
'''

class Day(datetime.date):
	
	#rooms_no=9

	def __init__(self, year, month, day):
		super(Day, self).__init__(year,month,day)		
		self.busy=[]
		self.free=[i for i in range(9)]


	def getFree_names(self,rooms):
		free=[]
		for i in range(len(self.free)):
			 for room in rooms:
				if (room.id== self.free[i]): 
					free.append(room.name)				
		return free
		
		
	def getBusy_names(self, rooms):
		busy=[]
		for i in range(len(self.busy)):
			 for element in rooms:
				if (element.id== self.busy[i]): 
					busy.append(element.name)				
		return busy



class Reservation(object):
	
	def __init__(self, room_id, f, l, pax, cin, cout, mode):
		self.first_name=f
		self.last_name=l
		self.pax=pax
		self.cin=cin
		self.cout=cout
		self.mode=mode
		
		
