# Generated by Django 4.0.4 on 2022-06-19 23:28

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0019_readingprogress_date_latest_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readingprogress',
            name='reading_progress_log',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
    ]
