# Generated by Django 4.0.4 on 2022-07-12 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iamown', '0059_alter_task_task_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailcampaign',
            name='sender_email',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
