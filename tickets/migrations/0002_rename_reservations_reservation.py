# Generated by Django 4.2.8 on 2023-12-13 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("tickets", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(old_name="Reservations", new_name="Reservation",),
    ]
