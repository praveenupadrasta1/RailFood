from datetime import datetime

from django.db import models
from core.utils import get_otp
from django.utils import timezone
import logging
logger = logging.getLogger(__name__)


class OTPManager(models.Manager):
    """
    This is OTP manager, responsible for CRUD operations on OTP model
    """
    def create_otp(self, user, category):
        try:
            otp_row = self.model(username=user, otp=get_otp(), category=category,
                                 created_datetime=datetime.now(timezone.get_current_timezone()))
            otp_row.save()
            return otp_row
        except Exception, e:
            logger.error(str(e))
            print str(e)

    def delete_otp(self, otp_row_item):
        try:
            otp_row_item.delete()
        except Exception as e:
            logger.error(str(e))