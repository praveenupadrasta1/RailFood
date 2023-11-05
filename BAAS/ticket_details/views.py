# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

from serializers import AddJourneySerializer, GetJourneySerializer
from utilities.TicketDetailsUtility import TicketDetailsUtility
from core.railway_api_utilities import get_train_number_from_pnr_details
from core.utils import get_mins_difference_between_two_dates
from core.permissions import ADD_TICKETDETAILS, DELETE_TICKETDETAILS, CAN_GET_MY_JOURNEYS
from train_details.utilities.TrainDetailsUtility import TrainDetailsUtility
from utilities.StationDetailsUtility import StationDetailsUtility
from utilities.SeatDetailsUtility import SeatDetailsUtility
from ModelManagers.SeatDetailsManager import SeatDetailsManager
from ModelManagers.StationDetailsManager import StationDetailsManager
from ModelManagers.TicketDetailsManager import TicketDetailsManager
from user_authentication.utilities.UserUtilities import UserUtilities
from train_details.models import TrainDetails
from ticket_details.models import TicketDetails, SeatDetails
from train_details.ModelManagers.TrainDetailsManager import TrainDetailsManager
from BAAS.config import TRAIN_DETAILS_UPDATE_INTERVAL, RESPONSE_CODE_KEY, PNR_NO_KEY, FROM_STATION_KEY, TO_STATION_KEY,\
                        INVALID_PNR_NUMBER, HTTP_API_VERSION_KEY, BETA_VERSION_KEY, INVALID_API_VERSION, STATUS_KEY, DETAILS_KEY, \
                        PNR_DETAILS_ALREADY_EXISTS, TRAIN_NUMBER_KEY, TRAIN_ARRIVAL_DETAILS_KEY, DOJ_KEY, BOARDING_POINT_KEY,\
                        STATION_CODE_KEY, DESTINATION_STATION_KEY, PNR_KEY, PNR_DETAILS_KEY, SEAT_DETAILS_KEY, TRAIN_DETAILS_KEY, \
                        NO_JOURNEYS_EXIST, SERVER_DATETIME_UTC_KEY, PNR_DETAILS_UPDATE_INTERVAL_KEY, PNR_DETAILS_UPDATE_INTERVAL

# Create your views here.


