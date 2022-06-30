# Generated by Django 4.0.4 on 2022-06-29 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iamown', '0017_task_date_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.CharField(blank=True, choices=[('---', '---'), ('Library Observation', 'Library Observation'), ('Book Edit', 'Book Edit')], default='---', max_length=50, null=True),
        ),
    ]