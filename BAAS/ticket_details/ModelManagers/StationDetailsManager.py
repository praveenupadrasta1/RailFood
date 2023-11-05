from django.db import models
from ticket_details.models import StationDetails
from datetime import datetime
from django.utils import timezone

from BAAS.config import STATION_NAME_KEY, STATION_CODE_KEY, STATION_LAT_KEY, STATION_LNG_KEY, STATE_SHORT_NAME_KEY

import logging
logger = logging.getLogger(__name__)


class StationDetailsManager(models.Manager):
    def create_station_details(self, station_details):
        try:
            station = StationDetails()
            station.station_code = station_details.get(STATION_CODE_KEY)
            station.station_name = station_details.get(STATION_NAME_KEY)
            station.latitude = station_details.get(STATION_LAT_KEY)
            station.longitude = station_details.get(STATION_LNG_KEY)
            station.state = station_details.get(STATE_SHORT_NAME_KEY)
            station.created_datetime = datetime.now(timezone.get_current_timezone())
            station.last_updated = datetime.now(timezone.get_current_timezone())
            station.save()
            return station
        except Exception as e:
            logger.error(e)
            raise Exception(e)