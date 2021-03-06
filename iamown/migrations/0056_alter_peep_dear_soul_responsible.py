# Generated by Django 4.0.4 on 2022-07-10 22:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('iamown', '0055_emailcampaign_number_of_accepted_reviews_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peep',
            name='dear_soul_responsible',
            field=models.ForeignKey(help_text='Select the Dear Soul responsible for this task. Please note that this required field is integral to ServiceFlow automation in that information in both this field and Process function is used to, where appropriate, assign tasks as a part of ServiceFlow.', on_delete=django.db.models.deletion.CASCADE, related_name='dear_soul_in_peep', to=settings.AUTH_USER_MODEL),
        ),
    ]
