# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-14 11:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_auto_20171223_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availabilitydate',
            name='barn_booking_status',
            field=models.CharField(choices=[('FR', 'free'), ('BK', 'booked'), ('AM', 'bookedAm'), ('PM', 'bookedPm')], default='FR', max_length=2),
        ),
        migrations.AlterField(
            model_name='availabilitydate',
            name='cottage_booking_status',
            field=models.CharField(choices=[('FR', 'free'), ('BK', 'booked'), ('AM', 'bookedAm'), ('PM', 'bookedPm')], default='FR', max_length=2),
        ),
    ]
