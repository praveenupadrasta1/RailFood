from django.core.management import BaseCommand

from restaurant.models import Cuisines
from restaurant.utilities.cuisines import CUISINES
from BAAS.config import RESTAURANT_CUISINES_KEY


class Command(BaseCommand):

    help = "This Command adds the cuisines to the database"

    def handle(self, *args, **options):
        self.stdout.write("Adding/Updating Cuisines........")

        cuisines = CUISINES.get(RESTAURANT_CUISINES_KEY)
        for cuisine in cuisines:
            cuisine_obj = Cuisines.objects.filter(cuisine_id=cuisine[0])
            if cuisine_obj.exists():
                cuisine_obj = cuisine_obj.first()
                cuisine_obj.cuisine_name = cuisine[1]
                cuisine_obj.save()
            else:
                Cuisines.objects.create(cuisine_id=cuisine[0], cuisine_name=cuisine[1])

        self.stdout.write("Cuisines Added/Updated successfully........")