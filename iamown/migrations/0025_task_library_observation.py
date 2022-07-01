# Generated by Django 4.0.4 on 2022-07-01 20:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0038_alter_libraryrecord_book_urls_and_more'),
        ('iamown', '0024_task_library_task_actions_taken'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='library_observation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='library_observation_in_library_task', to='library.libraryobservation'),
        ),
    ]
