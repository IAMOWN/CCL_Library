# Generated by Django 4.0.4 on 2022-06-29 19:58

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0035_remove_libraryobservation_general_observation'),
    ]

    operations = [
        migrations.AddField(
            model_name='libraryobservation',
            name='general_observation',
            field=tinymce.models.HTMLField(blank=True, help_text='Please describe what you are observing and what you believe could be changed or corrected.', null=True),
        ),
        migrations.AddField(
            model_name='libraryobservation',
            name='header_title_observation',
            field=tinymce.models.HTMLField(blank=True, help_text='Please describe what is not correct in the Header or Title of the record.', null=True),
        ),
    ]