import json
from datetime import datetime

from django.utils import timezone
from django.db import models
from train_details.models import TrainLiveStatus

import logging
logger = logging.getLogger(__name__)


class TrainLiveStatusManager(models.Manager):

    def create_live_train_status_entry(self, train_no, train_start_date, live_status):
        try:
            train_live_status = TrainLiveStatus()
            train_live_status.train_no = train_no
            train_live_status.train_start_date = train_start_date
            train_live_status.live_status = json.dumps(live_status)
            train_live_status.created_datetime = datetime.now(timezone.get_current_timezone())
            train_live_status.last_updated = datetime.now(timezone.get_current_timezone())
            train_live_status.save()
        except Exception as e:
            logger.error(str(e))
            raise Exception(e)

    def update_live_train_status_entry(self, train_no, train_start_date, live_status):
        try:
            train_live_status = TrainLiveStatus.objects.get(train_no=train_no,
                                                            train_start_date=train_start_date)
            train_live_status.live_status = json.dumps(live_status)
            train_live_status.last_updated = datetime.now(timezone.get_current_timezone())
            train_live_status.save()
        except Exception as e:
            logger.error(str(e))
            raise Exception(e)