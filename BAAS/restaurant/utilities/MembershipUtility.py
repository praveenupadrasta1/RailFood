from restaurant.models import MembershipDetails
from BAAS.config import PRICE_KEY, VALIDITY_KEY, TYPE_KEY

import logging
logger = logging.getLogger(__name__)


class MembershipUtility:

    @staticmethod
    def is_membership_exists(membership_id):
        try:
            return MembershipDetails.objects.get(membership_id=membership_id)
        except Exception as e:
            return None

    @staticmethod
    def get_all_memberships():
        try:
            return MembershipDetails.objects.all()
        except Exception as e:
            logger.error(str(e))
            raise Exception(e)

    @staticmethod
    def frame_data(membership_obj):
        membership = dict()
        membership[TYPE_KEY] = membership_obj.membership_type
        membership[VALIDITY_KEY] = membership_obj.valid_for_months
        membership[PRICE_KEY] = membership_obj.price
        return membership