 # Copy this as a DataHolder method. Returns a dict of room names as keys and 
 # lists of dates ranges where room is available
 ## Fix: indentation shifted by 4
    def getFreeRooms(self, first_day, last_day = None,
                     room_name = None):
        bookings = self.data #list of Reservation
        if not last_day: #default last_day
            last_day = first_day + timedelta(1)
        
        #setting the dict of rooms to check for availability
        free_rooms_list = {} #dict of rooms and days when free
        if not room_name:# check all rooms
            for key in rooms.keys():#init with entire interval of dates
                free_rooms_list.setdefault(key, []).append((first_day,
                                                            last_day))
        else:# check just given room
            free_rooms_list.setdefault(room_name,[]).append((first_day,
                                                             last_day))

        for booking in bookings:#scanning reservations
            test_room = booking.room.name #room of the scanned reserve
            if test_room not in free_rooms_list.keys():
                continue
            # (checkin, checkout) of 'booking' to compare to 
            test_interval = (booking.checkin, booking.checkout)
            # list of intervals belonging to the current scanned room
            intervals = free_rooms_list[test_room]
            free = [] #a provv list of intervals where room is free
            not_free = [] #a provv list of busy intervals
            
            # The algorithm: (first_day, last_day) range  is
            # tested  by checking if it overlaps  with the 
            # checkin-ckeckout interval of the current booking.
            # Depending on if/how they overlap, (first_day, last_day)
            # is divided (or rejected if included) into
            # smaller intervals that are still potentially free.
            # Such smaller intervals are then tested on the next
            # booking, by applying the same principle.
            # At the end of the loop over all bookings
            # we obtain, for each room, a list of intervals
            # where they are available.
            for interval in intervals:
                start_range, end_range = interval
                start_scan, end_scan = test_interval
                if (isDaysOverlap(start_range, end_range,
                                  start_scan, end_scan)):
                    not_free.append(interval)
                    #       |-----------|          interval
                    #   |------------------|      test_interval
                    case_a = ((start_range >= start_scan) and
                              (end_range <= end_scan))
                    #       |-----------|          interval
                    #           -----              test_interval
                    case_b = ((start_range < start_scan) and
                              (end_range > end_scan))
                    #       |-----------|          interval
                    #   |---------                 test_interval
                    case_c = ((start_range >= start_scan) and
                              (end_range > end_scan))
                    #       |-----------|          interval
                    #              ----------|     test_interval
                    case_d = ((start_range < start_scan) and
                              (end_range <= end_scan))
                    
                    if case_b:
                        interval_1 = (start_range, start_scan)
                        interval_2 = (end_scan, end_range)
                        free.append(interval_1)
                        free.append(interval_2)
                    elif case_c:
                        interval_1 = (end_scan, end_range)
                        free.append(interval_1)
                    elif case_d:
                        interval_1 = (start_range, start_scan)
                        free.append(interval_1)

            for interval in not_free:
                intervals.remove(interval)#not a free interval
            for interval in free:
                intervals.append(interval)#maybe a free interval
        return free_rooms_list
