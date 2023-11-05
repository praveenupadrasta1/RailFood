# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timedelta

from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

from core.utils import convert_datetime_to_utc
from core.formats import IST_TIMEZONE
from core.permissions import CAN_GET_TRAIN_LIVE_STATUS_CONSUMER
from BAAS.config import HTTP_API_VERSION_KEY, BETA_VERSION_KEY, DETAILS_KEY, INVALID_API_VERSION, PNR_NO_KEY, INVALID_PNR_NUMBER, \
                        TRAIN_DAY_NUMBER_KEY, IS_LIVE_STATUS
from serializers import TrainLiveStatusSerializer
from ticket_details.utilities.TicketDetailsUtility import TicketDetailsUtility
from ticket_details.utilities.SeatDetailsUtility import SeatDetailsUtility
from ticket_details.ModelManagers.SeatDetailsManager import SeatDetailsManager
from ticket_details.ModelManagers.TicketDetailsManager import TicketDetailsManager
from train_details.utilities.TrainDetailsUtility import TrainDetailsUtility
from train_details.utilities.TrainLiveStatusUtility import TrainLiveStatusUtility
from train_details.models import TrainDetails

# Create your views here.


class GetTrainLiveStatusForConsumer(generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.META.get(HTTP_API_VERSION_KEY).lower() == BETA_VERSION_KEY:
            return TrainLiveStatusSerializer
        raise Exception(INVALID_API_VERSION)

    @method_decorator(permission_required((CAN_GET_TRAIN_LIVE_STATUS_CONSUMER[3] + '.' + CAN_GET_TRAIN_LIVE_STATUS_CONSUMER[0])))
    def post(self, request):
        pnr_no = request.data.get(PNR_NO_KEY)
        ticket_details = TicketDetailsUtility.get_ticket_details_from_pnr(pnr_no=pnr_no)
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

            pnr_details = TicketDetailsUtility.get_ticket_details_from_pnr(pnr_no=pnr_no)
            train_no = pnr_details.train_no.train_no
            doj = pnr_details.date_of_journey
            train_details = TrainDetails.objects.get(train_no=train_no)
            train_arrival_details = TrainDetailsUtility.get_train_arrival_details_at_stations(train_details=train_details,
                                                                                              station_codes=[pnr_details.
                                                                                                            boarding_station.
                                                                                                            station_code],
                                                                                              update_train_details=True)
            # Subtracting the day the passenger boarded the train with the date of journey gives the train start date
            # at source station
            day_number = train_arrival_details.get(pnr_details.boarding_station.station_code).get(TRAIN_DAY_NUMBER_KEY)-1
            train_start_date = doj + timedelta(days=(-1*day_number))
            train_start_time = train_details.train_start_time
            train_start_date_time = datetime.combine(train_start_date, train_start_time)
            live_status = None
            if datetime.now(timezone.get_current_timezone()) >= convert_datetime_to_utc(train_start_date_time, IST_TIMEZONE):
                if TrainLiveStatusUtility.is_train_live_status_exists(train_no=train_no,
                                                                      train_start_date=train_start_date):
                    if not TrainLiveStatusUtility.is_latest_record(train_no=train_no,
                                                               train_start_date=train_start_date):
                        live_status = TrainLiveStatusUtility.get_live_train_status_from_external_api(train_no=train_no,
                                                                                                     train_start_date=train_start_date)
                else:
                    live_status = TrainLiveStatusUtility.get_live_train_status_from_external_api(train_no=train_no,
                                                                                                 train_start_date=train_start_date)
                TrainLiveStatusUtility.put_data_in_db(train_no=train_no,
                                                      train_start_date=train_start_date,
                                                                  live_status=live_status)
                train_live_status_json = TrainLiveStatusUtility.get_train_live_status_json(train_no=train_no,
                                                                  train_start_date=train_start_date)
                return Response({DETAILS_KEY: train_live_status_json,
                                 IS_LIVE_STATUS: True}, status=status.HTTP_200_OK)
            else:
                train_live_status_json = TrainDetailsUtility.get_route_json(train_details)
                return Response({DETAILS_KEY: train_live_status_json,
                                 IS_LIVE_STATUS: False}, status=status.HTTP_200_OK)
        else:
            return Response({DETAILS_KEY: INVALID_PNR_NUMBER}, status=status.HTTP_400_BAD_REQUEST)