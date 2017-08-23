from datetime import timedelta
from settings.constants import DATE_FMT, reservation_template
from collections import OrderedDict


def set_reservation_template(*reservation_data):
    reservation = OrderedDict()
    res_data = reservation_data[0]
    if isinstance(res_data, OrderedDict):
        for key, value in reservation_template.items():
            if key in res_data and res_data[key]:
                reservation[key] = res_data[key]
            else:
                reservation[key] = value
        return reservation
    else:
        for key, value in zip(reservation_template.keys(), res_data):
            reservation[key] = value
        return reservation

 
def format_reservation_line(reservation):
    reservation_line = str()
    for value in reservation.values():
        reservation_line += str(value)
        reservation_line += '\t'
    reservation_line += '\n'
    return reservation_line

    
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
