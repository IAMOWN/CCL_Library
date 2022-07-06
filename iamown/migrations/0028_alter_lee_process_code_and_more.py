# Generated by Django 4.0.4 on 2022-07-06 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iamown', '0027_lee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lee',
            name='process_code',
            field=models.CharField(blank=True, default='', help_text="If applicable. enter the process code for this process activity. The recommended format should be abbreviations of the organism's name and the process name. There is a 12 character limit for the Process Code.", max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='lee',
            name='relevant_django_file',
            field=models.CharField(blank=True, default='library/views.py', help_text='If applicable, enter the specific file path and file name within the Django web app.', max_length=100, null=True),
        ),
    ]
