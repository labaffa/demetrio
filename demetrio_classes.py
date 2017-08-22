from datetime import datetime, date, timedelta
import random

from settings.constants import rooms, DATE_FMT
from settings.names import names # a list of names
from settings.surnames import surnames # a list of surnames 
from utils.formatters import customer_field_formatter, format_date_range, date_or_date_range, \
    set_reservation_template, format_reservation_line
from utils.generators import date_range
from utils.checkers import is_room_available


class Room:
    def __init__(self, room_name):
        self.name = room_name
        self.no_beds = rooms[room_name]
        # TODO Add optional fields

        
class Reservation:
    def __init__(self, reservation_id, room_name, name, surname, checkin, checkout, *args):
        self.id = reservation_id
        self.room = Room(room_name)
        self.customer = name + ' ' + surname
        self.checkin = datetime.strptime(checkin, DATE_FMT).date()
        self.checkout = datetime.strptime(checkout, DATE_FMT).date()
        self.no_nights = self.checkout - self.checkin # a timedelta object
        
           
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
                    values = line.split('\t') 
                    values.remove('') 
                    data.append(Reservation(*values))
            f.close()
        # if 'data_source' does not exist create them
        except IOError: 
            print('\'Reservation file\' you have chosen does not exist.'
                  + '\nGoing to create one with a random reservation!')
            data = self.generate_reservations(n=1000)
            
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

    def add_booking_as_text(self, room_name, customer,
                           checkin, nights_or_checkout=1, **kw):
        """ Once checked for room availability, creates a 
            Reservation object from given fields.
            Update self.data and self.busy_days
        """
        # Creating checkin date object
        checkin_date = datetime.strptime(checkin, DATE_FMT).date() 
        # Creating checkout_date and string field if not given
        if isinstance(nights_or_checkout, int):
            no_nights = nights_or_checkout 
            checkout_date = checkin_date + timedelta(no_nights)
            checkout = checkout_date.strftime(DATE_FMT)
        else:
            checkout_date = datetime.strptime(nights_or_checkout, DATE_FMT).date()
        # Checking if room is available
        room_is_available = is_room_available(self.data, room_name, checkin_date, checkout_date)
        if self.data and not room_is_available:
            msg =  (room_name + ' cannot be booked in ' +
                    format_date_range(checkin_date, checkout_date))
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
    
    def generate_reservations(self, interval=200, max_no_nights=15, n=1):
        """ Creates n (default=1) Reservation objects with checkin
            in a range of 'interval' days from 'today' day onward
            and max nights number 'max_no_nights'.
            Appends it to 'self.source' containing other reservations.
            'data_file' is created if it does not exist.
        """
        reservations = list() 
        for _ in range(n):
            room = random.choice(list(rooms.keys())) #draw of room
            # draws of checkin and checkout
            rand_cin = random.randint(0, interval)
            no_days = random.randint(1, max_no_nights)
            checkin_date = date.today() + timedelta(rand_cin)
            checkout_date = checkin_date + timedelta(no_days)
            checkin = checkin_date.strftime(DATE_FMT)
            checkout = checkout_date.strftime(DATE_FMT)
            
            try:
                if self.data:
                    room_is_available = is_room_available(self.data, room, checkin_date, checkout_date)
                    last_used_id = int(self.data[-1].id)
                    if not room_is_available:
                        continue
            except AttributeError:
                last_used_id = 0

            reservation_id = last_used_id + 1
            # draws of customer's name and surname
            name = random.choice(names)
            surname = random.choice(surnames)
            # optional fields (add date of creation and more optional fields)
            pax = random.randint(1, 5)
            parking = random.choice([True, False]) # fix: part of staying time
            booking_type = random.choice(['Booking', 'Email', 'Phone'])
            breakfast = random.choice(['No', 'Ticket', 'Room'])
            
            booking = set_reservation_template(reservation_id, 
                                               room, name, surname, checkin, checkout, pax, parking, booking_type, breakfast)
            with open(self.source, 'a') as f:
                f.writelines(format_reservation_line(booking))
            f.close()

            reservations.append(Reservation(*booking.values()))

        return reservations
    
    
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
