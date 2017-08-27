from datetime import timedelta
from settings.constants import rooms


def is_room_available(reservation_data, room_name, first_day, last_day=None):
        """
        Return True if Room with 'room_name' is free during
        the whole interval 'last_day - first_day' 
        (i.e. it can be booked) and False if not.
        """
        if not last_day:
            last_day = first_day + timedelta(1) # default = 1 night
        # Controls
        if room_name not in rooms.keys():
            raise KeyError('Room you inserted does not exist.')
        if last_day <= first_day:
            raise ValueError('Second day must be greater than first.')
    
        # Scanning  reservations
        for booking in reservation_data:
            test_start = booking.checkin
            test_end = booking.checkout
            test_room = booking.room.name
            # Checking for availability
            days_overlap = is_days_overlap(first_day, last_day, test_start, test_end)
            if days_overlap and room_name == test_room:
                return False
        return True
    

def is_days_overlap(start, end, test_start, test_end):
    """ Check if two checkin-checkout intervals overlap """
    # End points are checkins and checkouts,
    # so '=' are removed.
    if ((start < test_end) and (end > test_start)):
        return True
    else:
        return False
    
