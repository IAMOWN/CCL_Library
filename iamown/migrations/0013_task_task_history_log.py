# Generated by Django 4.0.4 on 2022-06-27 00:16

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('iamown', '0012_alter_task_task_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='task_history_log',
            field=tinymce.models.HTMLField(blank=True, default='', null=True),
        ),
    ]