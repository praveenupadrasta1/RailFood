# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid

# Create your models here.


class TrainDetails(models.Model):
    train_no = models.IntegerField(primary_key=True, db_index=True)
    train_name = models.CharField(max_length=30)
    routeJSON = models.TextField(blank=False)
    train_start_time = models.TimeField()
    created_datetime = models.DateTimeField()
    last_updated = models.DateTimeField()

    objects = models.Manager()


class TrainLiveStatus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    train_no = models.IntegerField(db_index=True)
    train_start_date = models.DateField()
    live_status = models.TextField(blank=False)
    created_datetime = models.DateTimeField()
    last_updated = models.DateTimeField()

    objects = models.Manager()

    class Meta:
        unique_together = (('train_no', 'train_start_date'))


class CancelledTrains(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cancelled_train_date = models.DateField()
    # Cannot link with foreign key because the train number may not exist in TrainDetails table.
    train_no = models.IntegerField(db_index=True)
    train_name = models.CharField(max_length=30)
    created_datetime = models.DateTimeField()
    last_updated = models.DateTimeField()

    objects = models.Manager()

    class Meta:
        unique_together = (('train_no', 'cancelled_train_date'),)


class RescheduledTrains(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Cannot link with foreign key because the train number may not exist in TrainDetails table.
    train_no = models.IntegerField(db_index=True)
    train_name = models.CharField(max_length=50)
    rescheduled_date = models.DateField()
    rescheduled_to_time_in_IST = models.TimeField()
    rescheduled_to_date_in_IST = models.DateField()
    created_datetime = models.DateTimeField()
    last_updated = models.DateTimeField()

    objects = models.Manager()

    class Meta:
        unique_together = (('train_no', 'rescheduled_date'),)