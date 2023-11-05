# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-04-24 19:51
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CancelledTrains',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('cancelled_train_date', models.DateField()),
                ('train_no', models.IntegerField(db_index=True)),
                ('train_name', models.CharField(max_length=30)),
                ('created_datetime', models.DateTimeField()),
                ('last_updated', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='RescheduledTrains',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('train_no', models.IntegerField(db_index=True)),
                ('train_name', models.CharField(max_length=50)),
                ('rescheduled_date', models.DateField()),
                ('rescheduled_to_time_in_IST', models.TimeField()),
                ('rescheduled_to_date_in_IST', models.DateField()),
                ('created_datetime', models.DateTimeField()),
                ('last_updated', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='TrainDetails',
            fields=[
                ('train_no', models.IntegerField(db_index=True, primary_key=True, serialize=False)),
                ('train_name', models.CharField(max_length=30)),
                ('routeJSON', models.TextField()),
                ('train_start_time', models.TimeField()),
                ('created_datetime', models.DateTimeField()),
                ('last_updated', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='TrainLiveStatus',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('train_no', models.IntegerField(db_index=True)),
                ('train_start_date', models.DateField()),
                ('live_status', models.TextField()),
                ('created_datetime', models.DateTimeField()),
                ('last_updated', models.DateTimeField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='trainlivestatus',
            unique_together=set([('train_no', 'train_start_date')]),
        ),
        migrations.AlterUniqueTogether(
            name='rescheduledtrains',
            unique_together=set([('train_no', 'rescheduled_date')]),
        ),
        migrations.AlterUniqueTogether(
            name='cancelledtrains',
            unique_together=set([('train_no', 'cancelled_train_date')]),
        ),
    ]
