# Generated by Django 4.0.4 on 2022-07-13 15:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_profile_spiritual_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0043_alter_collection_collection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libraryobservation',
            name='observer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile_for_library_observation', to='users.profile'),
        ),
        migrations.AlterField(
            model_name='readingprogress',
            name='dear_soul',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_in_reading_progress', to=settings.AUTH_USER_MODEL),
        ),
    ]
