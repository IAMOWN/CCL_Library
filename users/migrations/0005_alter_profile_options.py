# Generated by Django 4.0.4 on 2022-07-24 23:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_profile_pronoun'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['spiritual_name']},
        ),
    ]