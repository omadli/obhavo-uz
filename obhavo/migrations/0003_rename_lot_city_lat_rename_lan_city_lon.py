# Generated by Django 4.0.2 on 2022-02-24 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('obhavo', '0002_city'),
    ]

    operations = [
        migrations.RenameField(
            model_name='city',
            old_name='lot',
            new_name='lat',
        ),
        migrations.RenameField(
            model_name='city',
            old_name='lan',
            new_name='lon',
        ),
    ]