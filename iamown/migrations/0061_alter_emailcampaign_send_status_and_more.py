# Generated by Django 4.0.4 on 2022-07-13 15:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('iamown', '0060_emailcampaign_sender_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailcampaign',
            name='send_status',
            field=models.CharField(blank=True, choices=[('1) Created', '1) Created'), ('2) In progress', '2) In progress'), ('3) Declined', '3) Declined'), ('Sent', 'Sent')], default='1) Created', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='emailcampaign',
            name='sender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user_in_email_campaign', to=settings.AUTH_USER_MODEL),
        ),
    ]
