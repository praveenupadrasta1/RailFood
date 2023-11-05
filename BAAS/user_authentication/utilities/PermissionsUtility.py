from django.contrib.auth.models import Permission
from core.permissions import USER_PERMISSIONS


class PermissionsUtility:

    @staticmethod
    def get_permissions(group_name):

        ROLE_PERMISSIONS = USER_PERMISSIONS.get(group_name)

        if ROLE_PERMISSIONS:
            temp_permissions = []
            for PERMISSION in ROLE_PERMISSIONS:
                temp_permissions.append(Permission.objects.get(codename=PERMISSION))
            return temp_permissions
        return None