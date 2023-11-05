from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import Group
from user_authentication.utilities.GroupUtility import GroupUtility

import logging
logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User`.

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """
    def create_user(self, email, password, role):
        """Create and return a 'user' with and email, username and password"""
        # if username is None:
        #     raise TypeError('Users must have a username')

        if email is None:
            raise TypeError('Users must have an Email address')

        if password is None:
            raise TypeError('Users must have a password')

        user = self.model(email=self.normalize_email(email),
                          created_datetime=datetime.now(timezone.get_current_timezone()),
                          updated_datetime=datetime.now(timezone.get_current_timezone()),
                          last_login=datetime.now(timezone.get_current_timezone()),
                          role=str(role))
        user.set_password(password)
        user.save()

        group_name = GroupUtility.get_group(role=role)
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.set([group])
        user.save()

        # perms = PermissionsUtility.get_permissions(group_name=group_name)
        # if perms:
        #     group.permissions.set(perms)
        # else:
        #     group.permissions.clear()
        return user

    def create_superuser(self, username, email, password, role):
        """
        Create and return a 'user' with superuser (admin) permissions
        :param username:
        :param email:
        :param password:
        :return:
        """
        if password is None:
            raise TypeError('Superusers must have a password')

        user = self.create_user(email=email, password=password, role=role)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

    def delete_user(self, user):
        """
        This method is responsible for deleting a particular user instance from DB
        :param user:
        :return:
        """
        try:
            user.is_active = False
            user.updated_datetime = datetime.now(timezone.get_current_timezone())
            user.save()
            return True
        except Exception as e:
            logger.error(e)
            return False

    def change_password(self, user, password):
        """
        This method is used to change the password for a particular user
        :param password:
        :return:
        """
        try:
            user.set_password(password)
            user.updated_datetime = datetime.now(timezone.get_current_timezone())
            user.save()
            return True
        except Exception as e:
            logger.error(e)
            return False
