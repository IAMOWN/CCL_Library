# Generated by Django 4.0.4 on 2022-07-14 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0044_alter_libraryobservation_observer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cosmicauthor',
            name='author',
            field=models.CharField(default='', max_length=100, unique=True, verbose_name='master'),
        ),
        migrations.AlterField(
            model_name='discourseseries',
            name='discourse_series',
            field=models.CharField(default='', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='tag',
            field=models.CharField(default='', max_length=100, unique=True),
        ),
    ]
