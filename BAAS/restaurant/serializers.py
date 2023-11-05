from rest_framework import serializers

from restaurant.models import RestaurantBankDetails, RestaurantMembershipDetails, RestaurantReviewRating
from BAAS.config import VEGETARIAN, NON_VEGETARIAN, MULTI_CUISINE, INVALID_MOBILE_NUMBER, INVALID_STATION, INVALID_CUISINE
from ticket_details.utilities.StationDetailsUtility import StationDetailsUtility
from restaurant.models import Cuisines


class RestaurantProfileSerializer(serializers.Serializer):

    CATEGORY_CHOICES = (('V', VEGETARIAN),
                        ('N', NON_VEGETARIAN),
                        ('M', MULTI_CUISINE))

    name = serializers.CharField(max_length=50, allow_blank=False)
    category = serializers.ChoiceField(choices=CATEGORY_CHOICES, allow_blank=False)
    mobile_number = serializers.CharField(max_length=13, allow_blank=False)
    address = serializers.CharField(max_length=250, allow_blank=False)
    image_url = serializers.CharField(max_length=150, required=False, allow_null=True, allow_blank=True)
    order_open_timing_from = serializers.CharField(max_length=5, allow_blank=False)
    order_open_timing_to = serializers.CharField(max_length=5, allow_blank=False)
    station = serializers.CharField(max_length=30, allow_blank=False)
    cuisines = serializers.ListField(allow_null=False, allow_empty=False, required=True)

    def validate_mobile_number(self, mobile_num):
        if str(mobile_num).isdigit():
            return mobile_num
        else:
            raise serializers.ValidationError(INVALID_MOBILE_NUMBER)

    def validate_restaurant_station(self, station_code):
        if StationDetailsUtility.is_station_details_exist(station_code=station_code):
            return station_code
        else:
            raise serializers.ValidationError(INVALID_STATION)

    def validate_cuisines(self, cuisines_data):
        try:
            for cuisine in cuisines_data:
                Cuisines.objects.get(cuisine_id=cuisine)
            return cuisines_data
        except Exception as e:
            raise serializers.ValidationError(INVALID_CUISINE)


class GetRestaurantsSerializer(serializers.Serializer):

    station_code = serializers.CharField(max_length=10, allow_blank=False, required=True)

    def validate_station_code(self, data):
        if StationDetailsUtility.is_station_details_exist(station_code=data):
            return data
        else:
            raise serializers.ValidationError(INVALID_STATION)


class RestaurantBankDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = RestaurantBankDetails
        fields = ['account_name', 'account_number', 'IFSC_code', 'bank_name']


class RestaurantMembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = RestaurantMembershipDetails
        fields = ['membership_type']


class RestaurantReviewRatingSerializer(serializers.ModelSerializer):

    rating = serializers.IntegerField()
    review = serializers.CharField(max_length=250, allow_blank=True)

    class Meta:
        model = RestaurantReviewRating
        fields = ['review','rating']