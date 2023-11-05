from rest_framework import status
from django.utils import timezone
from datetime import datetime

from user_authentication.models import OTP
from core.utils import frame_response
from BAAS.config import OTP_EXPIRY_MINUTES_LIMIT, OTP_EXPIRED, INCORRECT_OTP, CATEGORY_KEY, OTP_SENT_SUCCESSFULLY, \
    BAD_CATEGORY, INVALID_REQUEST, OTP_KEY, OTP_FAIL_ATTEMPTS_THRESHOLD
from user_authentication.utilities.UserUtilities import UserUtilities

import logging
logger = logging.getLogger(__name__)


class OTPUtilities:
    """
    This class is responsible for application logic using OTP model
    """

    @staticmethod
    def verify_otp(request):
        """
        This method verifies whether the OTP is correct or not.
        Time limit is 7mins.
        :param data:
        :return:
        """
        # if request.data.get('category') == 'MOBILE':
        #     return OTPUtilities.is_otp_valid(request, user, 'MOBILE')
        if request.data.get(CATEGORY_KEY) == 'EMAIL':
            return OTPUtilities.is_otp_valid(request, 'EMAIL')

        return frame_response(details=BAD_CATEGORY,
                              status=False,
                              status_code=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def is_otp_valid(request, category):
        try:
            otp_row_item, user = OTPUtilities.get_user_otp(user=request.user, category=category)
            if otp_row_item:
                if otp_row_item.no_failed_attempts <= OTP_FAIL_ATTEMPTS_THRESHOLD and OTPUtilities.is_otp_latest(otp_row_item):
                    if otp_row_item.otp == request.data.get(OTP_KEY):
                        user.is_email_verified = True
                        user.save()
                        OTP.otp_objects.delete_otp(otp_row_item)
                        return frame_response(details=category + ' Verification Successful',
                                              status=True,
                                              status_code=status.HTTP_200_OK)
                    else:
                        otp_row_item.no_failed_attempts += 1
                        otp_row_item.save()
                        return frame_response(details=INCORRECT_OTP,
                                              status=False,
                                              status_code=status.HTTP_401_UNAUTHORIZED)
                else:
                    OTP.otp_objects.delete_otp(otp_row_item)
                    return frame_response(details=OTP_EXPIRED,
                                          status=False,
                                          status_code=status.HTTP_401_UNAUTHORIZED)
            else:
                return frame_response(details=INVALID_REQUEST,
                                      status=False,
                                      status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(str(e))
            return frame_response(details=str(e),
                                  status=False,
                                  status_code=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def regenerate_otp(request):
        try:
            category = request.data.get(CATEGORY_KEY)
            otp_row_item, user = OTPUtilities.get_user_otp(user=request.user, category=category)
            if not user.is_email_verified:
                if otp_row_item:
                    OTP.otp_objects.delete_otp(otp_row_item)

                regenrated_otp = OTP.otp_objects.create_otp(user, category)
                ########## Send otp to mail or mobile ###############

                ###################################################
                return frame_response(details=OTP_SENT_SUCCESSFULLY.format(category),
                                      status=True,
                                      status_code=status.HTTP_200_OK)
            else:
                return frame_response(details=INVALID_REQUEST,
                                      status=False,
                                      status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(str(e))
            return frame_response(details=str(e),
                                  status=False,
                                  status_code=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def is_otp_latest(otp):
        return divmod((datetime.now(timezone.utc) - otp.created_datetime).total_seconds(), 60)[0] < OTP_EXPIRY_MINUTES_LIMIT

    @staticmethod
    def resend_otp(request):
        try:
            category = request.data.get(CATEGORY_KEY)
            otp_row_item, user = OTPUtilities.get_user_otp(user=request.user, category=category)
            if otp_row_item:
                if otp_row_item.no_failed_attempts <= OTP_FAIL_ATTEMPTS_THRESHOLD and OTPUtilities.is_otp_latest(otp_row_item):
                    if otp_row_item:
                        ########## Send OTP to email or mobile #############


                        ###################################################
                        return frame_response(details=OTP_SENT_SUCCESSFULLY.format(category),
                                              status=True,
                                              status_code=status.HTTP_200_OK)
                    else:
                        return frame_response(details=INVALID_REQUEST,
                                              status=False,
                                              status_code=status.HTTP_400_BAD_REQUEST)
                else:
                    OTP.otp_objects.delete_otp(otp_row_item)
                    return frame_response(details=OTP_EXPIRED,
                                          status=False,
                                          status_code=status.HTTP_400_BAD_REQUEST)
            else:
                return frame_response(details=INVALID_REQUEST,
                                      status=False,
                                      status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(str(e))
            return frame_response(details=str(e),
                                  status=False,
                                  status_code=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_user_otp(user, category):
        user = UserUtilities.get_user(user=user)
        try:
            otp_row_item = OTP.objects.get(username_id=user, category=category)
            return otp_row_item, user
        except Exception as e:
            logger.error(str(e))
            print str(e)
            return None, user