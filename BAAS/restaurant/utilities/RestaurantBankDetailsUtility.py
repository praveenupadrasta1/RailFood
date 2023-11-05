from restaurant.models import RestaurantBankDetails
from BAAS.config import ACCOUNT_NAME_KEY, ACCOUNT_NUMBER_KEY, BANK_NAME_KEY, IFSC_CODE_KEY, RESTAURANT_ID_KEY

import logging
logger = logging.getLogger(__name__)


class RestaurantBankDetailsUtility:

    @staticmethod
    def put_data_in_db(request, is_update):
        if not is_update:
            return RestaurantBankDetails.bank_details.create(user=request.user, data=request.data)
        else:
            bank = RestaurantBankDetailsUtility.get_bank_details(user=request.user)
            if bank:
                return RestaurantBankDetails.bank_details.update(user=request.user, data=request.data, bank_details=bank)
            else:
                return RestaurantBankDetails.bank_details.create(user=request.user, data=request.data)

    @staticmethod
    def frame_data(bank_details):
        bank = dict()
        bank[RESTAURANT_ID_KEY] = bank_details.restaurant.id
        bank[ACCOUNT_NAME_KEY] = bank_details.account_name
        bank[ACCOUNT_NUMBER_KEY] = bank_details.account_number
        bank[BANK_NAME_KEY] = bank_details.bank_name
        bank[IFSC_CODE_KEY] = bank_details.IFSC_code
        return bank

    @staticmethod
    def get_bank_details(user):
        try:
            return RestaurantBankDetails.objects.get(restaurant=user)
        except Exception as e:
            logger.error(str(e))
            return None