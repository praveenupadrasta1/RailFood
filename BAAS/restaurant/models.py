# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid
from datetime import datetime

from django.db import models
from django.utils import timezone

from BAAS.config import VEGETARIAN, NON_VEGETARIAN, MULTI_CUISINE, BRONZE_MEMBERSHIP, SILVER_MEMBERSHIP, GOLD_MEMBERSHIP, \
    PLATINUM_MEMBERSHIP, BRONZE_MEMBERSHIP_CODE, SILVER_MEMBERSHIP_CODE, GOLD_MEMBERSHIP_CODE, PLATINUM_MEMBERSHIP_CODE
from ticket_details.models import StationDetails
from user_authentication.models import User
from restaurant.ModelManagers.RestaurantProfileManager import RestaurantProfileManager
from restaurant.ModelManagers.RestaurantBankDetailsManager import RestaurantBankDetailsManager

# Create your models here.


class Cuisines(models.Model):

    cuisine_id = models.IntegerField(primary_key=True)
    cuisine_name = models.CharField(max_length=30)


class RestaurantProfile(models.Model):

    CATEGORY_CHOICES = (('V', VEGETARIAN),
                        ('N', NON_VEGETARIAN),
                        ('M', MULTI_CUISINE))
    restaurant = models.OneToOneField(User, related_name='restaurant_profile_restaurant_id', on_delete=models.DO_NOTHING,
                                         db_index=True)
    name = models.CharField(max_length=50, blank=False)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=1, blank=False)
    mobile_number = models.CharField(max_length=13, blank=False)
    address = models.TextField(blank=False)
    image_url = models.CharField(max_length=150, blank=True, null=True)
    order_open_timing_from = models.CharField(max_length=5, blank=False)
    order_open_timing_to = models.CharField(max_length=5, blank=False)
    restaurant_station = models.ForeignKey(StationDetails, related_name='restaurant_profile_restaurant_station',
                                           on_delete=models.DO_NOTHING)
    convenience_fee = models.IntegerField(blank=True, null=True)
    commission_percentage = models.IntegerField(blank=True, null=True)
    cuisines = models.ManyToManyField(Cuisines)
    created_datetime = models.DateTimeField()
    last_updated = models.DateTimeField()

    profile = RestaurantProfileManager()
    objects = models.Manager()


class RestaurantBankDetails(models.Model):

    restaurant = models.OneToOneField(User, related_name='restaurant_bank_details', on_delete=models.DO_NOTHING,
                                         db_index=True)
    account_name = models.CharField(max_length=70, blank=False)
    account_number = models.CharField(max_length=25, blank=False)
    IFSC_code = models.CharField(max_length=25, blank=False)
    bank_name = models.CharField(max_length=40, blank=False)
    created_datetime = models.DateTimeField()
    last_updated = models.DateTimeField()

    bank_details = RestaurantBankDetailsManager()
    objects = models.Manager()


class MembershipDetails(models.Model):

    MEMBERSHIP_CHOICES = ((BRONZE_MEMBERSHIP_CODE, BRONZE_MEMBERSHIP),
                          (SILVER_MEMBERSHIP_CODE, SILVER_MEMBERSHIP),
                          (GOLD_MEMBERSHIP_CODE, GOLD_MEMBERSHIP),
                          (PLATINUM_MEMBERSHIP_CODE, PLATINUM_MEMBERSHIP))

    membership_id = models.IntegerField(primary_key=True, db_index=True)
    membership_type = models.CharField(choices=MEMBERSHIP_CHOICES, max_length=1)
    valid_for_months = models.IntegerField()
    price = models.IntegerField()


class RestaurantMembershipDetails(models.Model):

    restaurant = models.OneToOneField(User, related_name='restaurant_membership_details_restaurant', on_delete=models.DO_NOTHING,
                                         db_index=True)
    membership_type = models.OneToOneField(MembershipDetails, related_name='restaurant_membership_details_membership_type',
                                              on_delete=models.DO_NOTHING)
    membership_valid_from = models.DateTimeField()
    membership_valid_to = models.DateTimeField()
    created_datetime = models.DateTimeField()
    last_updated = models.DateTimeField()


class RestaurantNotification(models.Model):

    notification_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    restaurant = models.ForeignKey(User, related_name='restaurant_notification', on_delete=models.DO_NOTHING,
                                         db_index=True)
    notification_message = models.TextField(blank=False)
    is_viewed = models.BooleanField(default=False)
    created_datetime = models.DateTimeField()


class RestaurantReviewRating(models.Model):

    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    restaurant = models.ForeignKey(User, related_name='restaurant_review_rating_restaurant', on_delete=models.DO_NOTHING,
                                         db_index=True)
    user = models.ForeignKey(User, related_name='restaurant_review_rating_user', on_delete=models.DO_NOTHING,
                                         db_index=True)
    image_urls = models.TextField(blank=True)
    rating = models.IntegerField()
    review = models.CharField(max_length=250, blank=True)
    created_datetime = models.DateTimeField()
    last_updated = models.DateTimeField()