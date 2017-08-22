from datetime import datetime, date, timedelta
import random

from settings.constants import rooms, DATE_FMT # list of SanDemetrio rooms
from settings.names import names # a list of names
from settings.surnames import surnames # a list of surnames 
from utils.formatters import format_date_range, date_or_date_range

def date_range(*args):
    ''' Generator of datetime.date objects in a given range of dates
        with steps of "step_days".
        Args can be start, stop and step_days. 
        start and stop can be either integers or datetime.date
        if integers: start is "num of days from today"
                     stop is "num of days from start"    
        One arg given: stop (def: start = date.today(), step_days = 1)
        Two args given: start, stop (def: step_days = 1)
        Three args given: start, stop and step_days'''
    # Controls on number of given arguments and meaning assignement 
    if len(args) == 1:
        start = date.today()
        stop, = args
        step_days = 1
    elif len(args) == 2:
        start, stop = args
        step_days = 1
    elif len(args) == 3:
        start, stop, step_days = args
    if len(args) > 0 and len(args) < 4:
        # Converting start and stop in datetime.date object
        # if 'int' is given
        try:
            days_from_today = start
            start = date.today() + timedelta(days_from_today)
        except TypeError:
            pass
        try:
            no_days = stop
            stop = start + timedelta(no_days)
        except TypeError:
            pass
        # Generating days
        current = start
        step = timedelta(step_days)
        if step_days > 0:
            while current < stop:
                yield current
                current += step
        elif step_days < 0:
            while current > stop:
                yield current
                current += step
        else:
            raise ValueError('step_days must not be zero')
        
def is_days_overlap(start, end, test_start, test_end):
    ''' Given two intervals it checks if they overlap'''
    
    # Condition of overlap. Endpoints are checkins and checkouts,
    # so '=' are removed.
    if ((start < test_end) and
        (end > test_start)):
        return True
    else:
        return False

def customer_field_formatter(customer_name):
    # Capitalizing just first letter in words (Fix: names as McGregor)
    capital_customer = customer_name.title()
    # Removing unusual spacing (as '   ') between words 
    formatted_name =' '.join(word for word in capital_customer.split())
    return formatted_name

class Room:
    def __init__(self, room_name):
        self.name = room_name
        self.no_beds = rooms[room_name]

        
            
