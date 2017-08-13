from settings import rooms # list of SanDemetrio rooms
from names import names # a list of names
from surnames import surnames # a list of surnames

from datetime import datetime, date, timedelta
import random 


class Room:
    def __init__(self, room_name):
        self.name = room_name
        self.no_beds = rooms[room_name]

    # - Returns True if 'self' is free during
    #   the whole interval 'last_day - first_day' (i.e. is bookable)
    def isAvailable(self, data_source,
                    first_day, last_day = None):
        # data_source must be a DataHolder object
        bookings = data_source.data
        if not last_day:
            last_day = first_day  
        for booking in bookings:
            if ((first_day < booking.checkout) and
                (last_day >= booking.checkin)):# overlap
                if (self.name == booking.room.name):
                    print('Room \'' + str(self.name) +
                          '\' is not available.')
                    return False
        return True
        
            
class DataHolder:
    def __init__(self, data_source):
        self.source = data_source 
        self.data = []
        try:
            with open(self.source) as f:
                lines_list = f.read().splitlines()
                for line in lines_list:
                    values = line.split('  ') #two bspaces separation 
                    self.data.append(Reservation(*values))
            f.close()
        # if 'data_source' does not exist bookingGenerator is called
        except IOError: 
            print('\'Reservation file\' you have chosen does not exist.'
                  + '\nGoing to create one with a random reservation!')
            self.bookingGenerator()

    # - Creates n (default=1) Reservation objects with checkin
    #   in a range of 'interval' days from 'today' day onward
    #   and max nights number 'max_no_nights'.
    # - Appends it to 'self.source' containing other reservations.
    #   'data_file' is created if it does not exist.

    
    def bookingGenerator(self,
                         interval = 200, max_no_nights = 15, n = 1):
        for i in range(n):
            room = random.choice(rooms.keys()) #draw of room
            # draws of checkin and checkout
            rand_cin = random.randint(0, interval)
            no_days = random.randint(1, max_no_nights)
            checkin_date = date.today() + timedelta(rand_cin)
            checkout_date = checkin_date + timedelta(no_days)
            checkin = checkin_date.strftime('%Y-%m-%d')
            checkout = checkout_date.strftime('%Y-%m-%d')
            if self.data and not Room(room).isAvailable(self,
                                                        checkin_date,
                                                        checkout_date):
                print(room, checkin, checkout) 
                print('Reservation not possible, sorry.')
                continue
            # reservation_id substitued with this.
            reservation_id = ((int(self.data[-1].id) + 1)
                              if self.data else 1)
            # draws of customer's name and surname
            name = random.choice(names)
            surname = random.choice(surnames)
            customer = str(name) + ' ' + str(surname)
            # optional fields (add date of creation and more optionals)
            pax = random.randint(1, 5)
            parking = random.choice([True, False])#fix: part of staytime
            bookingType = random.choice(['Booking', 'Email', 'Phone'])
            breakfast = random.choice(['No', 'Ticket', 'Room'])
            # Fix: check how to add optional fields and
            # if better creating 'booking' tuple in a loop
            booking = (str(reservation_id), room,  customer,
                       checkin, checkout) 

            with open(self.source, 'a') as f: #appends reservation
                f.write(str(reservation_id) + '  ' +
                        room + '  ' +
                        customer + '  ' +
                        checkin + '  ' +
                        checkout + '\n')
            f.close()
            self.data.append(Reservation(*booking))
        


            
class Reservation:
    def __init__(self, reservation_id, room_name,
                 customer_name, checkin, checkout, **kw):
        self.id = reservation_id
        self.room = Room(room_name)
        self.customer = customer_name
        self.checkin = datetime.strptime(checkin,'%Y-%m-%d').date()
        self.checkout = datetime.strptime(checkout,'%Y-%m-%d').date()



a = DataHolder('test3.dat')
b = a.bookingGenerator()
