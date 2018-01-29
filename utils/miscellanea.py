from classes.demetrio_classes import Reservation, Status, Room
from utils.generators import date_range
from utils.formatters import dict_from_reservation_object, \
    string_from_reservation


# TODO: decide if some of following functions are better as data_holder
#       methods

def set_to_modified(reservation_number, reservation_list,
                    status=str(Status.active)):
    """
    Set Status of reservation with 'reservation_number' ID and
    'status' Status of the given 'reservation_list' to 'modified'
    Return reservation_list

    """
    
    for reservation in reservation_list:
        if ((reservation.id == str(reservation_number)) and
            (reservation.status == str(status))):
            reservation.status = str(Status.modified)
    return reservation_list


def set_to_deleted(reservation_number, reservation_list,
                   status=str(Status.active)):
    """
    Set Status of reservation with 'reservation_number' ID and
    'status' Status of the given 'reservation_list' to 'deleted'
    Return reservation_list

    """
    
    for reservation in reservation_list:
        if ((reservation.id == str(reservation_number)) and
            (reservation.status == str(status))):
            reservation.status = str(Status.deleted)
    return reservation_list


def set_to_active(reservation_number, reservation_list,
                  status=str(Status.deleted)):
    """
    Set Status of reservation with 'reservation_number' ID and
    'status' Status of the given 'reservation_list' to 'active'
    Return reservation_list

    """
    
    for reservation in reservation_list:
        if ((reservation.id == str(reservation_number)) and
            (reservation.status == str(status))):
            reservation.status = str(Status.active)
    return reservation_list


def data_on_file(source_file, reservation_list):
    """ Write a reservation_list on given source_file """
    
    with open(source_file, 'w') as f:
        for reservation in reservation_list:
            reservation_dict = dict_from_reservation_object(reservation)
            reservation_line = string_from_reservation(reservation_dict)
            f.write(reservation_line)


def remove_days_from_busy(reservation_number, reservation_list,
                          busy_days_dict):
    """
    For the checkin-checkout period of the reservation with 
    'reservation_number' ID, remove the corresponding room from 
    'busy_days_dict' and return it

    """
    
    for reservation in reservation_list:
        if ((reservation.id == str(reservation_number)) and
            (reservation.status == str(Status.active))):
            start, stop  = reservation.check_in, reservation.check_out
            room = reservation.room.name
            for date in date_range(start, stop):
                busy_days_dict.remove(room)
    return busy_days_dict


