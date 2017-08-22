from datetime import date, timedelta


#def parse_args():
#    def set_arguments(func, *args):
#        def case(*args):
#            if len(args) == 1:
#                return func(args[0])
#            if len(args) == 2:
#                return 
#            
#        return case
#    
#    return set_arguments
    
    
def date_range(*args):
    """ Generator of datetime.date objects in a given range of dates
        with steps of "step_days".
        Args can be start, stop and step_days. 
        start and stop can be either integers or datetime.date
        if integers: start is "num of days from today"
                     stop is "num of days from start"    
        One arg given: stop (def: start = date.today(), step_days = 1)
        Two args given: start, stop (def: step_days = 1)
        Three args given: start, stop and step_days.
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
