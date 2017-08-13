from settings import rooms #list of SanDemetrio rooms
from names import names # a list of names
from surnames import surnames # a list of surnames

from datetime import datetime, date, timedelta
import random 



class Room:
    def __init__(self, room_name):
        self.name = room_name
        self.no_beds = rooms[room_name]


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
        except: 
            print('\'Reservation file\' you have chosen does not exist.'
                  + '\nGoing to create one with a random reservation!')
            self.bookingGenerator()

    # Creates a Reservation with checkin in a range of 'interval' days
    # from 'today' day and max nights number 'max_no_nights'.
    # Appends it to 'self.source' containing other reservations.
    # 'data_file' is created if it does not exist.
    # Returns the Reservation object

    def bookingGenerator(self, interval = 200, max_no_nights = 15):
        try: # sets the sequential 'reservationId'
            with open(self.source) as f:
                last_id_used = len(f.readlines()) 
                reservationId = last_id_used + 1
            f.close()
        except: # if data_file does not exist
            #print('File \'' + str(self.source) + '\' does not exist.' +
                 # ' I\'m going to create it.')
            reservationId = 1

        room = random.choice(rooms.keys()) #draw of room
        # draws of checkin and checkout
        rand_cin = random.randint(0, interval)
        no_days = random.randint(1, max_no_nights)
        checkin_date = date.today() + timedelta(rand_cin)
        checkout_date = checkin_date + timedelta(no_days)
        checkin = checkin_date.strftime('%Y-%m-%d')
        checkout = checkout_date.strftime('%Y-%m-%d')
        # draws of customer's name and surname
        name = random.choice(names)
        surname = random.choice(surnames)
        customer = str(name) + ' ' + str(surname)
        # optional fields
        pax = random.randint(1, 5)
        parking = random.choice([True,False])
        bookingType = random.choice(['Booking', 'Email', 'Phone'])

        # check how to add optional fields and if better creating
        # 'booking' tuple in a loop
        booking = (str(reservationId), room,  customer,
                   checkin, checkout) 

        with open(self.source, 'a') as f: #appends reservation
            f.write(str(reservationId) + '  ' +
                    room + '  ' +
                    customer + '  ' +
                    checkin + '  ' +
                    checkout + '\n')
        f.close()


        return Reservation(*booking)


            
class Reservation:
    def __init__(self, ReservationId, RoomName,
                 CustomerName, Checkin, Checkout, **kw):
        self.id = ReservationId
        self.room = Room(RoomName)
        self.customer = CustomerName
        self.checkin = datetime.strptime(Checkin,'%Y-%m-%d').date()
        self.checkout = datetime.strptime(Checkout,'%Y-%m-%d').date()



