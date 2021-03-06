# Generated by Django 4.0.4 on 2022-06-28 21:35

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_profile_first_name_remove_profile_last_name_and_more'),
        ('library', '0028_delete_recordobservation'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibraryObservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observation_type', models.CharField(choices=[('---', '---'), ('Typo', 'Typo'), ('Missing Image', 'Missing Image'), ('Broken Link', 'Broken Link'), ('Incorrect Header/Title', 'Incorrect Header/Title')], default='---', help_text='Please select the applicable observation type.', max_length=30)),
                ('typo', models.CharField(blank=True, default='', help_text='Please copy/paste in the incorrect text as observed from the record.', max_length=255, null=True)),
                ('suggested_correction', models.CharField(blank=True, default='', help_text='Please enter in your suggested correction.', max_length=255, null=True)),
                ('image_observation', tinymce.models.HTMLField(blank=True, null=True)),
                ('link_observation', tinymce.models.HTMLField(blank=True, null=True)),
                ('header_title_observation', tinymce.models.HTMLField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('observer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
    ]
