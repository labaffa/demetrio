from datetime import datetime

from settings.constants import rooms, DATE_FMT


class Room:
    def __init__(self, room_name):
        self.name = room_name
        self.no_beds = rooms[room_name]
        # TODO Add optional fields

        
class Reservation:
    # Pass OrderedDict
    def __init__(self, reservation): # reservation_id, room_name, name, surname, checkin, checkout, *args):
        self.id = reservation['ReservationId']
        self.room = Room(reservation['RoomId'])
        self.customer = reservation['Name'] + ' ' + reservation['Surname']
        if isinstance(reservation['CheckIn'], str):
            self.checkin = datetime.strptime(reservation['CheckIn'], DATE_FMT).date()
        else:
            self.checkin = reservation['CheckIn']
        if isinstance(reservation['CheckOut'], str):
            self.checkout = datetime.strptime(reservation['CheckOut'], DATE_FMT).date()
        else:
            self.checkout = reservation['CheckOut']
        self.no_nights = self.checkout - self.checkin # a timedelta object
        self.pax = reservation['Pax']
        self.parking = reservation['Parking']
        self.booking_type = reservation['BookingType']
        self.breakfast = reservation['Breakfast']
