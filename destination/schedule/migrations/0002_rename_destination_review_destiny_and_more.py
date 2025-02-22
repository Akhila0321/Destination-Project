# Generated by Django 5.1.2 on 2024-10-23 14:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
        ('tours', '0006_alter_accommodation_availability_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='destination',
            new_name='destiny',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='attracts',
        ),
        migrations.AddField(
            model_name='booking',
            name='destiny',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tours.destiny'),
        ),
    ]
