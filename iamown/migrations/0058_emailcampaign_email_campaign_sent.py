# Generated by Django 4.0.4 on 2022-07-11 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iamown', '0057_alter_emailcampaign_send_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailcampaign',
            name='email_campaign_sent',
            field=models.CharField(choices=[('No', 'No'), ('Yes', 'Yes')], default='No', max_length=10),
        ),
    ]