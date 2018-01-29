from datetime import timedelta
from settings.constants import rooms
from utils.checkers import is_room_available
from utils.formatters import format_date_range, date_or_date_range, reservation_from_textline, complete_reservation, rename_to_bak_file, \
    reservation_dict_builder, string_from_reservation, \
    get_first_value, get_last_value
from utils.miscellanea import set_to_active, set_to_deleted, \
    set_to_modified, data_on_file
from utils.generators import date_range, generate_reservations
from classes.demetrio_classes import Reservation, Status
import os


class DataHolder:
    def __init__(self, data_source):
        self.source = data_source
        self.data = self.reservation_data_builder()
        self.busy_days = self.busy_days_builder(self.data)

    def reservation_data_builder(self):
        """
        Populate list of Reservation objects from data_source or
        create a new one if data_source does not exist
        """
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
        """Populate the busy_days dictionary

        keys: dates with at least one room booked
        values: list of rooms booked for the 'key' night
        """
        busy_days = {}
        if len(reservation_data) > 0:
            dates = list(busy_days.keys())
            # Loop over reservations
            for reservation in reservation_data:
                if reservation.status == str(Status.active):
                    date = reservation.check_in
                    if date not in dates:
                        busy_days[date] = [reservation.room.name]
                        dates.append(date)
                    else:
                        busy_days[date].append(reservation.room.name)
                        # Loop over days of a single reservation if no_of_nights > 1
                    number_of_nights = reservation.no_nights.days
                    if number_of_nights == 1:
                        continue
                    for j in range(1, number_of_nights):
                        next_date = date + timedelta(j)
                        if next_date not in dates:
                            busy_days[next_date] = [reservation.room.name]
                            dates.append(next_date)
                        else:
                            busy_days[next_date].append(reservation.room.name)
        return busy_days

    def add_booking_as_text(self, *args, **kw):
        """Create Reservation object from 'kw' and save it as text

        keywords = 'mandatory_fields + optional_fields' elements
        'self.data' and 'self.busy_days' update
        Note: CheckIn and CheckOut must be datetime.date objects
        """
        new_reservation = complete_reservation(kw)
        checkin_date = new_reservation['CheckIn']
        checkout_date = new_reservation['CheckOut']
        # Checking room availability
        room_id = new_reservation['RoomId']
        room_is_available = is_room_available(self.data,
                                              room_id,
                                              checkin_date,
                                              checkout_date)
        if self.data and not room_is_available:
            msg = (room_id + ' cannot be booked in ' +
                   format_date_range(checkin_date, checkout_date))
            print(msg)
            return False
        # Setting sequential id
        last_used_id = int(self.data[-1].id) if self.data else 0
        new_reservation_id = last_used_id + 1
        new_reservation['Id'] = new_reservation_id
        new_reservation['Status'] = str(Status.active)
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
        """Return a list of free dates for a room in a given period

        If return_day_obj = True consecutives dates are given in range
        format
        Check well, It feels buggy!!
        """
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
        """Same of get_availability_for_room but applied to all rooms"""
        for room_name in rooms.keys():
            if pax:
                if pax > rooms[room_name]:
                    continue
            available_days = self.get_availability_for_room(room_name, start_day, end_day, return_day_obj=return_day_obj)
            print('Room %s is available on:' % room_name)
            print(available_days)

    def delete_reservation(self, reservation_number):
        """
        -Set Status of reservation with id 'reservation_id' to 'deleted'
        -A backup file is created first for extra safety.
        -self.data and self.busy_days are then reloaded
        """
        # first create name for backup file
        origin_file_name = self.source
        root = origin_file_name.split('.')[0]
        backup_file_name = root + '.bak'
        # and now rename the source with the backup name
        os.rename(self.source, backup_file_name)
        # Once data are backuped we rewrite the source with
        # a new reservation status
        with open(backup_file_name, 'r') as b: # reading backup
            with open(self.source, 'a') as f: # writing new file
                lines_list = b.read().splitlines()
                for line in lines_list:
                    res_id = get_first_value(line)
                    res_status = get_last_value(line)
                    if  (res_id == str(reservation_number) and
                         res_status == str(Status.active)):
                        line = line[:-1] + str(Status.deleted)
                    f.write(line + '\n')
        # update data_holder
        self.data = self.reservation_data_builder() 
        self.busy_days = self.busy_days_builder(self.data)        

    def modify_reservation(self, reservation_number, *args, **kw):
        """
        -Reservation with reservation_id is substituted by 
        a reservation formed from kw dictionary.

        -New reservation is written on source-file, after backup, in 
        a consecutive row, with same ID (the old one is not deleted).

        TODO: store old reservations  in 'history' 
        reservation attribute

        """
        # temporarily delete reserve we want to modify
        self.data = set_to_deleted(reservation_number, self.data)
        modified_dict = reservation_dict_builder(kw,
                                                 source_list=self.source,
                                                 specific_id=reservation_number)
        modified_reservation = Reservation(modified_dict)

        # check if new modified reservation is possible
        checkin = modified_reservation.check_in # datetime.date object
        checkout = modified_reservation.check_out
        room_id = modified_reservation.room.name
        available = is_room_available(self.data, room_id, checkin,
                                      checkout, msg=room_id +
                                      ' is not available ' +
                                      format_date_range(checkin,
                                                        checkout))
        # If modifications are not possible we reset
        # old reserve to 'active' and quit 
        if not available:
            self.data = set_to_active(reservation_number, self.data)
            self.busy_days = self.busy_days_builder(self.data)
            return False
        # if it's bookable we set status of the old reserve
        # to 'modified' and then build new reservation up...
        self.data = set_to_modified(reservation_number, self.data,
                                    status=Status.deleted)

        # insert modified-version as last element
        # with reservation_number ID
        inserted = False 
        for index, reservation in enumerate(self.data):
            # we insert reservation just before the next one
            # in order to keep a chronological order of modifications
            # within elements of the Reservation list
            if str(reservation.id) == str(int(reservation_number) + 1):
                self.data.insert(index, modified_reservation)
                inserted = True
                break
        if not inserted: # i.e. reserve to modify is last in the list 
            self.data.insert(len(self.data), modified_reservation)

        # backup and update
        backup_file_name = rename_to_bak_file(self.source)
        data_on_file(self.source, self.data)
        self.busy_days = self.busy_days_builder(self.data)
