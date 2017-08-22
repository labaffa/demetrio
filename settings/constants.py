# Project constants
from collections import OrderedDict


DATE_FMT = "%Y-%m-%d"

rooms = {"22": 2, "23": 2, "24": 3, "25": 4, "26": 2,
         "Res": 2, "K": 1, "Alby": 2, "8": 3}

reservation_template = OrderedDict({"ReservationId": '', 
                                    "RoomId": '', 
                                    "Name": '', 
                                    "Surname": '', 
                                    "CheckIn": '', 
                                    "CheckOut": '', 
                                    "Pax": '', 
                                    "Parking": '', 
                                    "BookingType": '', 
                                    "Breakfast": ''
                                    })
