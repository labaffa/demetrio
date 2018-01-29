from datetime import datetime
from settings.constants import rooms, DATE_FMT
from enum import Enum


class Room:
    def __init__(self, room_name):
        self.name = room_name
        self.no_beds = rooms[room_name]
        # TODO Add optional fields


class Reservation:
    def __init__(self, reservation):
        self.id = reservation['Id']
        self.room = Room(reservation['RoomId'])
        self.name = reservation['Name']
        self.surname = reservation['Surname']
        self.customer = reservation['Name'] + ' ' + reservation['Surname']
        if isinstance(reservation['CheckIn'], str):
            self.check_in = datetime.strptime(reservation['CheckIn'], DATE_FMT).date()
        else:
            self.check_in = reservation['CheckIn']
        if isinstance(reservation['CheckOut'], str):
            self.check_out = datetime.strptime(reservation['CheckOut'], DATE_FMT).date()
        else:
            self.check_out = reservation['CheckOut']
        self.no_nights = self.check_out - self.check_in # a timedelta object
        self.pax = reservation['Pax']
        self.parking = reservation['Parking']
        self.booking_type = reservation['BookingType']
        self.breakfast = reservation['Breakfast']
        self.status = reservation['Status']


class DemetrioEnum(Enum):
    """Make the string representation of Enum as its value """
    def __str__(self):
        return u'{}'.format(self.value)


class Status(DemetrioEnum):
    active = 1
    deleted = 0
    in_progress = 2
    modified = 3
