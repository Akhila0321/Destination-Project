# Generated by Django 5.1.2 on 2024-11-01 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0006_remove_booking_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='number_of_guests',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='booking',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
