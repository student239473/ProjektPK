# Generated by Django 5.2 on 2025-05-23 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_car_drive_wheel'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='is_reserved',
            field=models.BooleanField(default=False),
        ),
    ]
