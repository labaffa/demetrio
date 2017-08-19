from settings import rooms # list of SanDemetrio rooms
from names import names # a list of names
from surnames import surnames # a list of surnames

from datetime import datetime, date, timedelta
import random 

# Evaluates if two couple of checkin-checkout overlap
def isDaysOverlap(start, end, test_start, test_end):
    # Controls
    if (end <= start) or (test_end <= test_start):
        raise ValueError('End of range must be greater than its start')
    # Condition of overlap. Endpoints are checkins and checkouts,
    # so '=' are removed.
    if ((start < test_end) and
        (end > test_start)):
        return True
    else:
        return False

# Return a string with the same content of 'customer_name', 
# first capital letter and single spacing separation.
def customer_field_formatter(customer_name):
    # Capitalizing just first letter in words (Fix: names as McGregor)
    capital_customer = customer_name.title()
    # Removing unusual spacing (as '   ') between words 
    customer_name =' '.join(word for word in capital_customer.split())
    return customer_name
    
    
class Room:
    def __init__(self, room_name):
        self.name = room_name
        self.no_beds = rooms[room_name]

            
class DataHolder:
    def __init__(self, data_source):
        self.source = data_source 
        self.data = []
        self.busy_days = {}
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
            self.bookingGenerator(n=1000)
            
        # Populate the busy_days dictionary
        if len(self.data) > 0:
            dates = list(self.busy_days.keys())
            # Loop over reservations
            for reservation in self.data:
                date = reservation.checkin
                if date not in dates:
                    self.busy_days[date] = [reservation.room.name]
                    dates.append(date)
                else:
                    self.busy_days[date].append(reservation.room.name)
                # Loop over days of a single reservation
                for j in range(1, reservation.no_days.days + 1):
                    next_date = date + timedelta(j)
                    if next_date not in dates:
                        self.busy_days[next_date] = [reservation.room.name]
                        dates.append(next_date)
                    else:
                        self.busy_days[next_date].append(reservation.room.name)

    # - Returns True if Room with 'room_name' is free during
    #   the whole interval 'last_day - first_day' (i.e. is bookable)
    #   and False if not
    def isAvailable(self, room_name, first_day, last_day = None):
        # Controls
        if not isinstance(room_name, str):
            raise TypeError('isAvailable() arg 1 must be a string')
        if room_name not in rooms.keys():
            raise ValueError('Room you inserted does not exist.')
        if (not isinstance(first_day, date) or not
            isinstance(last_day, date)):
            raise TypeError('datetime.date objects are required.')
        if last_day and last_day <= first_day:
            raise ValueError('Second day must be greater than first')
        # Setting variables
        bookings = self.data
        if not last_day:
            last_day = first_day + timedelta(1) # default = 1 night
        # Scanning  reservations
        for booking in bookings:
            test_start = booking.checkin
            test_end = booking.checkout
            test_room = booking.room.name
        # Checking for availability
            if (isDaysOverlap(first_day, last_day,
                              test_start, test_end) and
                (room_name == test_room)): #overlap found->not bookable 
                return False
        return True
                        

      def addBooking_as_text(self, room_name, customer,
                           checkin, nights_or_checkout = None, **kw):
        if not nights_or_checkout:# default = 1 night
            nights_or_checkout = 1
        # Creating checkin date object
        checkin_date = datetime.strptime(checkin, '%Y-%m-%d').date()
        # Creating checkout_date and string field if not given
        if isinstance(nights_or_checkout, int):
            no_nights = nights_or_checkout 
            checkout_date = checkin_date + timedelta(no_nights)
            checkout = checkout_date.strftime('%Y-%m-%d')
        else:# checkout string given
            checkout_date = datetime.strptime(nights_or_checkout,
                                              '%Y-%m-%d').date()
        # Checking if room is available
        if self.data and not self.isAvailable(room_name,
                                              checkin_date,
                                              checkout_date):
            msg =  (room_name + ' is not bookable in ' +
                    rangeFormat(checkin_date, checkout_date))
            print(msg)
            return False      
        # Formatting customer name
        customer = customer_field_formatter(customer)
        # Setting sequential id 
        last_used_id = int(self.data[-1].id) if self.data else 0
        reservation_id = last_used_id + 1
        # Creating and appending Reservation 
        new_reservation = Reservation(reservation_id, room_name,
                                      customer, checkin, checkout)
        with open(self.source, 'a') as f: 
            line = (str(reservation_id) + '  ' + room_name + '  ' +
                    customer + '  ' + checkin + '  ' + checkout + '\n')
            f.write(line)
        f.close()
        self.data.append(new_reservation)
        return new_reservation
                        
    # - Creates n (default=1) Reservation objects with checkin
    #   in a range of 'interval' days from 'today' day onward
    #   and max nights number 'max_no_nights'.
    # - Appends it to 'self.source' containing other reservations.
    #   'data_file' is created if it does not exist.

    def bookingGenerator(self, interval=200, max_no_nights=15, n=1):
        for i in range(n):
            room_ids = list(rooms.keys())
            room = random.choice(room_ids) #draw of room
            # draws of checkin and checkout
            rand_cin = random.randint(0, interval)
            no_days = random.randint(1, max_no_nights)
            checkin_date = date.today() + timedelta(rand_cin)
            checkout_date = checkin_date + timedelta(no_days)
            checkin = checkin_date.strftime('%Y-%m-%d')
            checkout = checkout_date.strftime('%Y-%m-%d')
            if self.data and not self.isAvailable(room,
                                                  checkin_date,
                                                  checkout_date):
                continue
            # reservation_id substitued with this.
            last_used_id = int(self.data[-1].id) if self.data else 0
            reservation_id = last_used_id + 1
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
            
    def get_availability_for_room(self, room_name, start_day, end_day): 
        available_days = list() 
        for day, list_of_busy_rooms in self.busy_days.items():
            if start_day <= day <= end_day:
                if room_name not in list_of_busy_rooms:
                    available_days.append(datetime.strftime(day, '%Y-%m-%d'))
        # day is now at the last busy day
        if start_day > day:
            # The whole period is available!
            from_day = datetime.strftime(start_day, '%Y-%m-%d')
            to_day = datetime.strftime(end_day, '%Y-%m-%d')
            available_days.append(from_day+' - '+to_day)

        print(available_days)


class Reservation:
    def __init__(self, reservation_id, room_name,
                 customer_name, checkin, checkout, **kw):
        self.id = reservation_id
        self.room = Room(room_name)
        self.customer = customer_name
        self.checkin = datetime.strptime(checkin, '%Y-%m-%d').date()
        self.checkout = datetime.strptime(checkout, '%Y-%m-%d').date()
        self.no_days = self.checkout - self.checkin # timedelta object


        
# a = DataHolder('test3.dat')
# b = a.bookingGenerator()
