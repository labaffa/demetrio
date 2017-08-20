from datetime import timedelta
from settings.constants import DATE_FMT


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
