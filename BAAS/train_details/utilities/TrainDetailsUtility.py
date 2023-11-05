from datetime import datetime

from django.utils import timezone
from django.conf import settings
from core.utils import get_data_from_external_api, get_mins_difference_between_two_dates
from train_details.models import TrainDetails
import json
from BAAS.config import STATION_KEY, STATION_CODE_KEY, TRAIN_NUMBER_KEY, TRAIN_NAME_KEY, SCHARRIVAL_KEY, SCHDEPT_KEY, \
    STATION_DISTANCE_KEY, TRAIN_DAY_NUMBER_KEY, SOURCE_VALUE, DEST_VALUE, STATION_NAME_KEY, TRAIN_DETAILS_UPDATE_INTERVAL

import logging
logger = logging.getLogger(__name__)


class TrainDetailsUtility:

    @staticmethod
    def get_train_details_from_external_api(train_number):
        return get_data_from_external_api(settings.RAILWAY_API_BASE_URL + 'v2/route/train/' +
                                          str(train_number) + '/apikey/' + settings.RAILWAY_API_KEY + '/')

    @staticmethod
    def is_train_number_record_exists(train_number):
        try:
            train_details = TrainDetails.objects.get(train_no=train_number)
            return (train_details, True)
        except Exception as e:
            logger.error(e)
            return (None, False)

    @staticmethod
    def get_train_detail_json(train_details):
        try:
            train = dict()
            train[TRAIN_NUMBER_KEY] = train_details.train_no
            train[TRAIN_NAME_KEY] = train_details.train_name
            return train
        except Exception as e:
            logger.error(e)
            return None

    @staticmethod
    def get_route_json(train_details):
        try:
            return json.loads(train_details.routeJSON)
        except Exception as e:
            logger.error(e)
            raise Exception(e)

    @staticmethod
    def get_train_arrival_details_at_stations(train_details, station_codes, update_train_details):
        """

        :param train_details:
        :param station_codes:
        :return:
        """
        try:
            # Check if the records are Latest or not and update the DB with latest data if the entries in the DB are not latest
            # Update train details flag is needed because, there are few cases where we don't need to update the records in database
            if (not TrainDetailsUtility.is_latest_record(train_details=train_details)) and update_train_details:
                # train_details are existing train details (Old records which already exist)
                recent_train_details = TrainDetailsUtility.\
                                        get_train_details_from_external_api(train_number=train_details.train_no)
                from train_details.ModelManagers.TrainDetailsManager import TrainDetailsManager
                TrainDetailsManager().update_train_detail_entry(train_details=recent_train_details,
                                                                existing_train_entry=train_details)
            route_json = TrainDetailsUtility.get_route_json(train_details=train_details)
            train_arrival_details = dict()
            for route in route_json:
                station = route.get(STATION_KEY)
                station_code = station.get(STATION_CODE_KEY)
                if station_code in station_codes:
                    temp_train_arrival_details = dict()
                    temp_train_arrival_details[SCHARRIVAL_KEY] = route.get(SCHARRIVAL_KEY)
                    temp_train_arrival_details[STATION_DISTANCE_KEY] = route.get(STATION_DISTANCE_KEY)
                    temp_train_arrival_details[TRAIN_DAY_NUMBER_KEY] = route.get(TRAIN_DAY_NUMBER_KEY)
                    temp_train_arrival_details[STATION_NAME_KEY] = station.get(STATION_NAME_KEY)
                    train_arrival_details[station_code] = temp_train_arrival_details
            return train_arrival_details
        except Exception as e:
            logger.error(e)
            raise Exception(e)

    @staticmethod
    def normalise_route_json(route_json):
        """
        This method normalises the route JSON which is consumed from external API.
        Normalisation done in this method is, instead of "SOURCE" key at scheduled arrival and "DEST" Key at scheduled departure,
        it copies the same value as of scheduled departure if it is source station in schd arrival key and if it is destination station
        it copies the same value as scheduled arrival into schd dept key
        :param route_json:
        :return:
        """
        try:
            routes = []
            train_start_time = None
            for route in route_json:
                if route.get(SCHARRIVAL_KEY) == SOURCE_VALUE:
                    route[SCHARRIVAL_KEY] = route.get(SCHDEPT_KEY)
                    train_start_time = route[SCHARRIVAL_KEY]
                elif route.get(SCHDEPT_KEY) == DEST_VALUE:
                    route[SCHDEPT_KEY] = route.get(SCHARRIVAL_KEY)
                routes.append(route)
            return routes, train_start_time
        except Exception as e:
            logger.error(e)
            raise Exception(e)

    @staticmethod
    def get_last_updated_date(train_details):
        return train_details.last_updated

    @staticmethod
    def is_latest_record(train_details):
        if get_mins_difference_between_two_dates(from_date=datetime.now(timezone.get_current_timezone()),
                                                 to_date=TrainDetailsUtility.get_last_updated_date(train_details=train_details)) \
                                                    > TRAIN_DETAILS_UPDATE_INTERVAL:
            return False
        else:
            return True