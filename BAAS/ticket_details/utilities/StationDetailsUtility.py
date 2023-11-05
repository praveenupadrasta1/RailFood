from django.conf import settings
import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from BAAS.config import STATION_LNG_KEY, STATION_LAT_KEY, RESULTS_KEY, ADDRESS_COMPONENTS_KEY, TYPES_KEY, \
    ADMIN_AREA_LEVEL_1_KEY, SHORT_NAME_KEY, STATE_SHORT_NAME_KEY, STATION_CODE_KEY
from ticket_details.models import StationDetails
from core.utils import get_data_from_external_api


class StationDetailsUtility:

    @staticmethod
    def get_station_details_from_pnr_details(pnr_details, type):
        try:
            station_details = pnr_details.get(type)
            lat = station_details.get(STATION_LAT_KEY)
            lng = station_details.get(STATION_LNG_KEY)
            temp_station = StationDetailsUtility.is_station_details_exist(station_details.get(STATION_CODE_KEY))
            if not temp_station:
                state_short_name = ''
                location_details = get_data_from_external_api(settings.GOOGLE_MAPS_BASE_URL +
                                                              'geocode/json?latlng=' + str(lat) + ',' + str(lng) + '&key=' +
                                                              settings.GOOGLE_MAPS_GEOCODING_API_KEY)
                results = location_details.get(RESULTS_KEY)[0]
                address_components = results.get(ADDRESS_COMPONENTS_KEY)
                for add_comp in address_components:
                    types = add_comp.get(TYPES_KEY)
                    if ADMIN_AREA_LEVEL_1_KEY in types:
                        state_short_name = add_comp.get(SHORT_NAME_KEY)
                        break
                station_details[STATE_SHORT_NAME_KEY] = state_short_name
            else:
                station_details[STATE_SHORT_NAME_KEY] = temp_station.state
            return station_details
        except Exception as e:
            logger.error(str(e))
            raise Exception(e)

    @staticmethod
    def is_station_details_exist(station_code):
        try:
            return StationDetails.objects.get(station_code=station_code)
        except Exception as e:
            logger.error(str(e))
            return None

    @staticmethod
    def get_all_stations():
        try:
            return StationDetails.objects.all().values('station_name','station_code','state')
        except Exception as e:
            logger.error(str(e))
            return None