class AddJourneyView(generics.GenericAPIView):
    """
    This View is responsible for adding a journey of a user
    """
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.META.get(HTTP_API_VERSION_KEY).lower() == BETA_VERSION_KEY:
            return AddJourneySerializer
        raise Exception(INVALID_API_VERSION)

    @method_decorator(permission_required((ADD_TICKETDETAILS[3] + '.' + ADD_TICKETDETAILS[0])))
    def post(self, request, *args, **kwargs):
        """
        :param request:
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not TicketDetailsUtility.is_pnr_number_exists(pnr_no=request.data.get(PNR_NO_KEY)):
            pnr_details = TicketDetailsUtility.get_pnr_details_from_external_api(pnr_no=request.data.get(PNR_NO_KEY))
            if pnr_details.get(RESPONSE_CODE_KEY) == 200:
                train_details = None
                train_entry = None

                # Get Seat details
                seat_details = SeatDetailsUtility.get_seat_details_from_pnr_details(pnr_details=pnr_details)

                if seat_details: # If seat details in not None. Also means it doesn't have any cancelled seats
                    # Get train details
                    train_number = get_train_number_from_pnr_details(pnr_details=pnr_details)
                    result = TrainDetailsUtility.is_train_number_record_exists(train_number=train_number)

                    # result[1] is boolean field, which states whether train record exists or not
                    if result[1]:
                        if not TrainDetailsUtility.is_latest_record(result[0]):
                            train_details = TrainDetailsUtility.get_train_details_from_external_api(train_number=train_number)

                            # Update train details
                            train_entry = TrainDetailsManager().update_train_detail_entry(train_details=train_details,
                                                                                          existing_train_entry=result[0])
                        else:
                            # result[0] is an object, which gives train details upon existence or returns None
                            train_entry = result[0]
                    else:
                        train_details = TrainDetailsUtility.get_train_details_from_external_api(train_number=train_number)
                        # Save train details
                        train_entry = TrainDetailsManager().create_train_detail_entry(train_details=train_details)

                    # Get Station Details
                    boarding_station_details = StationDetailsUtility.\
                        get_station_details_from_pnr_details(pnr_details=pnr_details, type=FROM_STATION_KEY)
                    destination_station_details = StationDetailsUtility.\
                        get_station_details_from_pnr_details(pnr_details=pnr_details, type=TO_STATION_KEY)

                    # Save Station Details
                    boarding_station = StationDetailsManager().create_station_details(station_details=boarding_station_details)
                    destination_station = StationDetailsManager().\
                        create_station_details(station_details=destination_station_details)

                    # Save PNR Details
                    pnr_entry = TicketDetailsUtility.put_data_in_db(user=request.user, pnr_details=pnr_details,
                                                                station_details=[boarding_station, destination_station],
                                                                train_details=train_entry)

                    # Save Seat Details
                    seat_entries = []
                    for seat_detail in seat_details:
                        seat = SeatDetailsManager().create_seat_detail_entry(seat_detail, pnr_entry)
                        seat_entries.append(seat)

                    # pnr_json = TicketDetailsUtility.get_pnr_details_json_based_on_pnr_object(pnr_entry=pnr_entry)
                    pnr_json = TicketDetailsUtility.get_pnr_details(ticket_details=TicketDetails.
                                                                                    objects.
                                                                                    get(pnr_no=pnr_entry.pnr_no))
                    seat_json = SeatDetailsUtility.get_seat_details(seat_details=SeatDetails.
                                                                                      objects.
                                                                                      filter(pnr=pnr_entry.pnr_no))
                    train_json = TrainDetailsUtility.get_train_detail_json(train_details=TrainDetails.
                                                                                         objects.
                                                                                         get(train_no=pnr_entry.train_no.train_no))
                    train_arrival_details = TrainDetailsUtility.\
                                            get_train_arrival_details_at_stations(train_details=TrainDetails.
                                                                                                objects.
                                                                                                get(train_no=train_json[TRAIN_NUMBER_KEY]),
                                                                                  station_codes=[pnr_json.get(BOARDING_POINT_KEY+'_'+STATION_CODE_KEY),
                                                                                                 pnr_json.get(DESTINATION_STATION_KEY+'_'+STATION_CODE_KEY)],
                                                                                  update_train_details=True)
                    train_json[TRAIN_ARRIVAL_DETAILS_KEY] = train_arrival_details
                    return Response({DETAILS_KEY: {PNR_DETAILS_KEY: pnr_json,
                                                   SEAT_DETAILS_KEY: seat_json,
                                                   TRAIN_DETAILS_KEY: train_json,
                                                   SERVER_DATETIME_UTC_KEY: datetime.now(timezone.get_current_timezone()),
                                                   PNR_DETAILS_UPDATE_INTERVAL_KEY: PNR_DETAILS_UPDATE_INTERVAL}},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({DETAILS_KEY: INVALID_PNR_NUMBER}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({DETAILS_KEY: INVALID_PNR_NUMBER}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({DETAILS_KEY: PNR_DETAILS_ALREADY_EXISTS}, status=status.HTTP_400_BAD_REQUEST)


class GetMyJourneys(generics.GenericAPIView):
    """
    This View is responsible for getting all the journeys of the user
    """
    permission_classes = (IsAuthenticated,)

    @method_decorator(permission_required((CAN_GET_MY_JOURNEYS[3] + '.' + CAN_GET_MY_JOURNEYS[0])))
    def get(self, request):
        if self.request.META.get(HTTP_API_VERSION_KEY).lower() == BETA_VERSION_KEY:
            user = UserUtilities.get_user(user=request.user)
            if user:
                journeys = []
                ticket_details = TicketDetailsUtility.get_ticket_details_from_user(user=user)
                if ticket_details.exists():
                    for i in range(0,len(ticket_details)):
                        # Check if the records are Latest or not and update the DB with latest data if the entries in the DB are not latest
                        if not TicketDetailsUtility.is_latest_record(ticket_details[i]):
                            pnr_details = TicketDetailsUtility.get_pnr_details_from_external_api(pnr_no=ticket_details[i].pnr_no)
                            seat_details = SeatDetailsUtility.get_seat_details_from_pnr_details(pnr_details=pnr_details)
                            if seat_details:  # If seat details in not None. Also means it doesn't have any cancelled seats
                                SeatDetailsManager().update_seat_detail_entry(seat_details, ticket_details[i].pnr_no)
                                TicketDetailsManager().update_pnr_entry(old_ticket_details=ticket_details[i],
                                                                        new_ticket_details=pnr_details)
                            else:
                                TicketDetailsManager().update_pnr_entry(old_ticket_details=ticket_details[i],
                                                                        new_ticket_details=None,
                                                                        is_cancelled=True)

                        pnr_details = TicketDetailsUtility.get_pnr_details(ticket_details=ticket_details[i])

                        seat_details = SeatDetailsUtility.get_seat_details(seat_details=SeatDetails.
                                                                        objects.
                                                                        filter(pnr=pnr_details.get(PNR_KEY)))

                        train_details = TrainDetailsUtility.get_train_detail_json(train_details=TrainDetails.
                                                                               objects.
                                                                               get(train_no=ticket_details[i].train_no.train_no))
                        train_arrival_details = TrainDetailsUtility. \
                            get_train_arrival_details_at_stations(train_details=TrainDetails.
                                                                  objects.
                                                                  get(train_no=train_details[TRAIN_NUMBER_KEY]),
                                                                  station_codes=[pnr_details.get(BOARDING_POINT_KEY + '_' + STATION_CODE_KEY),
                                                                                 pnr_details.get(DESTINATION_STATION_KEY + '_' + STATION_CODE_KEY)],
                                                                  update_train_details=True)
                        train_details[TRAIN_ARRIVAL_DETAILS_KEY] = train_arrival_details
                        journeys.append({PNR_DETAILS_KEY: pnr_details,
                                         SEAT_DETAILS_KEY: seat_details,
                                         TRAIN_DETAILS_KEY: train_details})
                    return Response({DETAILS_KEY: journeys,
                                     SERVER_DATETIME_UTC_KEY: datetime.now(timezone.get_current_timezone()),
                                     PNR_DETAILS_UPDATE_INTERVAL_KEY: PNR_DETAILS_UPDATE_INTERVAL}, status=status.HTTP_200_OK)
                else:
                    return Response({DETAILS_KEY: NO_JOURNEYS_EXIST}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({DETAILS_KEY:INVALID_API_VERSION}, status=status.HTTP_400_BAD_REQUEST)


class GetJourney(generics.GenericAPIView):
    """
    View to provide a single journey details based on PNR number
    """
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.META.get(HTTP_API_VERSION_KEY).lower() == BETA_VERSION_KEY:
            return GetJourneySerializer
        raise Exception(INVALID_API_VERSION)

    @method_decorator(permission_required((CAN_GET_MY_JOURNEYS[3] + '.' + CAN_GET_MY_JOURNEYS[0])))
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ticket_details = TicketDetailsUtility.get_ticket_details_from_pnr(pnr_no=request.data.get(PNR_NO_KEY))
        if ticket_details:
            # Check if the records are Latest or not and update the DB with latest data if the entries in the DB are not latest
            if not TicketDetailsUtility.is_latest_record(ticket_details):
                pnr_details = TicketDetailsUtility.get_pnr_details_from_external_api(pnr_no=ticket_details.pnr_no)
                seat_details = SeatDetailsUtility.get_seat_details_from_pnr_details(pnr_details=pnr_details)
                if seat_details:  # If seat details in not None. Also means it doesn't have any cancelled seats
                    SeatDetailsManager().update_seat_detail_entry(seat_details, ticket_details.pnr_no)
                    TicketDetailsManager().update_pnr_entry(old_ticket_details=ticket_details,
                                                            new_ticket_details=pnr_details)
                else:
                    TicketDetailsManager().update_pnr_entry(old_ticket_details=ticket_details,
                                                            new_ticket_details=None,
                                                            is_cancelled=True)

            pnr_details = TicketDetailsUtility.get_pnr_details(ticket_details=ticket_details)

            seat_details = SeatDetailsUtility.get_seat_details(seat_details=SeatDetails.
                                                               objects.
                                                               filter(pnr=pnr_details.get(PNR_KEY)))

            train_details = TrainDetailsUtility.get_train_detail_json(train_details=TrainDetails.
                                                                      objects.
                                                                      get(train_no=ticket_details.train_no.train_no))
            train_arrival_details = TrainDetailsUtility. \
                get_train_arrival_details_at_stations(train_details=TrainDetails.
                                                      objects.
                                                      get(train_no=train_details[TRAIN_NUMBER_KEY]),
                                                      station_codes=[
                                                          pnr_details.get(BOARDING_POINT_KEY + '_' + STATION_CODE_KEY),
                                                          pnr_details.get(
                                                              DESTINATION_STATION_KEY + '_' + STATION_CODE_KEY)],
                                                      update_train_details=True)
            train_details[TRAIN_ARRIVAL_DETAILS_KEY] = train_arrival_details
            return Response({DETAILS_KEY: {PNR_DETAILS_KEY: pnr_details,
                             SEAT_DETAILS_KEY: seat_details,
                             TRAIN_DETAILS_KEY: train_details},
                             SERVER_DATETIME_UTC_KEY: datetime.now(timezone.get_current_timezone()),
                             PNR_DETAILS_UPDATE_INTERVAL_KEY: PNR_DETAILS_UPDATE_INTERVAL}, status=status.HTTP_200_OK)
        else:
            return Response({DETAILS_KEY: INVALID_PNR_NUMBER}, status=status.HTTP_400_BAD_REQUEST)

