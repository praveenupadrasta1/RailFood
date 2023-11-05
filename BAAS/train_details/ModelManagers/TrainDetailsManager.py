from train_details.models import TrainDetails
from BAAS.config import TRAIN_KEY, TRAIN_NAME_KEY, TRAIN_NUMBER_KEY, TRAIN_ROUTE_KEY
from datetime import datetime
from django.utils import timezone
from django.db import models
from core.utils import convert_str_time_to_time_obj
from train_details.utilities.TrainDetailsUtility import TrainDetailsUtility
import json
import logging
logger = logging.getLogger(__name__)


class TrainDetailsManager(models.Manager):
    def create_train_detail_entry(self, train_details):
        try:
            train = TrainDetails()
            temp_train_details = train_details.get(TRAIN_KEY)
            train.train_no = temp_train_details.get(TRAIN_NUMBER_KEY)
            train.train_name = temp_train_details.get(TRAIN_NAME_KEY)
            route_json = train_details.get(TRAIN_ROUTE_KEY)
            route_json, train_start_time = TrainDetailsUtility.normalise_route_json(route_json=route_json)
            train.train_start_time = convert_str_time_to_time_obj(train_start_time + ':00')
            train.routeJSON = json.dumps(route_json)
            train.created_datetime = datetime.now(timezone.get_current_timezone())
            train.last_updated = datetime.now(timezone.get_current_timezone())
            train.save()
            return train
        except Exception as e:
            logger.error(str(e))
            raise Exception(e)

    def update_train_detail_entry(self, train_details, existing_train_entry):
        try:
            temp_train_details = train_details.get(TRAIN_KEY)
            existing_train_entry.train_name = temp_train_details.get(TRAIN_NAME_KEY)
            route_json = train_details.get(TRAIN_ROUTE_KEY)
            route_json, train_start_time = TrainDetailsUtility.normalise_route_json(route_json=route_json)
            existing_train_entry.train_start_time = convert_str_time_to_time_obj(train_start_time + ':00')
            existing_train_entry.routeJSON = json.dumps(route_json)
            existing_train_entry.last_updated = datetime.now(timezone.get_current_timezone())
            existing_train_entry.save()
            return existing_train_entry
        except Exception as e:
            logger.error(str(e))
            raise Exception(e)