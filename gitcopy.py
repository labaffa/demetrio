# In settings.constants
mandatory_fields = ['RoomId', 'Name', 'Surname',
                    'CheckIn', 'CheckOut']

optional_fields = ['Pax', 'Parking', 'BookingType', 'Breakfast']

all_fields = ['ReservationId'] + mandatory_fields + optional_fields



# In utils.formatters
def complete_reservation_dict(incomplete_reservation_dict): 
    '''
       Given a dictionary of variable number of reservation fields, 
       return the same dict but, if any of 'all_reservation_fields' 
       field is missing it will be added with an empty string value. 
    '''
    reservation = {}
    # Adding fields present in 'all_fields' and not given
    for field in all_fields:
        try:
            reservation[field] = incomplete_reservation_dict[field]
        except KeyError:
            reservation[field] = ''
    return reservation


# In utils.formatters
def string_from_reservation(reservation_dict):
    '''
       Given a reservation dict, return a string of all 
       reservation values ('\t' split).
    '''
    reservation_line = str()
    last_field_index = len(all_fields) - 1
    for field_index, field in enumerate(all_fields):
        reservation_line += str(reservation_dict[field])
        # Last field without tabbing
        if field_index < last_field_index:
            reservation_line += '\t'
    reservation_line += '\n'
    return reservation_line


# In utils.formatters
def reservation_dict_from_textline(reservation_line):
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


# In utils.generators
def generate_reservations(data_file, interval=200, max_no_nights=15, n=1):
    """ 
    Creates n (default=1) Reservation objects with checkin
    in a range of 'interval' days from 'today' day onward
    and max nights number 'max_no_nights'.
    Appends it to 'self.source' containing other reservations.
    'data_file' is created if it does not exist.
    """
    reservations = list()
    reservation_id = 0
    with open(data_file, 'a') as f:
        for _ in range(n):
            room_name = random.choice(list(rooms.keys())) #draw of room
            # draws of checkin and checkout
            rand_cin = random.randint(0, interval)
            no_days = random.randint(1, max_no_nights)
            checkin_date = date.today() + timedelta(rand_cin)
            checkout_date = checkin_date + timedelta(no_days)

            room_is_available = is_room_available(reservations, room_name, checkin_date, checkout_date)
            if not room_is_available:
                continue
            reservation_id += 1

            reservation_data = OrderedDict()
            reservation_data['ReservationId'] = reservation_id
            reservation_data['RoomId'] = room_name
            # draws of customer's name and surname
            reservation_data['Name'] = random.choice(names)
            reservation_data['Surname'] = random.choice(surnames)
            reservation_data['CheckIn'] = checkin_date
            reservation_data['CheckOut'] = checkout_date
            # optional fields (add date of creation and more optional fields)
            reservation_data['Pax'] = random.randint(1, 5)
            reservation_data['Parking'] = random.choice([True, False]) # fix: part of staying time
            reservation_data['BookingType'] = random.choice(['Booking', 'Email', 'Phone'])
            reservation_data['Breakfast'] = random.choice(['No', 'Ticket', 'Room'])

            booking = complete_reservation_dict(reservation_data)
            reservations.append(Reservation(booking))
            booking_line = string_from_reservation(booking)
            f.write(booking_line)

    f.close()
    return reservations


# DataHolder method
def reservation_data_builder(self):
    data = []
    try:
        with open(self.source, 'r') as f:
            lines_list = f.read().splitlines()
            for line in lines_list:
                reservation = reservation_dict_from_textline(line)
                data.append(Reservation(reservation))
        f.close()
    # if 'data_source' does not exist create them
    except IOError: 
        print('\'Reservation file\' you have chosen does not exist.'
              + '\nGoing to create one with a random reservation!')
        data = generate_reservations(self.source, n=1000)

    return data

# DataHolder method
def add_booking_as_text(self, *args, **kw):
    '''
    Method to create a Reservation from given **kw and  write
    its attributes  in 'self.source' as strings. 
    'self.data' and 'self.busy_days' are then updated
    Note: CheckIn and CheckOut must
    '''

    # Controls on inserted field
    if any(field not in kw.keys() for field in mandatory_fields):
        raise KeyError('Mandatory field missing')
    if any(field not in all_fields for field in kw.keys()):
        raise KeyError('Wrong field inserted. Allowed fields are: '
                       + str(all_fields))

    reservation = kw
    reservation['CheckIn'] = kw['CheckIn'] 
    reservation['CheckOut'] = kw['CheckOut']
    # Conversion of checkin and checkout
    # to datedatime.date if passed as strings (future use)
    try:
        checkin_date = datetime.strptime(kw['CheckIn'],
                                         DATE_FMT).date()
    except TypeError:
        pass
    try:
        checkout_date = datetime.strptime(kw['CheckOut'],
                                          DATE_FMT).date()
    except TypeError:
        pass
    # Checking room availability
    room_is_available = is_room_available(self.data,
                                          reservation['RoomId'],
                                          checkin_date,
                                          checkout_date)
    if self.data and not room_is_available:
        msg =  (reservation['RoomId'] + ' cannot be booked in ' +
                format_date_range(checkin_date, checkout_date))
        print(msg)
        return False      
    # Setting sequential id 
    last_used_id = int(self.data[-1].id) if self.data else 0
    reservation_id = last_used_id + 1
    reservation['ReservationId'] = reservation_id
    # Creating a complete reservation dictionary
    new_reservation = complete_reservation_dict(reservation)
    # Appending a fields' values textline to 'self.source'
    with open(self.source, 'a') as f:
        new_reservation_line = string_from_reservation(new_reservation)
        f.write(new_reservation_line)
    f.close()
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
