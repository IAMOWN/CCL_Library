# Generated by Django 4.0.4 on 2022-06-27 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iamown', '0013_task_task_history_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_priority',
            field=models.CharField(choices=[('1) High', '1) High'), ('2) Normal', '2) Normal'), ('3) Low', '3) Low')], default='2) Normal', help_text="Selecting '1) High' will not only place the task higher in the task list.", max_length=20),
        ),
    ]