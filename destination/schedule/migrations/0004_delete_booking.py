# Generated by Django 5.1.2 on 2024-10-28 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_alter_booking_destiny_alter_booking_total_price_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Booking',
        ),
    ]
