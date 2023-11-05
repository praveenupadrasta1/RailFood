# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from rest_framework.response import Response
from rest_framework import status

from BAAS.config import HTTP_API_VERSION_KEY, BETA_VERSION_KEY, INVALID_API_VERSION, DETAILS_KEY, STATION_CODE_KEY, \
    PROFILE_ALREADY_EXISTS, BANK_DETAILS_ALREADY_EXIST, BANK_DETAILS_DOESNT_EXIST, PROFILE_DOESNT_EXISTS
from core.permissions import CAN_CREATE_RESTAURANT_PROFILE, CAN_ADD_BANK_DETAILS, CAN_UPDATE_BANK_DETAILS, \
    CAN_UPDATE_RESTAURANT_PROFILE, CAN_GET_RESTAURANT_PROFILE, CAN_GET_BANK_DETAILS, CAN_GET_CUISINES, CAN_GET_MEMBERSHIP
from restaurant.serializers import RestaurantProfileSerializer, RestaurantBankDetailsSerializer, GetRestaurantsSerializer
from restaurant.utilities.RestaurantProfileUtility import RestaurantProfileUtility
from restaurant.utilities.RestaurantBankDetailsUtility import RestaurantBankDetailsUtility
from restaurant.utilities.RestaurantCuisineUtility import RestaurantCuisineUtility
from restaurant.utilities.MembershipUtility import MembershipUtility

# Create your views here.


class RestaurantCreateUpdateProfileView(generics.GenericAPIView):
    """
    This view is responsible for creating restaurant profile
    """

    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.META.get(HTTP_API_VERSION_KEY).lower() == BETA_VERSION_KEY:
            return RestaurantProfileSerializer
        raise Exception(INVALID_API_VERSION)

    @method_decorator(permission_required(CAN_CREATE_RESTAURANT_PROFILE[3] + '.' + CAN_CREATE_RESTAURANT_PROFILE[0]))
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not RestaurantProfileUtility.get_restaurant_profile(user=request.user):
            restaurant_profile = RestaurantProfileUtility.put_data_in_db(request, is_update=False)
            restaurant_data = RestaurantProfileUtility.frame_data(restaurant_profile=restaurant_profile)
            return Response({DETAILS_KEY: restaurant_data}, status=status.HTTP_200_OK)
        else:
            return Response({DETAILS_KEY: PROFILE_ALREADY_EXISTS}, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(permission_required(CAN_UPDATE_RESTAURANT_PROFILE[3] + '.' + CAN_UPDATE_RESTAURANT_PROFILE[0]))
    def put(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if RestaurantProfileUtility.get_restaurant_profile(user=request.user):
            restaurant_profile = RestaurantProfileUtility.put_data_in_db(request, is_update=True)
            restaurant_data = RestaurantProfileUtility.frame_data(restaurant_profile=restaurant_profile)
            return Response({DETAILS_KEY: restaurant_data}, status=status.HTTP_200_OK)
        else:
            return Response({DETAILS_KEY: PROFILE_DOESNT_EXISTS}, status=status.HTTP_400_BAD_REQUEST)


class GetRestaurantsView(generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.META.get(HTTP_API_VERSION_KEY).lower() == BETA_VERSION_KEY:
            return GetRestaurantsSerializer
        raise Exception(INVALID_API_VERSION)

    @method_decorator(permission_required(CAN_GET_RESTAURANT_PROFILE[3] + '.' + CAN_GET_RESTAURANT_PROFILE[0]))
    def post(self, request):
        restaurants = RestaurantProfileUtility.get_restaurants_assigned_to_station(station_code=request.data.get(STATION_CODE_KEY))
        if restaurants:
            restaurants_data = []
            for restaurant in restaurants:
                restaurants_data.append(RestaurantProfileUtility.frame_data(restaurant))
            return Response({DETAILS_KEY:restaurants_data}, status=status.HTTP_200_OK)
        else:
            return Response({DETAILS_KEY: None}, status=status.HTTP_400_BAD_REQUEST)


class RestaurantBankDetailsCreateUpdateView(generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.META.get(HTTP_API_VERSION_KEY).lower() == BETA_VERSION_KEY:
            return RestaurantBankDetailsSerializer
        raise Exception(INVALID_API_VERSION)

    @method_decorator(permission_required(CAN_ADD_BANK_DETAILS[3] + '.' + CAN_ADD_BANK_DETAILS[0]))
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not RestaurantBankDetailsUtility.get_bank_details(user=request.user):
            restaurant_bank_details = RestaurantBankDetailsUtility.put_data_in_db(request, is_update=False)
            bank_data = RestaurantBankDetailsUtility.frame_data(bank_details=restaurant_bank_details)
            return Response({DETAILS_KEY: bank_data}, status=status.HTTP_200_OK)
        else:
            return Response({DETAILS_KEY: BANK_DETAILS_ALREADY_EXIST}, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(permission_required(CAN_UPDATE_BANK_DETAILS[3] + '.' + CAN_UPDATE_BANK_DETAILS[0]))
    def put(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        restaurant_bank_details = RestaurantBankDetailsUtility.put_data_in_db(request, is_update=True)

        bank_data = RestaurantBankDetailsUtility.frame_data(bank_details=restaurant_bank_details)
        return Response({DETAILS_KEY: bank_data}, status=status.HTTP_200_OK)


class GetRestaurantBankDetailsView(generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)

    @method_decorator(permission_required(CAN_GET_BANK_DETAILS[3] + '.' + CAN_GET_BANK_DETAILS[0]))
    def get(self, request):
        if self.request.META.get(HTTP_API_VERSION_KEY).lower() == BETA_VERSION_KEY:
            restaurant_bank_details = RestaurantBankDetailsUtility.get_bank_details(user=request.user)
            if restaurant_bank_details:
                bank_data = RestaurantBankDetailsUtility.frame_data(bank_details=restaurant_bank_details)
                return Response({DETAILS_KEY: bank_data}, status=status.HTTP_200_OK)
            else:
                return Response({DETAILS_KEY: BANK_DETAILS_DOESNT_EXIST}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({DETAILS_KEY: INVALID_API_VERSION}, status=status.HTTP_400_BAD_REQUEST)


class GetCuisinesView(generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)

    @method_decorator(permission_required(CAN_GET_CUISINES[3] + '.' + CAN_GET_CUISINES[0]))
    def get(self, request):
        if self.request.META.get(HTTP_API_VERSION_KEY).lower() == BETA_VERSION_KEY:
            cuisines = RestaurantCuisineUtility.get_all_cuisines()
            cuisines_list = []
            for cuisine in cuisines:
                cuisines_list.append(RestaurantCuisineUtility.frame_data(cuisine_obj=cuisine))
            return Response({DETAILS_KEY: cuisines_list}, status=status.HTTP_200_OK)
        else:
            return Response({DETAILS_KEY: INVALID_API_VERSION}, status=status.HTTP_400_BAD_REQUEST)


class GetMembershipsView(generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)

    @method_decorator(permission_required(CAN_GET_MEMBERSHIP[3] + '.' + CAN_GET_MEMBERSHIP[0]))
    def get(self, request):
        if self.request.META.get(HTTP_API_VERSION_KEY).lower() == BETA_VERSION_KEY:
            memberships = MembershipUtility.get_all_memberships()
            membership_list = []
            for membership in memberships:
                membership_list.append(MembershipUtility.frame_data(membership_obj=membership))
            return Response({DETAILS_KEY: membership_list}, status=status.HTTP_200_OK)
        else:
            return Response({DETAILS_KEY: INVALID_API_VERSION}, status=status.HTTP_400_BAD_REQUEST)
