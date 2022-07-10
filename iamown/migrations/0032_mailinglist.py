# Generated by Django 4.0.4 on 2022-07-08 22:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('iamown', '0031_audience'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('subscribed', models.CharField(blank=True, choices=[('---', '---'), ('No', 'No'), ('Yes', 'Yes')], default='---', max_length=10, null=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('audience', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='audience_in_mailing_list', to='iamown.audience')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_in_mailing_list', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]