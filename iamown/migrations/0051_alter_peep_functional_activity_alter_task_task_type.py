# Generated by Django 4.0.4 on 2022-07-10 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iamown', '0050_alter_mailinglist_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peep',
            name='functional_activity',
            field=models.CharField(blank=True, default='', help_text='Enter the functional activity. Note: the application will only be able to act on this record if the applicable feature has been built into the application. However, please feel free to enter PEeP records for your reference, and to identify future ServiceFlow automation opportunities.', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.CharField(blank=True, choices=[('---', '---'), ('Decision', 'Decision'), ('Library Observation', 'Library Observation'), ('Book Edit', 'Book Edit'), ('Email Campaign', 'Email Campaign'), ('Email Campaign 2', 'Email Campaign 2')], default='---', max_length=50, null=True),
        ),
    ]