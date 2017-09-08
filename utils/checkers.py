from datetime import timedelta, date, datetime
from settings.constants import rooms, DATE_FMT


def validate_date(date_input):
    """str -> datetime.date; datetime.date -> do nothing"""
    if isinstance(date_input, date):
        return
    if isinstance(date_input, str):
        return datetime.strptime(date_input, DATE_FMT).date()
    raise ValueError('Data not understood')


def validate_datetime(date_input):
    """str -> datetime.datetime; datetime.datetime -> do nothing"""
    if isinstance(date_input, datetime):
        return
    if isinstance(date_input, str):
        return datetime.strptime(date_input, DATE_FMT)
    raise ValueError('Data not understood')


def is_room_available(reservation_data, room_name, first_day, last_day=None):
        """
        Return True if Room with 'room_name' is free during
        the whole interval 'last_day - first_day'
        (i.e. it can be booked) and False if not.
        """
        if not last_day:
            last_day = first_day + timedelta(1)  # default = 1 night
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
