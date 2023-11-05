from django.db import models
from datetime import datetime
from django.utils import timezone

from ticket_details.models import SeatDetails
from ticket_details.utilities.SeatDetailsUtility import SeatDetailsUtility
from BAAS.config import SEAT_CURRENT_STATUS_KEY, SEAT_NUMBER_KEY, SEAT_COACH_KEY
import logging
logger = logging.getLogger(__name__)


class SeatDetailsManager(models.Manager):

    def create_seat_detail_entry(self, seat_details, pnr_entry):
        try:
            seat_entry = SeatDetails()
            seat_entry.pnr = pnr_entry
            seat_no = seat_details.get(SEAT_COACH_KEY) + " " + seat_details.get(SEAT_NUMBER_KEY)
            seat_entry.seat_no = seat_no
            seat_entry.status = seat_details.get(SEAT_CURRENT_STATUS_KEY)
            seat_entry.created_datetime = datetime.now(timezone.get_current_timezone())
            seat_entry.last_updated = datetime.now(timezone.get_current_timezone())
            seat_entry.save()
            return seat_entry
        except Exception as e:
            logger.error(str(e))
            raise Exception(e)

    def update_seat_detail_entry(self, seat_details, pnr_no):
        try:
            result_set = SeatDetailsUtility.get_seat_details_records(pnr_no=pnr_no)
            for seat in result_set:
                seat_no = seat_details.get(SEAT_COACH_KEY) + " " + seat_details.get(SEAT_NUMBER_KEY)
                seat.seat_no = seat_no
                seat.status = seat_details.get(SEAT_CURRENT_STATUS_KEY)
                seat.last_updated = datetime.now(timezone.get_current_timezone())
                seat.save()
            return True
        except Exception as e:
            logger.error(str(e))
            return False