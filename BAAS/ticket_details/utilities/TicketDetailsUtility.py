from datetime import datetime

from django.conf import settings
from django.utils import timezone

from core.utils import get_data_from_external_api, convert_date_format, get_local_time_from_utc, convert_str_to_date_obj
from ticket_details.ModelManagers.TicketDetailsManager import TicketDetailsManager
from ticket_details.utilities.SeatDetailsUtility import SeatDetailsUtility
from train_details.ModelManagers.CancelledTrainsManager import CancelledTrainsManger
from train_details.ModelManagers.RescheduledTrainsManager import RescheduledTrainsManager
from train_details.utilities.CancelledTrainsUtility import CancelledTrainsUtility
from train_details.utilities.RescheduledTrainsUtility import RescheduledTrainsUtility
from ticket_details.ModelManagers.SeatDetailsManager import SeatDetailsManager
from core.utils import get_mins_difference_between_two_dates
from BAAS.config import DOJ_KEY, ERROR_DELETING_CANCELLED_TRAIN_RECORDS, PNR_KEY, BOARDING_POINT_KEY, \
    DESTINATION_STATION_KEY, IS_TICKET_CANCELLED, CHART_PREPARED_KEY, IS_TRAIN_CANCELLED_KEY, \
    ERROR_DELETING_RESCHEDULED_TRAIN_RECORDS, IS_TRAIN_RESCHEDULED_KEY, RESCHEDULED_TO_DATE_KEY, RESCHEDULED_TO_TIME_KEY, \
    STATION_CODE_KEY, STATION_NAME_KEY, PNR_DETAILS_UPDATE_INTERVAL, LAST_UPDATED_UTC_KEY
from core.formats import DATE_INPUT_FORMAT, ACCEPTED_DATE_FORMAT
from user_authentication.models import User

from ticket_details.models import TicketDetails
import logging
logger = logging.getLogger(__name__)


