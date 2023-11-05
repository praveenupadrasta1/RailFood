from restaurant.models import RestaurantProfile
from ticket_details.utilities.StationDetailsUtility import StationDetailsUtility
from restaurant.utilities.RestaurantReviewRatingUtility import RestaurantReviewRatingUtility
from restaurant.utilities.RestaurantCuisineUtility import RestaurantCuisineUtility
from BAAS.config import NAME_KEY, CATEGORY_KEY, MOBILE_NUM_KEY, ADDRESS_KEY, IMAGE_URL_KEY, ORDER_OPEN_TIMING_FROM_KEY, \
    ORDER_OPEN_TIMING_TO_KEY, STATION_CODE_KEY, STATION_NAME_KEY, STATION_KEY, RESTAURANT_ID_KEY, RESTAURANT_RATING_KEY, \
    RESTAURANT_NUMBER_REVIEWS_KEY, RESTAURANT_CUISINES_KEY, RESTAURANT_HAS_OFFER_KEY

import logging
logger = logging.getLogger(__name__)


class RestaurantProfileUtility:

    @staticmethod
    def put_data_in_db(request, is_update):
        if not is_update:
            return RestaurantProfile.profile.create(user=request.user, data=request.data)
        else:
            restaurant_profile = RestaurantProfileUtility.get_restaurant_profile(user=request.user)
            if restaurant_profile:
                return RestaurantProfile.profile.update(user=request.user, restaurant_profile=restaurant_profile, data=request.data)
            else:
                return RestaurantProfile.profile.create(user=request.user, data=request.data)

    @staticmethod
    def frame_data(restaurant_profile):
        restaurant = dict()
        restaurant[NAME_KEY] = restaurant_profile.name
        restaurant[CATEGORY_KEY] = restaurant_profile.category
        restaurant[MOBILE_NUM_KEY] = restaurant_profile.mobile_number
        restaurant[ADDRESS_KEY] = restaurant_profile.address
        restaurant[IMAGE_URL_KEY] = restaurant_profile.image_url
        restaurant[ORDER_OPEN_TIMING_FROM_KEY] = restaurant_profile.order_open_timing_from
        restaurant[ORDER_OPEN_TIMING_TO_KEY] = restaurant_profile.order_open_timing_to
        restaurant[RESTAURANT_ID_KEY] = restaurant_profile.restaurant.id
        restaurant[RESTAURANT_RATING_KEY] = RestaurantReviewRatingUtility.get_restaurant_rating(restaurant_profile)
        restaurant[RESTAURANT_NUMBER_REVIEWS_KEY] = RestaurantReviewRatingUtility.get_restaurant_count_reviews(restaurant_profile)
        restaurant[RESTAURANT_CUISINES_KEY] = RestaurantCuisineUtility.get_restaurant_cuisines(restaurant_profile)
        restaurant[RESTAURANT_HAS_OFFER_KEY] = False
        station = dict()
        station[STATION_CODE_KEY] = restaurant_profile.restaurant_station.station_name
        station[STATION_NAME_KEY] = restaurant_profile.restaurant_station.station_code
        restaurant[STATION_KEY] = station
        return restaurant

    @staticmethod
    def get_restaurant_profile(user):
        try:
            return RestaurantProfile.objects.get(restaurant=user)
        except Exception as e:
            logger.error(str(e))
            return None

    @staticmethod
    def get_restaurants_assigned_to_station(station_code):
        try:
            station = StationDetailsUtility.is_station_details_exist(station_code=station_code)
            if station:
                restaurants = RestaurantProfile.objects.filter(restaurant_station=station_code)
                if restaurants.exists():
                    return restaurants
                else:
                    return None
            else:
                return None
        except Exception as e:
            logger.error(str(e))
            return None