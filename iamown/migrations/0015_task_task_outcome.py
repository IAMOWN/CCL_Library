# Generated by Django 4.0.4 on 2022-06-28 00:58

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('iamown', '0014_alter_task_task_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='task_outcome',
            field=tinymce.models.HTMLField(blank=True, default='', null=True),
        ),
    ]