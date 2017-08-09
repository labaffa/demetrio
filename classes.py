import datetime
import pickle
import functions as fn 

class Room:
    def __init__(self,id,name,beds,**kw):
        self.id=id
        self.name=name
        self.beds=beds
        self.file='rooms_list.pickle'

        
class List(object):    
    def __init__(self,**kw):
        #fyear=kw.pop('firstyear',2000)
        #lyear=kw.pop('lastyear',2080)
        self.fyear=2000 #FIX: use default optional kwargs instead
        self.lyear=2080 #FIX: ''   ''      '''       ''     '' 
        self._day=[]
        self._fill_day()
        self._rooms=[]

        
    def _fill_day(self,**kw):
        fday=datetime.date(self.fyear,1,1)
        day=fday 
        while (day.year<self.lyear+1):
             self._day.append(Day(day.year,day.month,day.day))
             day+=datetime.timedelta(1)

    ## Returns Day objects of List in a given range of dates
    def _iter_Day(self, fday,lday):
        d = fn.diff_dates(lday,fday)
        start = self._day.index(fday)
        interval= [day for day in self._day[start:start+d]]
        return interval    


    
class Day(datetime.date):
    def __init__(self,year,month,day):
        super(Day,self).__init__(year,month,day)
        self.busy=[]
        self.free=range(9)
        self.reservations=[]
        self.file='dates_list.pickle'

    

    def getFree_names(self,rooms):#try to rewrite 
        free=[]
        for i in range(len(self.free)):
            for room in rooms:
                if(room.id==self.free[i]):
                    free.append(room.name)
        return free


    def getBusy_names(self, rooms): #try to rewrite
        busy=[]
        for i in range(len(self.busy)):
            for room in rooms:
                if(room.id==self.busy[i]):
                    busy.append(room.name)
        return busy


    
    def getRes_info(self,reservations_list):#print info(won't use this)
        for reservation in reservations_list:
            if reservation.id in self.reservation:
                print(reservation.first_name,
                      reservation.last_name,
                      reservation.cin,
                      reservation.cout)

                
class Reservation(object):
    def __init__(self,id, room_id,f,l,pax,cin,cout,mode):
        self.id=id
        self.room_id=room_id
        self.first_name=f
        self.last_name=l
        self.pax=pax
        self.cout=cout
        self.mode=mode
        self.file='reservations_list.pickle'


