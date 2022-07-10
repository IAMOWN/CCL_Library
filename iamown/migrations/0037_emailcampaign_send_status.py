# Generated by Django 4.0.4 on 2022-07-09 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iamown', '0036_emailcampaign'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailcampaign',
            name='send_status',
            field=models.CharField(blank=True, choices=[('1) Created', '1) Created'), ('2) In progress', '2) In progress'), ('3) Approved', '3) Approved'), ('Sent', 'Sent')], default='1) Created', max_length=20, null=True),
        ),
    ]