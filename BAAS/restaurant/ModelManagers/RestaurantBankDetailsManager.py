from datetime import datetime

from django.db import models
from django.utils import timezone

from BAAS.config import ACCOUNT_NAME_KEY, ACCOUNT_NUMBER_KEY, BANK_NAME_KEY, IFSC_CODE_KEY

import logging
logger = logging.getLogger(__name__)


class RestaurantBankDetailsManager(models.Manager):

    def create(self, user, data):
        try:
            bank_info = self.model(restaurant=user,
                                      account_name=data.get(ACCOUNT_NAME_KEY),
                                      account_number=data.get(ACCOUNT_NUMBER_KEY),
                                      IFSC_code=data.get(IFSC_CODE_KEY),
                                      bank_name=data.get(BANK_NAME_KEY),
                                      created_datetime=datetime.now(timezone.get_current_timezone()),
                                      last_updated=datetime.now(timezone.get_current_timezone())
                                      )
            bank_info.save()
            return bank_info
        except Exception as e:
            logger.error(str(e))
            raise Exception(e)

    def update(self, user, data, bank_details):
        try:
            bank_details.account_name = data.get(ACCOUNT_NAME_KEY)
            bank_details.account_number = data.get(ACCOUNT_NUMBER_KEY)
            bank_details.IFSC_code = data.get(IFSC_CODE_KEY)
            bank_details.bank_name = data.get(BANK_NAME_KEY)
            bank_details.last_updated = datetime.now(timezone.get_current_timezone())
            bank_details.save()
            logger.info(str(user) + 'has changed the bank details at ' + str(bank_details.last_updated))
            return bank_details
        except Exception as e:
            logger.error(str(e))
            raise Exception(e)