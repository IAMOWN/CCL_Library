# Generated by Django 4.0.4 on 2022-06-19 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0017_alter_readingprogress_reading_progress'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='readingprogress',
            options={'ordering': ['reading_progress'], 'verbose_name_plural': 'Reading Progress'},
        ),
    ]
