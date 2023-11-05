from BAAS.config import CUISINE_ID_KEY, CUISINE_NAME_KEY
from restaurant.models import Cuisines


class RestaurantCuisineUtility:

    @staticmethod
    def get_restaurant_cuisines(restaurant):
       cuisines = restaurant.cuisines.filter(restaurantprofile=restaurant)
       cuisine_list = []
       for cuisine in cuisines:
           cuisine_list.append((cuisine.cuisine_id, cuisine.cuisine_name))
       return cuisine_list

    @staticmethod
    def get_all_cuisines():
        return Cuisines.objects.all()

    @staticmethod
    def frame_data(cuisine_obj):
        cuisine = dict()
        cuisine[CUISINE_ID_KEY] = cuisine_obj.cuisine_id
        cuisine[CUISINE_NAME_KEY] = cuisine_obj.cuisine_name
        return cuisine