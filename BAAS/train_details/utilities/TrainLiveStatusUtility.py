import json
from datetime import datetime
from django.conf import settings
from django.utils import timezone

from train_details.models import TrainLiveStatus
from core.utils import get_data_from_external_api, convert_date_format, get_mins_difference_between_two_dates
from core.formats import ACCEPTED_DATE_FORMAT, DATE_INPUT_FORMAT
from BAAS.config import TRAIN_LIVE_STATUS_UPDATE_INTERVAL, TRAIN_LIVE_STATUS
from train_details.ModelManagers.TrainLiveStatusManager import TrainLiveStatusManager

import logging
logger = logging.getLogger(__name__)


class TrainLiveStatusUtility:

    @staticmethod
    def get_live_train_status_from_external_api(train_no, train_start_date):
        train_start_date = convert_date_format(date=train_start_date, convert_from_format=ACCEPTED_DATE_FORMAT,
                                                     convert_to_format=DATE_INPUT_FORMAT)
        return get_data_from_external_api(settings.RAILWAY_API_BASE_URL + 'v2/live/train/' + str(train_no) + '/date/' +
                                          train_start_date + '/apikey/' + settings.RAILWAY_API_KEY + '/')

    @staticmethod
    def is_train_live_status_exists(train_no, train_start_date):
        try:
            return TrainLiveStatus.objects.get(train_no=train_no, train_start_date=train_start_date)
        except Exception as e:
            logger.error(str(e))
            return None

    @staticmethod
    def is_latest_record(train_no, train_start_date):
        try:
            live_status = TrainLiveStatus.objects.get(train_no=train_no, train_start_date=train_start_date)
            if get_mins_difference_between_two_dates(from_date=datetime.now(timezone.get_current_timezone()),
                                                  to_date=live_status.last_updated) > TRAIN_LIVE_STATUS_UPDATE_INTERVAL:
                return False
            else:
                return True
        except Exception as e:
            logger.error(str(e))
            return False

    @staticmethod
    def put_data_in_db(train_no, train_start_date, live_status):
        TrainLiveStatusManager().create_live_train_status_entry(train_no=train_no,
                                                                train_start_date=train_start_date,
                                                                live_status=live_status)

    @staticmethod
    def get_train_live_status_json(train_no, train_start_date):
        try:
            return TrainLiveStatusUtility.frame_data(TrainLiveStatus.objects.get(train_no=train_no,
                                                                                 train_start_date=train_start_date))
        except Exception as e:
            logger.error(str(e))
            return None

    @staticmethod
    def get_live_status_json(train_live_status):
        try:
            return json.loads(train_live_status.live_status)
        except Exception as e:
            logger.error(e)
            raise Exception(e)

    @staticmethod
    def frame_data(train_live_status):
        train_live_status_dict = dict()
        train_live_status_dict[TRAIN_LIVE_STATUS] = TrainLiveStatusUtility.get_live_status_json(train_live_status=train_live_status)
        return train_live_status_dict
