from django.db import models
from datetime import datetime
from django.utils import timezone

from ticket_details.models import TicketDetails
from BAAS.config import PNR_KEY, DOJ_KEY, CHART_PREPARED_KEY
from core.formats import DATE_INPUT_FORMAT, ACCEPTED_DATE_FORMAT

import logging
logger = logging.getLogger(__name__)


class TicketDetailsManager(models.Manager):
    def create_pnr_entry(self, user, pnr_details, station_details, train_details):
        try:
            ticket_details = TicketDetails()
            ticket_details.user = user
            ticket_details.pnr_no = int(pnr_details.get(PNR_KEY))
            doj = pnr_details.get(DOJ_KEY)
            doj = datetime.strptime(str(doj), DATE_INPUT_FORMAT).strftime(ACCEPTED_DATE_FORMAT)
            ticket_details.date_of_journey = doj
            ticket_details.boarding_station = station_details[0]
            ticket_details.destination_station = station_details[1]
            ticket_details.train_no = train_details
            ticket_details.is_cancelled = False
            ticket_details.is_chart_prepared = pnr_details.get(CHART_PREPARED_KEY)
            ticket_details.created_datetime = datetime.now(timezone.get_current_timezone())
            ticket_details.last_updated = datetime.now(timezone.get_current_timezone())
            ticket_details.save()
            return ticket_details
        except Exception as e:
            logger.error(str(e))
            raise Exception(e)

    def update_pnr_entry(self, old_ticket_details, new_ticket_details, is_cancelled=False):
        try:
            if not is_cancelled:
                old_ticket_details.is_chart_prepared = new_ticket_details.get(CHART_PREPARED_KEY)
                old_ticket_details.last_updated = datetime.now(timezone.get_current_timezone())
                old_ticket_details.save()
                return old_ticket_details
            else:
                old_ticket_details.is_cancelled = True
                old_ticket_details.last_updated = datetime.now(timezone.get_current_timezone())
                old_ticket_details.save()
                return old_ticket_details
        except Exception as e:
            logger.error(str(e))
            raise Exception(e)