class TicketDetailsUtility:

    @staticmethod
    def get_pnr_details_from_external_api(pnr_no):
        return get_data_from_external_api(settings.RAILWAY_API_BASE_URL + 'v2/pnr-status/pnr/' +
                                   str(pnr_no) + '/apikey/' + settings.RAILWAY_API_KEY + '/')

    @staticmethod
    def is_pnr_number_exists(pnr_no):
        try:
            TicketDetails.objects.get(pnr_no=pnr_no)
            return True
        except Exception as e:
            return False

    @staticmethod
    def get_ticket_details_from_user(user):
        try:
            return TicketDetails.objects.filter(user=user)
        except Exception as e:
            logger.error(str(e))
            return None

    @staticmethod
    def get_ticket_details_from_pnr(pnr_no):
        try:
            return TicketDetails.objects.get(pnr_no=pnr_no)
        except Exception as e:
            logger.error(e)
            return None

    @staticmethod
    def put_data_in_db(user, pnr_details, station_details, train_details):
        try:
            doj = pnr_details.get(DOJ_KEY)
            converted_date = convert_date_format(doj, DATE_INPUT_FORMAT, ACCEPTED_DATE_FORMAT)
            cancelled_trains = CancelledTrainsUtility.is_cancelled_trains_exists(date=doj)
            # rescheduled_trains = RescheduledTrainsUtility.is_rescheduled_trains_exists(date=doj)

            # If the cancelled trains exists on the particular day, check if they are not latest
            # If the cancelled trains doesn't exist
            # In both the above conditions it should populate the DB
            if cancelled_trains and (not CancelledTrainsUtility.is_latest_record(cancelled_train=cancelled_trains[0])):
                data = CancelledTrainsUtility.get_cancelled_trains_from_external_api(date=doj)
                is_deleted = CancelledTrainsManger().delete_entries_based_on_date(date=converted_date)
                if is_deleted:
                    CancelledTrainsUtility.put_data_in_db(data=data, cancelled_train_date=converted_date)
                else:
                    raise Exception(ERROR_DELETING_CANCELLED_TRAIN_RECORDS)
            else:
                data = CancelledTrainsUtility.get_cancelled_trains_from_external_api(date=doj)
                CancelledTrainsUtility.put_data_in_db(data=data, cancelled_train_date=converted_date)

            # If the rescheduled trains exists on the particular day, check if they are not latest
            # If the rescheduled trains doesn't exist
            # In both the above conditions it should populate the DB
            # print 'date of journey'
            # print doj
            # if get_local_time_from_utc(date=convert_str_to_date_obj(datetime.now().strftime(DATE_INPUT_FORMAT))) == doj:
            #     print 'yes the dates are equal'
            #     if rescheduled_trains and (not RescheduledTrainsUtility.is_latest_records(rescheduled_trains=rescheduled_trains)):
            #         data = RescheduledTrainsUtility.get_rescheduled_trains_from_external_api(date=doj)
            #         is_deleted = RescheduledTrainsManager().delete_entries_based_on_date(date=converted_date)
            #         if is_deleted:
            #             RescheduledTrainsUtility.put_data_in_db(data=data, rescheduled_date=converted_date)
            #         else:
            #             raise Exception(ERROR_DELETING_RESCHEDULED_TRAIN_RECORDS)
            #     else:
            #         data = RescheduledTrainsUtility.get_rescheduled_trains_from_external_api(date=doj)
            #         RescheduledTrainsUtility.put_data_in_db(data=data, rescheduled_date=converted_date)

            # Now save the pnr details
            return TicketDetailsManager().create_pnr_entry(user, pnr_details=pnr_details,
                                                  station_details=station_details,
                                                  train_details=train_details)
        except Exception as e:
            logger.error(str(e))
            raise Exception(e)

    @staticmethod
    def get_pnr_details(ticket_details):
        try:
            # journeys = []
            # if ticket_details.exists():
            #     for ticket in ticket_details:
            pnr_details = TicketDetailsUtility.frame_pnr_data(ticket_details=ticket_details)
            #         journeys.append(pnr_details)
            #     return journeys
            # else:
            return pnr_details
        except Exception as e:
            logger.error(str(e))
            print str(e)
            raise Exception(e)

    @staticmethod
    def frame_pnr_data(ticket_details):
        try:
            pnr_details = dict()
            pnr_details[PNR_KEY] = ticket_details.pnr_no
            pnr_details[DOJ_KEY] = ticket_details.date_of_journey
            pnr_details[BOARDING_POINT_KEY + '_' + STATION_CODE_KEY] = ticket_details.boarding_station.station_code
            pnr_details[BOARDING_POINT_KEY + '_' + STATION_NAME_KEY] = ticket_details.boarding_station.station_name
            pnr_details[DESTINATION_STATION_KEY + '_' + STATION_CODE_KEY] = ticket_details.destination_station.station_code
            pnr_details[DESTINATION_STATION_KEY + '_' + STATION_NAME_KEY] = ticket_details.destination_station.station_name
            pnr_details[LAST_UPDATED_UTC_KEY] = ticket_details.last_updated
            pnr_details[IS_TICKET_CANCELLED] = ticket_details.is_cancelled
            pnr_details['is_' + CHART_PREPARED_KEY] = ticket_details.is_chart_prepared

            is_train_cancelled = CancelledTrainsUtility.is_train_cancelled(train_no=ticket_details.train_no.train_no,
                                                                           date=ticket_details.date_of_journey)
            # rescheduled_train = RescheduledTrainsUtility.is_train_rescheduled(train_no=ticket_details.train_no.train_no,
            #                                                                      date=ticket_details.date_of_journey)
            pnr_details[IS_TRAIN_CANCELLED_KEY] = is_train_cancelled
            # if rescheduled_train:
            #     pnr_details[IS_TRAIN_RESCHEDULED_KEY] = True
            #     pnr_details[RESCHEDULED_TO_DATE_KEY] = rescheduled_train.rescheduled_to_date
            #     pnr_details[RESCHEDULED_TO_TIME_KEY] = rescheduled_train.rescheduled_to_time
            # else:
            #     pnr_details[IS_TRAIN_RESCHEDULED_KEY] = False

            return pnr_details
        except Exception as e:
            logger.error(str(e))
            print str(e)
            raise Exception(e)

    @staticmethod
    def get_last_updated_date(ticket_details):
        return ticket_details.last_updated

    @staticmethod
    def is_latest_record(ticket_details):
        if get_mins_difference_between_two_dates(from_date=datetime.now(timezone.get_current_timezone()),
                                                 to_date=TicketDetailsUtility.get_last_updated_date(ticket_details)) \
                                                > PNR_DETAILS_UPDATE_INTERVAL:
            return False
        else:
            return True