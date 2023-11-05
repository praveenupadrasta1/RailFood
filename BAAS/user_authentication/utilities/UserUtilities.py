from rest_framework import status

from user_authentication.models import User
from core.utils import generate_random_password, frame_response
from EmailUtility import send_mail
from BAAS.config import NEW_PASSWORD_SET_MESSAGE, VERIFY_EMAIL, INVALID_EMAIL_ADDRESS

import logging
logger = logging.getLogger(__name__)


class UserUtilities:
    """
    This Class defines all the user related utilities
    """

    @staticmethod
    def forgot_password(user_email):
        """
        To create a random password for the user
        :param user:
        :return:
        """
        try:
            user = UserUtilities.get_user(user=user_email)
            if user.is_email_verified:
                new_password = generate_random_password()
                User.objects.change_password(user, new_password)
                ########### send password to email ###########################
                # send_mail([user_email], "Reset password for your Chuk Bhuk account", "The following is the new password for"
                #                                                                    "your Chuk Bhuk account \n"+new_password)
                ###############################################################
                return frame_response(NEW_PASSWORD_SET_MESSAGE, status=True, status_code=status.HTTP_200_OK)
            else:
                return frame_response(VERIFY_EMAIL, status=False, status_code=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            logger.error(e)
            return frame_response(INVALID_EMAIL_ADDRESS, status=False, status_code=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_user(user):
        try:
            return User.objects.get(email=user)
        except Exception as e:
            logger.error(e)
            return None

    @staticmethod
    def is_user_exists(email):
        try:
            User.objects.get(email=email)
            return True
        except Exception as e:
            return False