class DataHolder:
    def __init__(self, data_source):
        self.source = data_source 
        self.data = self.reservation_data_builder()
        self.busy_days = self.busy_days_builder(self.data)
        
    def reservation_data_builder(self):
        data = []
        try:
            with open(self.source) as f:
                lines_list = f.read().splitlines()
                for line in lines_list:
                    values = line.split('  ') # two blank spaces separation 
                    data.append(Reservation(*values))
            f.close()
        # if 'data_source' does not exist bookingGenerator is called
        except IOError: 
            print('\'Reservation file\' you have chosen does not exist.'
                  + '\nGoing to create one with a random reservation!')
            self.bookingGenerator(n=1000)
            
        return data
        
    def busy_days_builder(self, reservation_data):
        busy_days = {}
    # Populate the busy_days dictionary
        if len(reservation_data) > 0:
            dates = list(busy_days.keys())
            # Loop over reservations
            for reservation in reservation_data:
                date = reservation.checkin
                if date not in dates:
                    busy_days[date] = [reservation.room.name]
                    dates.append(date)
                else:
                    busy_days[date].append(reservation.room.name)
                # Loop over days of a single reservation if no_of_nights > 1
                number_of_nights = reservation.no_nights.days
                if number_of_nights == 1:
                    continue
                for j in range(1,  number_of_nights):
                    next_date = date + timedelta(j)
                    if next_date not in dates:
                        busy_days[next_date] = [reservation.room.name]
                        dates.append(next_date)
                    else:
                        busy_days[next_date].append(reservation.room.name)
            
        return busy_days

    
    def is_available(self, room_name, first_day, last_day = None):
        ''' Return True if Room with 'room_name' is free during
            the whole interval 'last_day - first_day'(i.e. is bookable) 
            and False if not '''

        # Setting variables
        bookings = self.data
        if not last_day:
            last_day = first_day + timedelta(1) # default = 1 night
        # Controls
        if room_name not in rooms.keys():
            raise ValueError('Room you inserted does not exist.')
        if last_day <= first_day:
            raise ValueError('Second day must be greater than first')
    
        # Scanning  reservations
        for booking in bookings:
            test_start = booking.checkin
            test_end = booking.checkout
            test_room = booking.room.name
        # Checking for availability
            if (is_days_overlap(first_day, last_day,
                              test_start, test_end) and
                (room_name == test_room)): #overlap found->not bookable 
                return False
        return True

    def add_booking_as_text(self, room_name, customer,
                           checkin, nights_or_checkout = None, **kw):
        ''' Once checked for room availability, creates a 
            Reservation object from given fields.
            Appends it to self.data and updates self.busy_days'''
        
        # Creating checkin date object
        checkin_date = datetime.strptime(checkin, '%Y-%m-%d').date() 
        if not nights_or_checkout:# default = 1 night
            nights_or_checkout = 1
        # Creating checkout_date and string field if not given
        if isinstance(nights_or_checkout, int):
            no_nights = nights_or_checkout 
            checkout_date = checkin_date + timedelta(no_nights)
            checkout = checkout_date.strftime('%Y-%m-%d')
        else:
            checkout_date = datetime.strptime(nights_or_checkout,
                                              '%Y-%m-%d').date()
        # Checking if room is available
        if self.data and not self.is_available(room_name,
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
        
        new_reservation = Reservation(reservation_id, room_name,
                                      customer, checkin, checkout)
        with open(self.source, 'a') as f: #appends reservation
            line = (str(reservation_id) + '  ' + room_name + '  ' +
                    customer + '  ' + checkin + '  ' + checkout + '\n')
            f.write(line)
            
        f.close()
        # Updating self.data and self.busy_days
        self.data.append(new_reservation)
        for night in date_range(checkin_date, checkout_date):
            dates = list(self.busy_days.keys())
            if night not in dates:
                self.busy_days[night] = [room_name]
                dates.append(night)
            else:
                self.busy_days[night].append(room_name)
        return
    
    
    
     def bookingGenerator(self,
                         interval = 200, max_no_nights = 15, n = 1):
        '''Creates n (default=1) Reservation objects with checkin
           in a range of 'interval' days from 'today' day onward
           and max nights number 'max_no_nights'.
           Appends it to 'self.source' containing other reservations.
           'data_file' is created if it does not exist.'''

        for _ in range(n):
            room = random.choice(rooms.keys()) #draw of room
            # draws of checkin and checkout
            rand_cin = random.randint(0, interval)
            no_days = random.randint(1, max_no_nights)
            checkin_date = date.today() + timedelta(rand_cin)
            checkout_date = checkin_date + timedelta(no_days)
            checkin = checkin_date.strftime('%Y-%m-%d')
            checkout = checkout_date.strftime('%Y-%m-%d')
            if self.data and not self.is_available(room,
                                                  checkin_date,
                                                  checkout_date):
                print(self.is_available(room, checkin_date, checkout_date))
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
            # Updating self.data and self.busy_days
            self.data.append(Reservation(*booking))
            for night in date_range(checkin_date, checkout_date):
                dates = list(self.busy_days.keys())
                if night not in dates:
                    self.busy_days[night] = [room]
                    dates.append(night)
                else:
                    self.busy_days[night].append(room)

            
    def get_availability_for_room(self, room_name, start_day, end_day, return_day_obj=False): 
        available_days = list() 
        for day, list_of_busy_rooms in self.busy_days.items():
            if start_day <= day < end_day:
                if room_name not in list_of_busy_rooms:
                    available_days.append(day)
        
        # day is now at the last busy day
        if start_day > day:
            # The whole period is available!
            available_days.append(format_date_range(start_day, end_day))
            return available_days
        
        if not return_day_obj:
            return date_or_date_range(sorted(available_days))
        else:
            return sorted(available_days)
    
        
class Reservation:
    def __init__(self, reservation_id, room_name,
                 customer_name, checkin, checkout, **kw):
        self.id = reservation_id
        self.room = Room(room_name)
        self.customer = customer_name
        self.checkin = datetime.strptime(checkin, '%Y-%m-%d').date()
        self.checkout = datetime.strptime(checkout, '%Y-%m-%d').date()
        self.no_nights = self.checkout - self.checkin # a timedelta object


# a = DataHolder('test3.dat')
# b = a.bookingGenerator()
