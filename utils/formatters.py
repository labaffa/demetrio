from datetime import timedelta
from settings.constants import DATE_FMT, reservation_template, all_fields, mandatory_fields, optional_fields
from collections import OrderedDict


def complete_reservation(incomplete_reservation): 
    '''
    Given a dictionary of variable number of reservation fields, 
    return the same dict but, if any of 'optional_fields' 
    field is missing it will be added with an empty string value.
    Errores raised if mandatories missing or mispelled inserted
    '''
    reservation = {}
    # Adding fields present in 'all_fields' and not given
    for field in mandatory_fields:
        try:
            reservation[field] = incomplete_reservation[field]
            del incomplete_reservation[field]
        except KeyError:
            msg = ('Field \'' + str(field) + '\' is mandatory.' +
                   'Right spellings are: ' + str(mandatory_fields))
            raise KeyError(msg)           
    for field in optional_fields:
        try:
            reservation[field] = incomplete_reservation[field]
            del incomplete_reservation[field]
        except KeyError:
            reservation[field] = ''
    if incomplete_reservation:
        allowed_fields = mandatory_fields + optional_fields
        msg = ('Wrong fields inserted. Allowed fields are: ' +
               str(allowed_fields))
        raise KeyError(msg)
    return reservation


def string_from_reservation(reservation):
    '''
    Given a reservation dict, return a string of all 
    reservation values ('\t' split).
    '''
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
    '''
    Return a reservation dict by taking field values from
    'reservation_line' words.
    If 'reservation_line' is hand-written, pay attention
    that values respect order given in 'all_reservation_fields', 
    to avoid mismatches. 
    '''
    reservation = {}
    reservation_values = reservation_line.split('\t')
    for key, value in zip(all_fields, reservation_values):
        reservation[key] = value
    return reservation

    
def customer_field_formatter(customer_name):
    # Capitalizing just first letter in words (Fix: names as McGregor)
    capital_customer = customer_name.title()
    # Removing unusual spacing (as '   ') between words 
    formatted_name =' '.join(word for word in capital_customer.split())
    return formatted_name


def format_date_range(start, end):
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
