# Generated by Django 4.0.4 on 2022-06-29 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0029_libraryobservation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libraryobservation',
            name='observation_type',
            field=models.CharField(choices=[('Typo', 'Typo'), ('Missing Image', 'Missing Image'), ('Broken Link', 'Broken Link'), ('Incorrect Header/Title', 'Incorrect Header/Title')], default='Typo', help_text='Please select the applicable observation type.', max_length=30),
        ),
    ]
