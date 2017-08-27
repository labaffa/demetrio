from datetime import datetime, timedelta
from settings.constants import rooms, DATE_FMT, mandatory_fields, all_fields
from utils.checkers import is_room_available
from utils.formatters import format_date_range, customer_field_formatter, date_or_date_range, set_reservation_template, reservation_from_textline, complete_reservation, string_from_reservation
from utils.generators import date_range, generate_reservations
from classes.demetrio_classes import Reservation


class DataHolder:
    def __init__(self, data_source):
        self.source = data_source 
        self.data = self.reservation_data_builder()
        self.busy_days = self.busy_days_builder(self.data)
        
    def reservation_data_builder(self):
        data = []
        try:
            with open(self.source, 'r') as f:
                lines_list = f.read().splitlines()
                for line in lines_list:
                    reservation = reservation_from_textline(line)
                    data.append(Reservation(reservation))
            f.close()
        # if 'data_source' does not exist create them
        except IOError: 
            print('\'Reservation file\' you have chosen does not exist.'
                  + '\nGoing to create one with a random reservation!')
            data = generate_reservations(self.source, n=1000)
            
        return data
        
    def busy_days_builder(self, reservation_data):
        # Populate the busy_days dictionary
        busy_days = {}
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

    def add_booking_as_text(self, *args, **kw):
        '''
        Method to create a Reservation from given **kw and  write
        its attributes  in 'self.source' as strings. 
        'self.data' and 'self.busy_days' are then updated
        Note: CheckIn and CheckOut must
        '''
        reservation = complete_reservation(kw)
        # Conversion of checkin and checkout
        # to datedatime.date if passed as strings (future use)
        try:
            checkin_date = datetime.strptime(reservation['CheckIn'],
                                             DATE_FMT).date()
        except TypeError:
            checkin_date = reservation['CheckIn']
        try:
            checkout_date = datetime.strptime(reservation['CheckOut'],
                                              DATE_FMT).date()
        except TypeError:
            checkout_date = reservation['CheckOut']
        # Checking room availability
        room_id = reservation['RoomId']
        room_is_available = is_room_available(self.data,
                                              room_id,
                                              checkin_date,
                                              checkout_date)
        if self.data and not room_is_available:
            msg =  (room_id + ' cannot be booked in ' +
                    format_date_range(checkin_date, checkout_date))
            print(msg)
            return False      
        # Setting sequential id 
        last_used_id = int(self.data[-1].id) if self.data else 0
        reservation_id = last_used_id + 1
        reservation['ReservationId'] = reservation_id
        # Appending a fields' values textline to 'self.source'
        with open(self.source, 'a') as f:
            new_reservation_line = string_from_reservation(new_reservation)
            f.write(new_reservation_line)
        # Updating self.data with a Reservation object and
        # self.busy_days
        self.data.append(Reservation(new_reservation))
        for night in date_range(checkin_date, checkout_date):
            dates = list(self.busy_days.keys())
            if night not in dates:
                self.busy_days[night] = [new_reservation['RoomId']]
                dates.append(night)
            else:
                self.busy_days[night].append(new_reservation['RoomId'])
        return

    
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

    def get_availability(self, start_day, end_day, pax=0, return_day_obj=False):
        for room_name in rooms.keys():
            if pax:
                if pax > rooms[room_name]:
                    continue
            available_days = self.get_availability_for_room(room_name, start_day, end_day, return_day_obj=return_day_obj)
            print('Room %s is available on:' % room_name)
            print(available_days)


