from django.db import models
from datetime import datetime
from django.utils import timezone

from train_details.models import RescheduledTrains
import logging
logger = logging.getLogger(__name__)


class RescheduledTrainsManager(models.Manager):
    def create_rescheduled_entry(self, train_no, train_name, rescheduled_date, rescheduled_to_time_in_IST,
                                 rescheduled_to_date_in_IST):
        try:
            rescheduled_train = RescheduledTrains()
            rescheduled_train.train_no = train_no
            rescheduled_train.train_name = train_name
            rescheduled_train.rescheduled_to_time_in_IST = rescheduled_to_time_in_IST
            rescheduled_train.rescheduled_to_date_in_IST = rescheduled_to_date_in_IST
            rescheduled_train.rescheduled_date = rescheduled_date
            rescheduled_train.created_datetime = datetime.now(timezone.get_current_timezone())
            rescheduled_train.last_updated = datetime.now(timezone.get_current_timezone())
            rescheduled_train.save()
            return rescheduled_train
        except Exception as e:
            logger.error(e)
            print str(e)
            raise Exception(e)

    def update_rescheduled_entry(self, train, train_name, rescheduled_to_time_in_IST,
                                 rescheduled_to_date_in_IST):
        try:
            train.train_name = train_name
            train.rescheduled_to_time_in_IST = rescheduled_to_time_in_IST
            train.rescheduled_to_date_in_IST = rescheduled_to_date_in_IST
            train.last_updated = datetime.now(timezone.get_current_timezone())
            train.save()
        except Exception as e:
            logger.error(e)
            print str(e)
            raise Exception(e)

    def delete_entries_based_on_date(self, date):
        try:
            rescheduled_trains = RescheduledTrains.objects.filter(rescheduled_date=date)
            rescheduled_trains.delete()
            return True
        except Exception as e:
            logger.error(e)
            raise Exception(e)