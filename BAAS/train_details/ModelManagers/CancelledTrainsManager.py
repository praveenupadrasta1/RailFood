from django.db import models
from datetime import datetime
from django.utils import timezone

from train_details.models import CancelledTrains
import logging
logger = logging.getLogger(__name__)


class CancelledTrainsManger(models.Manager):
    def create_cancelled_train_entry(self, cancelled_train_date, train_no, train_name):
        try:
            cancelled_train = CancelledTrains()
            cancelled_train.train_no = train_no
            cancelled_train.train_name = train_name
            cancelled_train.cancelled_train_date = cancelled_train_date
            cancelled_train.created_datetime = datetime.now(timezone.get_current_timezone())
            cancelled_train.last_updated = datetime.now(timezone.get_current_timezone())
            cancelled_train.save()
            return cancelled_train
        except Exception as e:
            logger.error(e)
            raise Exception(e)

    def delete_entries_based_on_date(self, date):
        try:
            cancelled_trains = CancelledTrains.objects.filter(cancelled_train_date=date)
            cancelled_trains.delete()
            return True
        except Exception as e:
            logger.error(e)
            raise Exception(e)

    def update_cancelled_train_entry(self, train, train_name):
        try:
            train.train_name=train_name
            train.last_updated=datetime.now(timezone.get_current_timezone())
            train.save()
        except Exception as e:
            logger.error(e)
            raise Exception(e)