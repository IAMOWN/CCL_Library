# Generated by Django 4.0.4 on 2022-07-10 16:48

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('iamown', '0051_alter_peep_functional_activity_alter_task_task_type'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='peep',
            unique_together={('functional_activity', 'dear_soul_responsible')},
        ),
    ]