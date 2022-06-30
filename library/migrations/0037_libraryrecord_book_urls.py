# Generated by Django 4.0.4 on 2022-06-30 20:53

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0036_libraryobservation_general_observation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='libraryrecord',
            name='book_urls',
            field=tinymce.models.HTMLField(blank=True, default='', null=True),
        ),
    ]
