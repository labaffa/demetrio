 # Copy this as a DataHolder method. Returns a dict of room names as keys and 
 # lists of dates ranges where room is available
 
    def getAvailabilityforRooms(self, first_day, last_day = None,
                                room_name = None):
        bookings = self.data #list of Reservation
        if not last_day:#default last_day
            last_day = first_day + timedelta(1)
            
        #setting the dict of rooms to check for availability
        free_rooms_list = {} #dict of rooms and days when free
        if not room_name: #all the rooms checked
            for key in rooms.keys():
                free_rooms_list.setdefault(key, []).append((first_day,
                                                            last_day))
        else: #just room_name checked
            free_rooms_list.setdefault(room_name,[]).append((first_day,
                                                             last_day))

        for booking in bookings:#scanning reservations
            test_room = booking.room.name #room of the scanned reserve
            if test_room not in free_rooms_list.keys():
                continue
            test_interval = (booking.checkin, booking.checkout)
            intervals = free_rooms_list[test_room]#scan room's interval
            free = [] #a provv list of intervals where room is free
            not_free = [] #a provv list of busy intervals
            for interval in intervals:# the algorythm
                if (isDaysOverlap(interval[0], interval[1],
                                  test_interval[0], test_interval[1])):
                    not_free.append(interval)
                    case_a = ((interval[0] >= test_interval[0]) and
                              (interval[1] <= test_interval[1]))
                    case_b = ((interval[0] < test_interval[0]) and
                              (interval[1] > test_interval[1]))
                    case_c = ((interval[0] > test_interval[0]) and
                              (interval[1] > test_interval[1]))
                    case_d = ((interval[0] < test_interval[0]) and
                              (interval[1] < test_interval[1]))

                    if case_b:
                        interval_1 = (interval[0], test_interval[0])
                        interval_2 = (test_interval[1], interval[1])
                        free.append(interval_1)
                        free.append(interval_2)

                    elif case_c:
                        interval_1 = (test_interval[1], interval[1])
                        free.append(interval_1)

                    elif case_d:
                        interval_1 = (interval[0], test_interval[0])
                        free.append(interval_1)

            for interval in not_free:
                intervals.remove(interval)#not a free interval
            for interval in free:
                intervals.append(interval)#maybe a free interval
        return free_rooms_list
