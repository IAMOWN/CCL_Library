# Generated by Django 4.0.4 on 2022-07-12 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iamown', '0058_emailcampaign_email_campaign_sent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.CharField(blank=True, choices=[('---', '---'), ('Decision', 'Decision'), ('Library Observation', 'Library Observation'), ('Book Edit', 'Book Edit'), ('Email Campaign', 'Email Campaign'), ('Email Campaign 2', 'Email Campaign 2'), ('Email Campaign 2 - Revise', 'Email Campaign 2 - Revise')], default='---', max_length=50, null=True),
        ),
    ]