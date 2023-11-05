# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid

from django.db import models

from train_details.models import TrainDetails
from user_authentication.models import User

# Create your models here.


class StationDetails(models.Model):
    station_code = models.CharField(primary_key=True, max_length=7, db_index=True)
    station_name = models.CharField(max_length=30)
    state = models.CharField(max_length=20)
    latitude = models.CharField(max_length=15)
    longitude = models.CharField(max_length=15)
    created_datetime = models.DateTimeField()
    last_updated = models.DateTimeField()

    objects = models.Manager()


class TicketDetails(models.Model):
    pnr_no = models.BigIntegerField(primary_key=True, db_index=True)
    user = models.ForeignKey(User, related_name='user', on_delete=models.DO_NOTHING)
    date_of_journey = models.DateField()
    boarding_station = models.OneToOneField(StationDetails, related_name='boarding_station_id', on_delete=models.DO_NOTHING)
    destination_station = models.OneToOneField(StationDetails, related_name='destination_station_id', on_delete=models.DO_NOTHING)
    train_no = models.OneToOneField(TrainDetails)
    is_cancelled = models.BooleanField()
    is_chart_prepared = models.BooleanField()
    created_datetime= models.DateTimeField()
    last_updated = models.DateTimeField()

    objects = models.Manager()


class SeatDetails(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pnr = models.ForeignKey(TicketDetails, related_name='pnr', on_delete=models.DO_NOTHING, db_index=True)
    seat_no = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    created_datetime = models.DateTimeField()
    last_updated = models.DateTimeField()

    objects = models.Manager()
