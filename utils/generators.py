import random
from datetime import date, timedelta
from settings.names import names # a list of names
from settings.surnames import surnames # a list of surnames 
from settings.constants import rooms
from utils.checkers import is_room_available
from utils.formatters import complete_reservation, string_from_reservation
from classes.demetrio_classes import Reservation, Status

        
def date_range(*args):
    """ Generator of datetime.date objects in a given range of dates
      
    integers:
    date_range(start = 0, end[, step]) -> 'end' dates from today

    datetime.date objects:
    date_range(start = today(), end[,step]) -> 'from today to end' dates
    """
    # Controls on number of given arguments and meaning assignment 
    if len(args) == 1:
        start = date.today()
        stop, = args
        step_days = 1
    elif len(args) == 2:
        start, stop = args
        step_days = 1
    elif len(args) == 3:
        start, stop, step_days = args
    else:
        raise Exception('Wrong number of arguments provided')

    # Converting start and stop in datetime.date object
    # if 'int' is given as the only argument
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
        raise ValueError('Third argument cannot be zero')


def generate_reservations(data_file, interval=200, max_no_nights=15, n=1):
    """ 
    Creates n (default=1) Reservation objects with checkin
    in a range of 'interval' days from 'today' day onward
    and max nights number 'max_no_nights'.
    Save them on 'data_source' as textlines
    """
    reservations = list()
    reservation_id = 0
    with open(data_file, 'a') as f:
        for _ in range(n):
            room_name = random.choice(list(rooms.keys())) #draw of room
            # draws of checkin and checkout
            rand_cin = random.randint(0, interval)
            no_days = random.randint(1, max_no_nights)
            checkin_date = date.today() + timedelta(rand_cin)
            checkout_date = checkin_date + timedelta(no_days)

            room_is_available = is_room_available(reservations, room_name, checkin_date, checkout_date)
            if not room_is_available:
                continue
            reservation_id += 1

            reservation_data = {}
            reservation_data['RoomId'] = room_name
            # draws of customer's name and surname
            reservation_data['Name'] = random.choice(names)
            reservation_data['Surname'] = random.choice(surnames)
            reservation_data['CheckIn'] = checkin_date
            reservation_data['CheckOut'] = checkout_date
            # optional fields
            reservation_data['Pax'] = random.randint(1, 5)
            reservation_data['Parking'] = random.choice([True, False]) # fix: part of staying time
            reservation_data['BookingType'] = random.choice(['Booking', 'Email', 'Phone'])
            reservation_data['Breakfast'] = random.choice(['No', 'Ticket', 'Room'])

            
            booking = complete_reservation(reservation_data)
            # 'ReservtionId' is always assigned after
            # validation and creation of the reservation dict
            # (i.e. after complete_reservation())
            booking['Id'] = reservation_id
            booking['Status'] = str(Status.active)
            reservations.append(Reservation(booking))
            booking_line = string_from_reservation(booking)
            f.write(booking_line)

    f.close()
    return reservations


