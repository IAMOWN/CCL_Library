# Generated by Django 4.0.4 on 2022-06-29 19:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0034_remove_libraryobservation_header_title_observation_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='libraryobservation',
            name='general_observation',
        ),
    ]