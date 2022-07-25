# Generated by Django 4.0.4 on 2022-07-25 17:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0046_alter_collection_collection'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecordRead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_read', models.DateTimeField(auto_now_add=True)),
                ('reader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reader_of_record', to=settings.AUTH_USER_MODEL)),
                ('record_read', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='record_read_by_user', to='library.libraryrecord')),
            ],
            options={
                'ordering': ['date_read'],
            },
        ),
    ]