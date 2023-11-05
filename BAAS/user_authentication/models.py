# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import calendar
import jwt
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .ModelManagers import UserManager, OTPManager
from BAAS.config import CONSUMER, RESTAURANT, DELIVERY_BOY

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):

    # The first option is the way it stored in DB and second option is the Human readable format
    ROLES_CHOICE = (('0', CONSUMER),
                    ('1', RESTAURANT),
                    ('2', DELIVERY_BOY),)

    # Each `User` needs a human-readable unique identifier that we can use to
    # represent the `User` in the UI. We want to index this column in the
    # database to improve lookup performance.
    # username = models.CharField(db_index=True, max_length=255, unique=True)

    # We also need a way to contact the user and a way for the user to identify
    # themselves when logging in. Since we need an email address for contacting
    # the user anyways, we will also use the email for logging in because it is
    # the most common form of login credential at the time of writing.
    email = models.EmailField(db_index=True, unique=True)
    # mobile_num = models.CharField(max_length=13, unique=True)

    # When a user no longer wishes to use our platform, they may try to delete
    # their account. That's a problem for us because the data we collect is
    # valuable to us and we don't want to delete it. We
    # will simply offer users a way to deactivate their account instead of
    # letting them delete it. That way they won't show up on the site anymore,
    # but we can still analyze the data.
    is_active = models.BooleanField(default=True)

    # The `is_staff` flag is expected by Django to determine who can and cannot
    # log into the Django admin site. For most users this flag will always be
    # false.
    is_staff = models.BooleanField(default=False)

    # A timestamp representing when this object was created.
    created_datetime = models.DateTimeField()

    # A timestamp reprensenting when this object was last updated.
    updated_datetime = models.DateTimeField()

    # A role to determine who the user is, ex: End-user, Restaurant user, Delivery boy
    role = models.CharField(choices=ROLES_CHOICE, max_length=1)

    # Boolean fields which is used to know whether the mobile and email are verified
    # is_mobile_num_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case we want it to be the email field.
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager.UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        return self.email

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    # def get_full_name(self):
    #     """
    #     This method is required by Django for things like handling emails.
    #     Typically this would be the user's first and last name. Since we do
    #     not store the user's real name, we return their username instead.
    #     """
    #     return self.username
    #
    # def get_short_name(self):
    #     """
    #     This method is required by Django for things like handling emails.
    #     Typically, this would be the user's first name. Since we do not store
    #     the user's real name, we return their username instead.
    #     """
    #     return self.username

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': calendar.timegm(dt.timetuple())
        }, settings.SECRET_KEY, 'HS256')

        return token.decode('utf-8')


class OTP(models.Model):
    """
    This model is responsibe for OTP generation and verification of Email and Mobile Number
    """
    OTP_CATEGORIES = (('EMAIL', 'email'),)
    otp_id = models.AutoField(primary_key=True, editable=False,)
    username = models.ForeignKey('User', on_delete=models.CASCADE,)
    otp = models.IntegerField(unique=True)
    category = models.CharField(choices=OTP_CATEGORIES, max_length=6)
    created_datetime = models.DateTimeField()
    no_failed_attempts = models.IntegerField(default=0)

    otp_objects = OTPManager.OTPManager()
    objects = models.Manager()
