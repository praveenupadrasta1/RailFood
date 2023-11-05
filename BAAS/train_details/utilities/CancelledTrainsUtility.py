from django.conf import settings
from datetime import datetime
from django.utils import timezone

from train_details.models import CancelledTrains
from BAAS.config import TRAINS_KEY, TRAIN_NUMBER_KEY, TRAIN_NAME_KEY
from core.utils import get_data_from_external_api, get_mins_difference_between_two_dates, convert_date_format
from train_details.ModelManagers.CancelledTrainsManager import CancelledTrainsManger
from BAAS.config import CANCELLED_TRAIN_DETAILS_UPDATE_INTERVAL
from core.formats import DATE_INPUT_FORMAT, ACCEPTED_DATE_FORMAT

import logging
logger = logging.getLogger(__name__)


class CancelledTrainsUtility:

    @staticmethod
    def get_cancelled_trains_from_external_api(date):
        return get_data_from_external_api(settings.RAILWAY_API_BASE_URL + 'v2/cancelled/date/' + date + '/apikey/' +
                                          settings.RAILWAY_API_KEY + '/')

    @staticmethod
    def put_data_in_db(data, cancelled_train_date):
        try:
            trains_data = data.get(TRAINS_KEY)
            for train in trains_data:
                cancelled_train = CancelledTrains.objects.filter(train_no=int(train.get(TRAIN_NUMBER_KEY)),
                                                                 cancelled_train_date=cancelled_train_date)
                if not cancelled_train.exists():
                    CancelledTrainsManger().create_cancelled_train_entry(cancelled_train_date=cancelled_train_date,
                                                           train_no=train.get(TRAIN_NUMBER_KEY),
                                                           train_name=train.get(TRAIN_NAME_KEY))
                else:
                    cancelled_train = cancelled_train[0]
                    CancelledTrainsManger().update_cancelled_train_entry(train=cancelled_train,
                                                                         train_name=train.get(TRAIN_NAME_KEY))
            return True
        except Exception as e:
            logger.error(e)
            return False

    @staticmethod
    def get_last_updated_date(cancelled_train):
        return cancelled_train.last_updated

    @staticmethod
    def is_cancelled_trains_exists(date):
        try:
            result_set = CancelledTrains.objects.filter(cancelled_train_date=date)
            return result_set
        except Exception as e:
            logger.error(e)
            return None

    @staticmethod
    def is_latest_record(cancelled_train):
        if get_mins_difference_between_two_dates(from_date=datetime.now(timezone.get_current_timezone()),
                                                 to_date=CancelledTrainsUtility.get_last_updated_date(cancelled_train)) \
                                                                            > CANCELLED_TRAIN_DETAILS_UPDATE_INTERVAL:
            return False
        else:
            return True

    @staticmethod
    def is_train_cancelled(train_no, date):
        try:
            cancelled_train = CancelledTrains.objects.get(cancelled_train_date=date,
                                    train_no=train_no)
            # Check if the records are Latest or not and update the DB with latest data if the entries in the DB are not latest
            if not CancelledTrainsUtility.is_latest_record(cancelled_train=cancelled_train):
                converted_date = convert_date_format(date=date, convert_from_format=ACCEPTED_DATE_FORMAT,
                                                     convert_to_format=DATE_INPUT_FORMAT)
                data = CancelledTrainsUtility.get_cancelled_trains_from_external_api(date=converted_date)
                is_deleted = CancelledTrainsManger().delete_entries_based_on_date(date=date)
                if is_deleted:
                    CancelledTrainsUtility.put_data_in_db(data=data, cancelled_train_date=date)
            if CancelledTrains.objects.get(cancelled_train_date=date,
                                                          train_no=train_no):
                return True
            else:
                return False
        except Exception as e:
            logger.error(e)
            return False