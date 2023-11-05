import logging
logger = logging.getLogger(__name__)

from ticket_details.models import SeatDetails
from BAAS.config import PASSENGERS_KEY, CURRENT_STATUS_KEY, SEAT_COACH_KEY, SEAT_CURRENT_STATUS_KEY, SEAT_NUMBER_KEY, \
                        BOOKING_STATUS_KEY, CANCELLED_STATUS, CONFIRMED_STATUS, STATUS_KEY


class SeatDetailsUtility:

    @staticmethod
    def get_seat_details_records(pnr_no):
        try:
            return SeatDetails.objects.filter(pnr=pnr_no)
        except Exception as e:
            logger.error(str(e))
            raise Exception(e)

    @staticmethod
    def get_seat_details_from_pnr_details(pnr_details):
        try:
            passenger_details = pnr_details.get(PASSENGERS_KEY)
            passenger_seat_details_normalised = list()
            for detail in passenger_details: # For each seat detail
                seat_details = detail.get(CURRENT_STATUS_KEY)
                temp = seat_details.split('/')
                if temp[0] != CANCELLED_STATUS: # Cancelled
                    if temp[0] == CONFIRMED_STATUS: # Confirmed
                        seat_details = detail.get(BOOKING_STATUS_KEY)
                        temp = seat_details.split('/')
                    passenger_seat_details_normalised.append({SEAT_CURRENT_STATUS_KEY: temp[0],
                                              SEAT_COACH_KEY : temp[1],
                                              SEAT_NUMBER_KEY: temp[2],
                                             })
            return passenger_seat_details_normalised
        except Exception as e:
            logger.error(str(e))
            raise Exception(e)

    @staticmethod
    def get_seat_details(seat_details):
        try:
            seats = []
            for seat in seat_details:
                temp_seat_details = dict()
                temp_seat_details[SEAT_NUMBER_KEY] = seat.seat_no
                temp_seat_details[STATUS_KEY] = seat.status
                seats.append(temp_seat_details)
            return seats
        except Exception as e:
            logger.error(str(e))
            return None