from datetime import datetime

from django.utils import timezone
from django.db import models
import logging
logger = logging.getLogger(__name__)

from BAAS.config import NAME_KEY, CATEGORY_KEY, MOBILE_NUM_KEY, ADDRESS_KEY, IMAGE_URL_KEY, ORDER_OPEN_TIMING_FROM_KEY, \
    ORDER_OPEN_TIMING_TO_KEY, STATION_KEY, RESTAURANT_CUISINES_KEY
from ticket_details.utilities.StationDetailsUtility import StationDetailsUtility


class RestaurantProfileManager(models.Manager):

    def create(self, user, data):
        try:
            station = StationDetailsUtility.is_station_details_exist(station_code=data.get(STATION_KEY))
            restaurant_profile = self.model(restaurant=user,
                                            name=data.get(NAME_KEY),
                                            category=data.get(CATEGORY_KEY),
                                            mobile_number=data.get(MOBILE_NUM_KEY),
                                            address=data.get(ADDRESS_KEY),
                                            image_url=data.get(IMAGE_URL_KEY),
                                            order_open_timing_from=data.get(ORDER_OPEN_TIMING_FROM_KEY),
                                            order_open_timing_to=data.get(ORDER_OPEN_TIMING_TO_KEY),
                                            restaurant_station=station,
                                            created_datetime=datetime.now(timezone.get_current_timezone()),
                                            last_updated=datetime.now(timezone.get_current_timezone()))
            restaurant_profile.save()
            from restaurant.models import Cuisines
            cuisines_list = data.get(RESTAURANT_CUISINES_KEY)
            for cuisine in cuisines_list:
                cuisine_obj = Cuisines.objects.get(cuisine_id=cuisine)
                restaurant_profile.cuisines.add(cuisine_obj)
                restaurant_profile.save()
            return restaurant_profile
        except Exception as e:
            logger.error(str(e))
            raise Exception(e)

    def update(self, user, restaurant_profile, data):
        try:
            restaurant_profile.name = data.get(NAME_KEY)
            restaurant_profile.category = data.get(CATEGORY_KEY)
            restaurant_profile.mobile_number = data.get(MOBILE_NUM_KEY)
            restaurant_profile.address = data.get(ADDRESS_KEY)
            restaurant_profile.order_open_timing_from = data.get(ORDER_OPEN_TIMING_FROM_KEY)
            restaurant_profile.order_open_timing_to = data.get(ORDER_OPEN_TIMING_TO_KEY)
            restaurant_profile.last_updated = datetime.now(timezone.get_current_timezone())
            restaurant_profile.save()
            logger.info(str(user) + "has changed the profile of this restaurant at " + str(restaurant_profile.last_updated))
            return restaurant_profile
        except Exception as e:
            logger.error(str(e))
            raise Exception(e)