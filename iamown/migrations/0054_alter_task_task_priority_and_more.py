# Generated by Django 4.0.4 on 2022-07-10 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iamown', '0053_task_email_campaign_test_accepted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_priority',
            field=models.CharField(choices=[('1) High', '1) High'), ('2) Normal', '2) Normal'), ('3) Low', '3) Low')], default='2) Normal', help_text='Task Priority is used to help determine the order of displayed tasks. The ordering of tasks is by: Status, then Priority, and finally Due Date. Selecting "1) High" presents tasks higher in the list, while selecting "3) Low" is a way of moving longer-term tasks to the end of the task list.', max_length=20),
        ),
        migrations.AlterUniqueTogether(
            name='emailcampaign',
            unique_together={('audience', 'subject')},
        ),
    ]
