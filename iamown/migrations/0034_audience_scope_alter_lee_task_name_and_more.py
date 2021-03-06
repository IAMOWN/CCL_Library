# Generated by Django 4.0.4 on 2022-07-08 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iamown', '0033_alter_mailinglist_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='audience',
            name='scope',
            field=models.CharField(choices=[('Internal', 'Internal'), ('External', 'External'), ('Both', 'Both')], default='Internal', max_length=20),
        ),
        migrations.AlterField(
            model_name='lee',
            name='task_name',
            field=models.CharField(blank=True, default='', help_text='Enter the specific task name. This should not be changed once it has been coded into the application as this will be used in task assignment. Do not change this value unless you know what you are doing.', max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='peep',
            name='functional_activity',
            field=models.CharField(blank=True, default='', help_text='Enter the functional activity. Note: the application will only be able to act on this record if the applicable feature has been built into the application. However, please feel free to enter PEeP records for your reference, and to identify future ServiceFlow automation opportunities.', max_length=50, null=True, unique=True),
        ),
    ]
