# Generated by Django 4.0.4 on 2022-06-29 19:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0032_alter_libraryobservation_observation_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='libraryobservation',
            name='library_record',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='record_in_observation', to='library.libraryrecord'),
        ),
    ]