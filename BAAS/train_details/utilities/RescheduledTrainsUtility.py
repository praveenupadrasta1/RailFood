from django.conf import settings
from django.utils import timezone
from datetime import datetime

from core.utils import get_data_from_external_api, get_mins_difference_between_two_dates, convert_date_format, convert_time_format
from BAAS.config import TRAINS_KEY, TRAIN_NUMBER_KEY, TRAIN_NAME_KEY, RESCHEDULED_TRAIN_DETAILS_UPDATE_INTERVAL, RESCHEDULED_TO_TIME_KEY, \
    RESCHEDULED_TO_DATE_KEY
from train_details.ModelManagers.RescheduledTrainsManager import RescheduledTrainsManager
from train_details.models import RescheduledTrains
from core.formats import DATE_INPUT_FORMAT, ACCEPTED_DATE_FORMAT, TIME_INPUT_FORMAT, ACCEPTED_TIME_FORMAT

import logging
logger = logging.getLogger(__name__)


class RescheduledTrainsUtility:

    @staticmethod
    def get_rescheduled_trains_from_external_api(date):
        return get_data_from_external_api(settings.RAILWAY_API_BASE_URL + 'v2/rescheduled/date/' + date + '/apikey/' +
                                          settings.RAILWAY_API_KEY + '/')

    @staticmethod
    def put_data_in_db(data, rescheduled_date):
        try:
            trains_data = data.get(TRAINS_KEY)
            for train in trains_data:
                # If the train details doesn't exists, create a new entry else update the fields
                rescheduled_train = RescheduledTrains.objects.filter(train_no=int(train.get(TRAIN_NUMBER_KEY)),
                                                                    rescheduled_date=rescheduled_date)
                if not rescheduled_train.exists():
                    rescheduled_to_time_in_IST = train.get(RESCHEDULED_TO_TIME_KEY)
                    rescheduled_to_date_in_IST = train.get(RESCHEDULED_TO_DATE_KEY)
                    rescheduled_to_time_in_IST = convert_time_format(rescheduled_to_time_in_IST, TIME_INPUT_FORMAT,
                                                                     ACCEPTED_TIME_FORMAT)
                    rescheduled_to_date_in_IST = convert_date_format(rescheduled_to_date_in_IST, DATE_INPUT_FORMAT,
                                                                     ACCEPTED_DATE_FORMAT)
                    RescheduledTrainsManager().create_rescheduled_entry(train_no=int(train.get(TRAIN_NUMBER_KEY)),
                                                      train_name=train.get(TRAIN_NAME_KEY),
                                                      rescheduled_date=rescheduled_date,
                                                      rescheduled_to_time_in_IST=rescheduled_to_time_in_IST,
                                                      rescheduled_to_date_in_IST=rescheduled_to_date_in_IST)
                else:
                    rescheduled_train = rescheduled_train[0]
                    rescheduled_to_time_in_IST = train.get(RESCHEDULED_TO_TIME_KEY)
                    rescheduled_to_date_in_IST = train.get(RESCHEDULED_TO_DATE_KEY)
                    rescheduled_to_time_in_IST = convert_time_format(rescheduled_to_time_in_IST, TIME_INPUT_FORMAT,
                                                                     ACCEPTED_TIME_FORMAT)
                    rescheduled_to_date_in_IST = convert_date_format(rescheduled_to_date_in_IST, DATE_INPUT_FORMAT,
                                                                     ACCEPTED_DATE_FORMAT)
                    RescheduledTrainsManager().update_rescheduled_entry(train=rescheduled_train,
                                                        train_name=train.get(TRAIN_NAME_KEY),
                                                      rescheduled_to_time_in_IST=rescheduled_to_time_in_IST,
                                                      rescheduled_to_date_in_IST=rescheduled_to_date_in_IST)
            return True
        except Exception as e:
            logger.error(e)
            print str(e)
            return False

    @staticmethod
    def is_rescheduled_trains_exists(date):
        try:
            result_set = RescheduledTrains.objects.filter(rescheduled_date=date)
            return result_set
        except Exception as e:
            logger.error(e)
            return None

    @staticmethod
    def get_last_updated_date(rescheduled_train):
        return rescheduled_train.last_updated

    @staticmethod
    def is_latest_records(rescheduled_train):
        if get_mins_difference_between_two_dates(from_date=datetime.now(timezone.get_current_timezone()),
                                                 to_date=RescheduledTrainsUtility.get_last_updated_date(rescheduled_train)) \
                                                > RESCHEDULED_TRAIN_DETAILS_UPDATE_INTERVAL:
            return False
        else:
            return True

    @staticmethod
    def is_train_rescheduled(train_no, date):
        try:
            rescheduled_train = RescheduledTrains.objects.get(rescheduled_date=date,
                                        train_no=train_no)
            return rescheduled_train
        except Exception as e:
            logger.error(e)
            return None