# Generated by Django 4.0.4 on 2022-07-25 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0049_alter_recordread_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='recordread',
            name='client_ip',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
