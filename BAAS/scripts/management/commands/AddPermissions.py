from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.permissions import USER_PERMISSIONS


class Command(BaseCommand):

    help = "This Command adds the permissions to the database and assigns those permissions to the groups"

    def handle(self, *args, **options):
        self.stdout.write("Adding/Updating Permissions........")

        groups = USER_PERMISSIONS.keys()

        for group in groups:
            new_group, created = Group.objects.get_or_create(name=group)

            permissions = USER_PERMISSIONS.get(group)
            temp_perms = []
            for codename, name, model, app_name in permissions:
                ct = ContentType.objects.get_for_model(model)
                perm, created = Permission.objects.get_or_create(codename=codename, name=name, content_type=ct)
                temp_perms.append(perm)
            if temp_perms:
                new_group.permissions.set(temp_perms)
            else:
                new_group.permissions.clear()

        self.stdout.write("Permissions added/updated successfully.......")