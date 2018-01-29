from datetime import timedelta
from settings.constants import DATE_FMT, all_fields, mandatory_fields, optional_fields
from collections import OrderedDict
from utils.checkers import validate_date
from classes.demetrio_classes import Reservation, Status
import os
import re

get_first_value = lambda x: x.split('\t')[0]
get_last_value = lambda x: x.split('\t')[-1]

def complete_reservation(incomplete_reservation): 
    """
    Given a dictionary of variable number of reservation fields, 
    return the same dict but, if any of 'optional_fields' 
    field is missing it will be added with an empty string value.
    Errors raised if mandatories missing or mispelled inserted
    """
    reservation = {}
    # Inserting mandatory fields
    for field in mandatory_fields:
        try:
            reservation[field] = incomplete_reservation[field]
            del incomplete_reservation[field]
        except KeyError:
            msg = ('Field \'' + str(field) + '\' is mandatory.' +
                   'Right spellings are: ' + str(mandatory_fields))
            raise KeyError(msg)
    # Inserting optional fields
    for field in optional_fields:
        reservation[field] = incomplete_reservation.pop(field, '')
    if incomplete_reservation:
        allowed_fields = mandatory_fields + optional_fields
        msg = ('Wrong fields inserted. Allowed fields are: ' +
               str(allowed_fields))
        raise KeyError(msg)
    return reservation


def string_from_reservation(reservation):
    """
    Given a reservation dict, return a string of all 
    reservation values ('\t' split).
    """
    # datetime.date -> str()
    reservation['CheckIn'] = reservation['CheckIn'].strftime(DATE_FMT)
    reservation['CheckOut'] = reservation['CheckOut'].strftime(DATE_FMT)
    # Writing field values in one textline
    reservation_line = str()
    last_field_index = len(all_fields) - 1
    for field_index, field in enumerate(all_fields):
        reservation_line += str(reservation[field])
        # Last field without tabbing
        if field_index < last_field_index:
            reservation_line += '\t'
    reservation_line += '\n'
    return reservation_line


def reservation_from_textline(reservation_line):
    """
    Return a reservation dict by taking field values from
    'reservation_line' words.
    If 'reservation_line' is hand-typed, pay attention
    that values respect order given in 'all_fields' 
    to avoid mismatches. 
    """
    reservation = {}
    reservation_values = reservation_line.split('\t')
    for key, value in zip(all_fields, reservation_values):
        reservation[key] = value
    # checkin, checkout -> datetime.date conversion
    reservation['CheckIn'] = validate_date(reservation['CheckIn'])
    reservation['CheckOut'] = validate_date(reservation['CheckOut'])
    return reservation

    
def customer_field_formatter(customer_name):
    # Capitalizing just first letter in words (Fix: names as McGregor)
    capital_customer = customer_name.title()
    # Removing unusual spacing (as '   ') between words 
    formatted_name =' '.join(word for word in capital_customer.split())
    return formatted_name


def format_date_range(start, end):
    """
    Return a 'range format' if end and start are different dates,
    and start/end otherwise
    """
    if start == end:
        formatted_date = start.strftime(DATE_FMT)
        return formatted_date
    else:
        from_date = start.strftime(DATE_FMT)
        to_date = end.strftime(DATE_FMT)
        formatted_range = from_date + " - " + to_date
    return formatted_range


def date_or_date_range(ordered_dates):
    """
    From a list of datetime objects return a list of date strings.
    As a date range if consecutive days found.  
    """
    date_ranges = []
    range_start = ordered_dates.pop(0)
    range_end = range_start 
    for date in ordered_dates:
    # A hole
        if date - range_end > timedelta(1):
            date_ranges.append(format_date_range(range_start, range_end))
            range_start = date
            range_end = range_start
            continue
        else:
        # Two consecutive days
            range_end = date 
    # Append the last dates left
    date_ranges.append(format_date_range(range_start, range_end))
    return date_ranges


def rename_to_bak_file(source_file):
    """    'Source_root.extension' -> 'Source_root.bak' """

    origin_file = str(source_file)
    root = "".join(origin_file.split('.')[:-1])
    backup_file = root + '.bak'
    os.rename(origin_file, backup_file)
    return backup_file


def reservation_dict_builder(incomplete_reservation, source_list=None,
                             specific_id=None):
    """
    Return a Reservation dict built from given incomplete_reservation 
    with ID assignement based on source_list element count.

    Specific_id should be passed in case of reservation modifications
    (see for example 'modify_reservation' method in DataHolder class

    """
    
    if specific_id:
        reservation_id = specific_id
    else:
        last_used_id = int(source_list[-1].id) if source_list else 0
        reservation_id = last_used_id + 1
    reservation = complete_reservation(incomplete_reservation)
    reservation['Id'] = reservation_id        
    reservation['Status'] = str(Status.active)
    return reservation


def snake_from_camel(camel_string):
    """ CamelString -> camel_string """

    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def camel_from_snake(snake_string):
    """ snake_string -> SnakeString """
    
    camel_string = snake_string.title()
    splits_number = 0
    for index, char in enumerate(snake_string):
        if char == '_':
            split_pos = index - splits_number
            camel_string = (camel_string[:split_pos] +
                            camel_string[split_pos + 1:].title())
            splits_number += 1
    return camel_string if splits_number else snake_string


def dict_from_reservation_object(reservation_obj):
    """
    Return same dictionary used to create 'reservation_obj'
    Can be seen as inverse operation of Reservation(dict)

    """
    
    reservation_dict = {}
    reservation_dict['RoomId'] = reservation_obj.room.name
    for attr, value in vars(reservation_obj).items():
        for field in all_fields:
            if str(attr) == snake_from_camel(field):
                reservation_dict[field] = value
    return reservation_dict


