# Generated by Django 4.0.4 on 2022-06-25 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iamown', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.CharField(choices=[('---', '---'), ('Library Observation', 'Library Observation')], default='---', max_length=50),
        ),
    ]
