# Generated by Django 4.0.4 on 2022-07-06 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0040_alter_discourseseries_discourse_series'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='tag',
            field=models.CharField(blank=True, default='', max_length=100, null=True, unique=True),
        ),
    ]
