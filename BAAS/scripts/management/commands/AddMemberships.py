from django.core.management import BaseCommand

from restaurant.models import MembershipDetails
from restaurant.utilities.memberships import MEMBERSHIP_DETAILS
from restaurant.utilities.MembershipUtility import MembershipUtility
from BAAS.config import TYPE_KEY, PRICE_KEY, VALIDITY_KEY


class Command(BaseCommand):

    help = "This Command adds the memberships to the database"

    def handle(self, *args, **options):
        self.stdout.write("Adding/Updating Memberships........")

        for membership_id in MEMBERSHIP_DETAILS.keys():
            membership_details = MEMBERSHIP_DETAILS.get(membership_id)
            membership_obj = MembershipUtility.is_membership_exists(membership_id)
            if not membership_obj:
                MembershipDetails.objects.create(membership_id=membership_id,
                                                 membership_type=membership_details.get(TYPE_KEY),
                                                 valid_for_months=membership_details.get(VALIDITY_KEY),
                                                 price = membership_details.get(PRICE_KEY))
            else:
                membership_obj.membership_id=membership_id
                membership_obj.membership_type=membership_details.get(TYPE_KEY)
                membership_obj.valid_for_months = membership_details.get(VALIDITY_KEY)
                membership_obj.price = membership_details.get(PRICE_KEY)
                membership_obj.save()

        self.stdout.write("Memberships Added/Updated successfully........")